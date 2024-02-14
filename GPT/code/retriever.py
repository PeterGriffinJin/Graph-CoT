import glob
import os
import sys
import json
import pickle
from contextlib import nullcontext
from typing import Dict, List
import logging
import math

import faiss
import numpy as np
import torch
from torch.cuda import amp
from torch.utils.data import DataLoader, IterableDataset
from tqdm import tqdm
import sentence_transformers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from IPython import embed

NODE_TEXT_KEYS = {'maple': {'paper': ['title'], 'author': ['name'], 'venue': ['name']},
                  'amazon': {'item': ['title'], 'brand': ['name']},
                  'biomedical': {'Anatomy': ['name'], 'Biological_Process':['name'], 'Cellular_Component':['name'], 'Compound':['name'], 'Disease':['name'], 'Gene':['name'], 'Molecular_Function':['name'], 'Pathway':['name'], 'Pharmacologic_Class':['name'], 'Side_Effect':['name'], 'Symptom':['name']},
                  'legal': {'opinion': ['plain_text'], 'opinion_cluster': ['syllabus'], 'docket': ['pacer_case_id', 'case_name'], 'court': ['full_name']},
                  'goodreads': {'book': ['title'], 'author': ['name'], 'publisher': ['name'], 'series': ['title']},
                  'dblp': {'paper': ['title'], 'author': ['name', 'organization'], 'venue': ['name']}
                  }

RELATION_NODE_TYPE_MAP = {'maple': {'author': 'author', 'venue': 'venue', 'reference': 'paper', 'cited_by': 'paper', 'paper': 'paper'},
                          'amazon': {'also_viewed_item': 'item', 'buy_after_viewing_item': 'item', 'also_bought_item': 'item', 'bought_together_item': 'item', 'brand': 'brand', 'item': 'item'},
                          'biomedical': {'Disease-localizes-Anatomy': ['Anatomy', 'Disease'], 'Anatomy-expresses-Gene': ['Anatomy', 'Gene'],
                                         'Anatomy-downregulates-Gene': ['Anatomy', 'Gene'], 'Anatomy-upregulates-Gene': ['Anatomy', 'Gene'],
                                         'Gene-participates-Biological Process': ['Biological_Process', 'Gene'],
                                         'Gene-participates-Cellular Component': ['Cellular_Component', 'Gene'],
                                         'Compound-causes-Side Effect': ['Compound', 'Side_Effect'],
                                         'Compound-resembles-Compound': ['Compound'], 'Compound-binds-Gene': ['Compound', 'Gene'],
                                         'Compound-downregulates-Gene': ['Compound', 'Gene'], 'Compound-palliates-Disease': ['Compound', 'Disease'],
                                         'Pharmacologic Class-includes-Compound': ['Compound', 'Pharmacologic_Class'],
                                         'Compound-upregulates-Gene': ['Compound', 'Gene'], 'Compound-treats-Disease': ['Compound', 'Disease'],
                                         'Disease-upregulates-Gene': ['Disease', 'Gene'], 'Disease-downregulates-Gene': ['Disease', 'Gene'],
                                         'Disease-associates-Gene': ['Disease', 'Gene'], 'Disease-presents-Symptom': ['Disease', 'Symptom'],
                                         'Disease-resembles-Disease': ['Disease'], 'Gene-regulates-Gene': ['Gene'], 'Gene-interacts-Gene': ['Gene'],
                                         'Gene-participates-Pathway': ['Gene', 'Pathway'], 'Gene-participates-Molecular Function': ['Gene', 'Molecular_Function'],
                                         'Gene-covaries-Gene': ['Gene']},
                          'legal': {'opinion_cluster': 'opinion_cluster', 'reference': 'opinion', 'cited_by': 'opinion', 'opinion': 'opinion', 'docket': 'docket', 'court': 'court'},
                          'goodreads': {'author': 'author', 'publisher': 'publisher', 'series': 'series', 'similar_books': 'book', 'book': 'book'},
                          'dblp': {'author': 'author', 'venue': 'venue', 'reference': 'paper', 'cited_by': 'paper', 'paper': 'paper'}
                          }

FEATURE_NODE_TYPE = {'maple': {'paper': ['title'], 'author': ['name'], 'venue': ['name']},
                  'amazon': {'item': ['title', 'price', 'category'], 'brand': ['name']},
                  'biomedical': {'Anatomy': ['name'], 'Biological_Process':['name'], 'Cellular_Component':['name'], 'Compound':['name'], 'Disease':['name'], 'Gene':['name'], 'Molecular_Function':['name'], 'Pathway':['name'], 'Pharmacologic_Class':['name'], 'Side_Effect':['name'], 'Symptom':['name']},
                  'legal': {'opinion': ['plain_text'], 'opinion_cluster': ['syllabus', 'judges'], 'docket': ['pacer_case_id', 'case_name'], 'court': ['full_name', 'start_date', 'end_date', 'citation_string']},
                  'goodreads': {'book': ['title', 'popular_shelves', 'genres', 'publication_year', 'num_pages', 'is_ebook', 'language_code', 'format'], 'author': ['name'], 'publisher': ['name'], 'series': ['title']},
                  'dblp': {'paper': ['title'], 'author': ['name', 'organization'], 'venue': ['name']}
                  }

class Retriever:

    def __init__(self, args, graph, cache=True, cache_dir=None):
        logger.info("Initializing retriever")

        self.dataset = args.dataset
        self.use_gpu = args.faiss_gpu
        self.node_text_keys = args.node_text_keys
        self.model_name = args.embedder_name
        self.model = sentence_transformers.SentenceTransformer(args.embedder_name)
        self.graph = graph
        self.cache = args.embed_cache
        self.cache_dir = args.embed_cache_dir

        self.reset()

    def reset(self):

        docs, ids, meta_type = self.process_graph()
        save_model_name = self.model_name.split('/')[-1]

        if self.cache and os.path.isfile(os.path.join(self.cache_dir, f'cache-{save_model_name}.pkl')):
            embeds, self.doc_lookup, self.doc_type = pickle.load(open(os.path.join(self.cache_dir, f'cache-{save_model_name}.pkl'), 'rb'))
            assert self.doc_lookup == ids
            assert self.doc_type == meta_type
        else:
            embeds = self.multi_gpu_infer(docs)
            self.doc_lookup = ids
            self.doc_type = meta_type
            pickle.dump([embeds, ids, meta_type], open(os.path.join(self.cache_dir, f'cache-{save_model_name}.pkl'), 'wb'))

        self.init_index_and_add(embeds)

    def process_graph(self):
        docs = []
        ids = []
        meta_type = []

        for node_type_key in self.graph.keys():
            node_type = node_type_key.split('_nodes')[0]
            logger.info(f'loading text for {node_type}')
            for nid in tqdm(self.graph[node_type_key]):
                tmp_string = ''
                for k in self.node_text_keys[node_type]:
                    vv = self.graph[node_type_key][nid]['features'][k]
                    tmp_string += k + ": " + str(vv) + '. ' if (isinstance(vv, str) or not math.isnan(vv)) else ''
                # docs.append(self.graph[node_type_key][nid]['features'][self.node_text_keys[node_type][0]])
                docs.append(tmp_string)
                ids.append(nid)
                meta_type.append(node_type)
        return docs, ids, meta_type

    def multi_gpu_infer(self, docs):
        pool = self.model.start_multi_process_pool()
        embeds = self.model.encode_multi_process(docs, pool)
        return embeds

    def _initialize_faiss_index(self, dim: int):
        self.index = None
        cpu_index = faiss.IndexFlatIP(dim)
        self.index = cpu_index

    def _move_index_to_gpu(self):
        logger.info("Moving index to GPU")
        ngpu = faiss.get_num_gpus()
        gpu_resources = []
        for i in range(ngpu):
            res = faiss.StandardGpuResources()
            gpu_resources.append(res)
        co = faiss.GpuMultipleClonerOptions()
        co.shard = True
        co.usePrecomputed = False
        vres = faiss.GpuResourcesVector()
        vdev = faiss.Int32Vector()
        for i in range(0, ngpu):
            vdev.push_back(i)
            vres.push_back(gpu_resources[i])
        self.index = faiss.index_cpu_to_gpu_multiple(vres, vdev, self.index, co)

    def init_index_and_add(self, embeds):
        
        logger.info("Initialize the index...")
        dim = embeds.shape[1]
        self._initialize_faiss_index(dim)
        self.index.add(embeds)

        if self.use_gpu:
            self._move_index_to_gpu()

    @classmethod
    def build_embeddings(cls, model, corpus_dataset, args):
        retriever = cls(model, corpus_dataset, args)
        retriever.doc_embedding_inference()
        return retriever

    @classmethod
    def from_embeddings(cls, model, args):
        retriever = cls(model, None, args)
        if args.process_index == 0:
            retriever.init_index_and_add()
        if args.world_size > 1:
            torch.distributed.barrier()
        return retriever

    def reset_index(self):
        if self.index:
            self.index.reset()
        self.doc_lookup = []
        self.query_lookup = []

    def search_single(self, query, hop=1, topk=10):
        # logger.info("Searching")
        if self.index is None:
            raise ValueError("Index is not initialized")
        
        query_embed = self.model.encode(query, show_progress_bar=False)

        D, I = self.index.search(query_embed[None,:], topk)
        original_indice = np.array(self.doc_lookup)[I].tolist()[0][0]
        original_type = np.array(self.doc_type)[I].tolist()[0][0]

        if hop == 1:
            context = self.one_hop(original_type, original_indice)
        elif hop == 2:
            context = self.two_hop(original_type, original_indice)
        elif hop == 0:
            context = self.zero_hop(original_type, original_indice)
        else:
            raise ValueError('Ego graph should be 0-hop, 1-hop or 2-hop.')

        return context

    def linearize_feature(self, node_type, node_indice):
        text = ''
        for f_name in self.graph[f'{node_type}_nodes'][node_indice]['features']:
            if f_name in FEATURE_NODE_TYPE[self.dataset][node_type]:
                val = self.graph[f'{node_type}_nodes'][node_indice]['features'][f_name]
                if isinstance(val, str):
                    text += f_name + ': ' + val + '. '
                elif isinstance(val, float):
                    text += f_name + ': ' + str(val) + '. '
                elif isinstance(val, List):
                    text += f_name + ': ' + ', '.join(val) + '. '
                elif math.isnan(val):
                    continue
                else:
                    print(val)
                    raise ValueError('Something is wrong here!')
        return text

    def zero_hop(self, node_type, node_indice):
        context = 'Center node: '
        # add feature
        context += self.linearize_feature(node_type, node_indice)
        return context

    def one_hop(self, node_type, node_indice, sample_n=20):
        context = 'Center node: '
        # add feature
        context += self.linearize_feature(node_type, node_indice)
        # add neighbor info
        for neighbor_type in self.graph[f'{node_type}_nodes'][node_indice]['neighbors']:
            context += neighbor_type + ': '
            for nid in self.graph[f'{node_type}_nodes'][node_indice]['neighbors'][neighbor_type][:sample_n]:
                if isinstance(RELATION_NODE_TYPE_MAP[self.dataset][neighbor_type], str):
                    try:
                        context += self.linearize_feature(RELATION_NODE_TYPE_MAP[self.dataset][neighbor_type], nid)
                    except:
                        pass
                elif isinstance(RELATION_NODE_TYPE_MAP[self.dataset][neighbor_type], List):
                    for ntt in RELATION_NODE_TYPE_MAP[self.dataset][neighbor_type]:
                        try:
                            context += self.linearize_feature(ntt, nid)
                        except:
                            pass
                else:
                    raise ValueError('Something is going wrong here.')
        
        return context

    def two_hop(self, node_type, node_indice, sample_n=20):
        context = 'Center node: '
        # add feature
        context += self.linearize_feature(node_type, node_indice)
        # add neighbor info
        for neighbor_type in self.graph[f'{node_type}_nodes'][node_indice]['neighbors']:
            context += neighbor_type + ': '
            for nid in self.graph[f'{node_type}_nodes'][node_indice]['neighbors'][neighbor_type][:sample_n]:
                try:
                    context += '[' + self.one_hop(neighbor_type, nid) + '].'
                except:
                    pass
        return context


if __name__ == '__main__':
    model_name = "sentence-transformers/all-mpnet-base-v2"
    graph_dir = "/home/ec2-user/quic-efs/user/bowenjin/llm-graph-plugin/data/processed_data/maple/Physics/graph.json"
    node_text_keys = {'paper': ['title'], 'author': ['name'], 'venue': ['name']}

    query = "quantum physics and machine learning"

    graph = json.load(open(graph_dir))
    node_retriever = Retriever(graph, model_name, node_text_keys, use_gpu=False)
    idd, node = node_retriever.search_single(query, 1)
    print(idd, node)
