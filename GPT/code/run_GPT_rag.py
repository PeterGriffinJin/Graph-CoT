
import os
import re
import tqdm
import time
import json
import openai
import jsonlines
import argparse
from transformers import AutoTokenizer

from typing import List, Dict, Any
import asyncio
from openai import AsyncOpenAI
import logging

from retriever import Retriever, NODE_TEXT_KEYS

from IPython import embed

logging.basicConfig(level=logging.INFO)
logging.getLogger('httpx').setLevel(logging.WARNING)
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


async def dispatch_openai_requests(
    args,
    messages_list: List[List[Dict[str, Any]]],
    model: str,
    temperature: float,
    max_tokens: int,
    top_p: float,
) -> List[str]:
    """Dispatches requests to OpenAI API asynchronously.
    
    Args:
        messages_list: List of messages to be sent to OpenAI ChatCompletion API.
        model: OpenAI model to use.
        temperature: Temperature to use for the model.
        max_tokens: Maximum number of tokens to generate.
        top_p: Top p to use for the model.
    Returns:
        List of responses from OpenAI API.
    """
    
    client = AsyncOpenAI(api_key=args.openai_key)
    async_responses = [
        client.chat.completions.create(
            model=model,
            messages=x,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
        )
        for x in messages_list
    ]
    return await asyncio.gather(*async_responses)

def main():
    parser = argparse.ArgumentParser("")
    parser.add_argument("--dataset", type=str, default="maple")
    parser.add_argument("--gpt_version", type=str, default="gpt-3.5-turbo")
    parser.add_argument("--graph_dir", type=str, default="None")
    parser.add_argument("--path", type=str, default="None")
    parser.add_argument("--save_file", type=str, default="None")
    parser.add_argument("--openai_key", type=str, default="None")
    parser.add_argument("--embedder_name", type=str, default="sentence-transformers/all-mpnet-base-v2")
    parser.add_argument("--faiss_gpu", type=bool, default=False)
    parser.add_argument("--embed_cache", type=bool, default=True)
    parser.add_argument("--hop", type=int, default=1)
    parser.add_argument("--max_len", type=int, default=4096)
    parser.add_argument("--retrieve_graph_hop", type=int, default=1)
    parser.add_argument("--graph_max_len", type=int, default=3000)
    args = parser.parse_args()

    args.embed_cache_dir = args.path
    args.graph_dir = os.path.join(args.path, "graph.json")
    args.data_dir = os.path.join(args.path, "data.json")
    args.retrieval_context_dir = os.path.join(args.path, f"retrieval_context_{args.retrieve_graph_hop}.json")
    args.node_text_keys = NODE_TEXT_KEYS[args.dataset]

    # truncate
    def truncate_string(input_text, tokenizer, max_len):
        return tokenizer.decode(tokenizer.encode(input_text, add_special_tokens=False, truncation=True, max_length=max_len))

    assert args.gpt_version in ['gpt-3.5-turbo', 'gpt-4', 'gpt-3.5-turbo-16k']
    openai.api_key = args.openai_key

    file_path = args.data_dir
    with open(file_path, 'r') as f:
        contents = []
        for item in jsonlines.Reader(f):
            contents.append(item)
    tokenizer = AutoTokenizer.from_pretrained('meta-llama/Llama-2-13b-chat-hf', use_fast=False) # this is for truncation only

    # retriever
    if not os.path.exists(args.retrieval_context_dir):
        contexts = []
        logger.info('Loading the graph...')
        graph = json.load(open(args.graph_dir))
        retriever = Retriever(args, graph)
        
        logger.info('Retrieving...')
        for item in tqdm.tqdm(contents):
            message = item["question"]
            context = truncate_string(retriever.search_single(query=message, hop=args.retrieve_graph_hop, topk=1), tokenizer, args.graph_max_len)
            contexts.append(context)
        save_jsonl_lines(args.retrieval_context_dir, contexts)
    else:
        logger.info('Loading previous retrieved context...')
        contexts = read_jsonl_lines(args.retrieval_context_dir)
    assert len(contexts) == len(contents)
    
    # inference
    system_message = "You are an AI assistant to answer questions. Please use your own knowledge and the given context to answer the questions. If you do not know the answer, please guess a most probable answer. Only include the answer in your response. Do not explain."
    query_messages = []
    
    # for item in contents:
    for i in tqdm.tqdm(range(len(contents))):
        # message = item["question"]
        message = contents[i]["question"]
        # context = truncate_string(retriever.search_single(query=message, hop=args.retrieve_graph_hop, topk=1), tokenizer, args.graph_max_len)
        context = contexts[i]
        message = system_message + message + '\nContext: ' + context
        # contexts.append(context)
        query_messages.append([
            {"role": "system", "content": system_message},
            {"role": "user", "content": message}
        ])
    logger.info('Retrieval step finished!')
        
    generated_text = []
    for i in tqdm.trange(0, len(query_messages), 5):
        try:
            response = asyncio.run(
                dispatch_openai_requests(
                    args,
                    messages_list=query_messages[i:i+5],
                    model=args.gpt_version,
                    temperature=0.01,
                    max_tokens=args.max_len,
                    top_p=1.0,
                )
            )
            time.sleep(15)
        except:
            print("rate limit exceeded, sleep for 60 seconds")
            time.sleep(60)
            response = asyncio.run(
                dispatch_openai_requests(
                    args,
                    messages_list=query_messages[i:i+5],
                    model=args.gpt_version,
                    temperature=0.01,
                    max_tokens=args.max_len,
                    top_p=1.0,
                )
            )
        # try:
        for j in range(len(response)):
            generated_text.append({"question": contents[i+j]["question"], "context": contexts[i+j], "model_answer": response[j].choices[0].message.content, "gt_answer": contents[i+j]["answer"]})

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
