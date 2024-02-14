import os
import re
import tqdm
import time
import logging
import openai
import jsonlines
import argparse

from typing import List, Dict, Any
import asyncio
from openai import AsyncOpenAI

from IPython import embed

logging.basicConfig(level=logging.INFO)
logging.getLogger('httpx').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

def clean_str(string):
    pattern = re.compile(r'^\d+\. ', flags=re.MULTILINE)
    string = pattern.sub('', string)
    return string.strip()

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
    parser.add_argument("--data_file", type=str, default="None")
    parser.add_argument("--save_file", type=str, default="None")
    parser.add_argument("--openai_key", type=str, default="None")
    args = parser.parse_args()

    assert args.gpt_version in ['gpt-3.5-turbo', 'gpt-4']
    openai.api_key = args.openai_key

    file_path = args.data_file
    with open(file_path, 'r') as f:
        contents = []
        for item in jsonlines.Reader(f):
            contents.append(item)
    
    system_message = "You are an AI assistant to answer questions. Please use your own knowledge to answer the questions. If you do not know the answer, please guess a most probable answer. Only include the answer in your response. Do not explain."
    query_messages = []
    for item in contents:
        message = item["question"]
        query_messages.append([
            {"role": "system", "content": system_message},
            {"role": "user", "content": message}
        ])
    generated_text = []
    
    for i in tqdm.trange(0, len(query_messages), 20):
        try:
            response = asyncio.run(
                dispatch_openai_requests(
                    args,
                    messages_list=query_messages[i:i+20],
                    model=args.gpt_version,
                    temperature=0.01,
                    max_tokens=2048,
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
                    messages_list=query_messages[i:i+20],
                    model=args.gpt_version,
                    temperature=0.01,
                    max_tokens=2048,
                    top_p=1.0,
                )
            )
        # try:
        for j in range(len(response)):
            generated_text.append({"question": contents[i+j]["question"], "model_answer": response[j].choices[0].message.content, "gt_answer": contents[i+j]["answer"]})

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
