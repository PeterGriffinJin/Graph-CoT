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

from typing import List, Dict, Any
import asyncio

from IPython import embed

def clean_str(string):
    pattern = re.compile(r'^\d+\. ', flags=re.MULTILINE)
    string = pattern.sub('', string)
    return string.strip()

def main():
    parser = argparse.ArgumentParser("")
    parser.add_argument("--version", type=str, default="meta-llama/Llama-2-13b-chat-hf")
    parser.add_argument("--data_file", type=str, default="None")
    parser.add_argument("--save_file", type=str, default="None")
    args = parser.parse_args()

    assert args.version in ["meta-llama/Llama-2-7b-hf", "meta-llama/Llama-2-7b-chat-hf", "meta-llama/Llama-2-13b-hf", 
                            "meta-llama/Llama-2-13b-chat-hf", "meta-llama/Llama-2-70b-hf", "meta-llama/Llama-2-70b-chat-hf",
                            "allenai/open-instruct-stanford-alpaca-7b", "mistralai/Mixtral-8x7B-Instruct-v0.1"]

    # model = f"meta-llama/{args.version}"
    model = args.version
    tokenizer = AutoTokenizer.from_pretrained(model, use_auth_token=True)
    pipeline = transformers.pipeline(
        "text-generation",
        model=model,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    # file_path = "/home/ec2-user/quic-efs/user/bowenjin/llm-graph-plugin/data/processed_data/maple/Physics/data.json"
    file_path = args.data_file
    with open(file_path, 'r') as f:
        contents = []
        for item in jsonlines.Reader(f):
            contents.append(item)
    
    system_message = "You are an AI assistant to answer questions. Please use your own knowledge to answer the questions. If you do not know the answer, please guess a most probable answer. Only include the answer in your response. Do not explain.\nQuestion: "
    query_messages = []
    attributes = []
    response = []
    for item in tqdm(contents):
        message = item["question"]
        message = system_message + message + '\nAnswer: '
        msg_list = pipeline(
                        message,
                        do_sample=True,
                        top_k=10,
                        num_return_sequences=1,
                        eos_token_id=tokenizer.eos_token_id,
                        max_length=1000,
                    )
        # response.append(msg_list[0]["generated_text"])
        response.append(msg_list[0]["generated_text"].split(message)[-1])

    generated_text = []
    for j in range(len(response)):
        generated_text.append({"question": contents[j]["question"], "model_answer": response[j], "gt_answer": contents[j]["answer"]})

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
