import jsonlines
import argparse
from tqdm import tqdm
import os

import os
import re
import time
import requests
import json
import openai
import jsonlines
from transformers import AutoTokenizer
import transformers
import torch
import sentence_transformers
import logging

from typing import List, Dict, Any
import asyncio
from retriever import Retriever, NODE_TEXT_KEYS

from IPython import embed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_str(string):
    pattern = re.compile(r'^\d+\. ', flags=re.MULTILINE)
    string = pattern.sub('', string)
    return string.strip()

def read_jsonl_lines(file):
    context = []
    with open(file) as f:
        readin = f.readlines()
        for line in readin:
            # context.add(line.strip())
            context.append(json.loads(line.strip())['context'])
    return context

def save_jsonl_lines(file, contexts):
    with open(file, 'w') as fout:
        for context in contexts:
            # fout.write(context + '\n')
            fout.write(json.dumps({'context': context}) + '\n')


def main():
    parser = argparse.ArgumentParser("")
    parser.add_argument("--dataset", type=str, default="flights")
    parser.add_argument("--version", type=str, default="meta-llama/Llama-2-13b-chat-hf")
    # parser.add_argument("--retriever", type=str, default="meta-llama/Llama-2-13b-chat-hf")
    parser.add_argument("--graph_dir", type=str, default="None")
    parser.add_argument("--path", type=str, default="None")
    parser.add_argument("--save_file", type=str, default="None")
    parser.add_argument("--embedder_name", type=str, default="sentence-transformers/all-mpnet-base-v2")
    parser.add_argument("--faiss_gpu", type=bool, default=False)
    parser.add_argument("--embed_cache", type=bool, default=True)
    parser.add_argument("--hop", type=int, default=1)
    parser.add_argument("--max_len", type=int, default=1000)
    parser.add_argument("--retrieve_graph_hop", type=int, default=1)
    parser.add_argument("--graph_max_len", type=int, default=3000)

    args = parser.parse_args()

    assert args.version in ["meta-llama/Llama-2-7b-hf", "meta-llama/Llama-2-7b-chat-hf", "meta-llama/Llama-2-13b-hf", 
                            "meta-llama/Llama-2-13b-chat-hf", "meta-llama/Llama-2-70b-hf", "meta-llama/Llama-2-70b-chat-hf",
                            "allenai/open-instruct-stanford-alpaca-7b", "mistralai/Mixtral-8x7B-Instruct-v0.1"]

    args.embed_cache_dir = args.path
    args.graph_dir = os.path.join(args.path, "graph.json")
    args.data_dir = os.path.join(args.path, "data.json")
    args.retrieval_context_dir = os.path.join(args.path, f"retrieval_context_{args.retrieve_graph_hop}.json")
    args.node_text_keys = NODE_TEXT_KEYS[args.dataset]

    # model = f"meta-llama/{args.version}"
    model = args.version
    tokenizer = AutoTokenizer.from_pretrained(model, use_auth_token=True)
    pipeline = transformers.pipeline(
        "text-generation",
        model=model,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    # truncate
    def truncate_string(input_text, tokenizer, max_len):
        return tokenizer.decode(tokenizer.encode(input_text, add_special_tokens=False, truncation=True, max_length=max_len))

    # file_path = "/home/ec2-user/quic-efs/user/bowenjin/llm-graph-plugin/data/processed_data/maple/Physics/data.json"
    file_path = args.data_dir
    with open(file_path, 'r') as f:
        contents = []
        for item in jsonlines.Reader(f):
            contents.append(item)

    # retriever
    if not os.path.exists(args.retrieval_context_dir):
        contexts = []
        logger.info('Loading the graph...')
        graph = json.load(open(args.graph_dir))
        retriever = Retriever(args, graph)
        
        logger.info('Retrieving...')
        for item in tqdm(contents):
            message = item["question"]
            context = truncate_string(retriever.search_single(query=message, hop=args.retrieve_graph_hop, topk=1), tokenizer, args.graph_max_len)
            contexts.append(context)
        save_jsonl_lines(args.retrieval_context_dir, contexts)
    else:
        logger.info('Loading previous retrieved context...')
        contexts = read_jsonl_lines(args.retrieval_context_dir)
    assert len(contexts) == len(contents)
    
    # inference
    system_message = "You are an AI assistant to answer questions. Please use your own knowledge to answer the questions. If you do not know the answer, please guess a most probable answer. Only include the answer in your response. Do not explain.\nQuestion: "
    response = []
    # for item, context in tqdm(zip(contents, contexts)):
    for i in tqdm(range(len(contents))):
        message = contents[i]["question"]
        context = contexts[i]
        # context = truncate_string(retriever.search_single(query=message, hop=args.retrieve_graph_hop, topk=1), tokenizer, args.graph_max_len)
        message = system_message + message + '\nContext: ' + context + '\nAnswer: '
        msg_list = pipeline(
                        message,
                        do_sample=True,
                        top_k=10,
                        num_return_sequences=1,
                        eos_token_id=tokenizer.eos_token_id,
                        max_length=args.max_len,
                    )
        # response.append(msg_list[0]["generated_text"])
        response.append((msg_list[0]["generated_text"].split(message)[-1], context))

    generated_text = []
    for j in range(len(response)):
        generated_text.append({"question": contents[j]["question"], "context": response[j][1], "model_answer": response[j][0], "gt_answer": contents[j]["answer"]})

    print(generated_text[0], len(generated_text))
    output_file_path = args.save_file
    
    parent_folder = os.path.dirname(output_file_path)
    parent_parent_folder = os.path.dirname(parent_folder)
    if not os.path.exists(parent_parent_folder):
        os.mkdir(parent_parent_folder)
    if not os.path.exists(parent_folder):
        os.mkdir(parent_folder)
    
    with jsonlines.open(output_file_path, 'w') as writer:
        for row in generated_text:
            writer.write(row)

if __name__ == '__main__':
    main()
