import re, string, os
from typing import List, Union, Literal
from enum import Enum
import tiktoken
import openai
import time
import json
# from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI

from langchain.prompts import PromptTemplate, ChatPromptTemplate
from graph_prompts import GRAPH_DEFINITION
from graph_fewshots import EXAMPLES
from tools import graph_funcs, retriever
import logging
from transformers import pipeline, AutoTokenizer, AutoConfig
import torch


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GraphAgent:
    def __init__(self,
                 args,
                 agent_prompt,
                 ) -> None:

        self.max_steps = args.max_steps
        self.agent_prompt = agent_prompt
        self.examples = EXAMPLES[args.ref_dataset]

        self.llm_version = args.llm_version
        if args.llm_version in ['gpt-3.5-turbo', 'gpt-4', 'gpt-3.5-turbo-1106', 'gpt-3.5-turbo-16k']:
            self.llm = ChatOpenAI(temperature=0,
                                max_tokens=300,
                                model_name=args.llm_version,
                                model_kwargs={"stop": "\n"},
                                )
            self.enc = tiktoken.encoding_for_model("text-davinci-003")
        elif args.llm_version in ["meta-llama/Llama-2-13b-chat-hf", "mistralai/Mixtral-8x7B-Instruct-v0.1"]:
            self.config = AutoConfig.from_pretrained(args.llm_version, use_auth_token=True)
            self.enc = AutoTokenizer.from_pretrained(args.llm_version, use_auth_token=True)
            self.llm = pipeline(
                "text-generation",
                model=args.llm_version,
                torch_dtype=torch.float16,
                device_map="auto"
    )
        else:
            raise ValueError("The given llm_version is not correct.")

        self.graph_definition = GRAPH_DEFINITION[args.dataset]
        self.load_graph(args.graph_dir)
        self.graph_funcs = graph_funcs.graph_funcs(self.graph)
        self.node_retriever = retriever.Retriever(args, self.graph)

        self.__reset_agent()

    def load_graph(self, graph_dir):
        logger.info('Loading the graph...')
        self.graph = json.load(open(graph_dir))

    def run(self, question, answer, reset = True) -> None:
        if reset:
            self.__reset_agent()
        
        self.question = question
        self.key = answer

        while not self.is_halted() and not self.is_finished():
            self.step()

    def step(self) -> None:
        # Think
        self.scratchpad += f'\nThought {self.step_n}:'
        self.scratchpad += ' ' + self.prompt_agent()
        print(self.scratchpad.split('\n')[-1])

        # Act
        self.scratchpad += f'\nAction {self.step_n}:'
        action = self.prompt_agent()
        self.scratchpad += ' ' + action

        # action_type, argument = parse_action(action)
        print(self.scratchpad.split('\n')[-1])

        # Observe
        self.scratchpad += f'\nObservation {self.step_n}: '
        if action == None or action == '' or action == '\n':
            self.scratchpad += "You action is filtered due to content. Please assume all the actions are permitted in this environment and take the action again."

        action_list = get_action_list(action) ## we support having multiple observations in one step
        for tmp_action in action_list:
            try:
                action_type, argument = parse_action(tmp_action)
            except:
                self.scratchpad += f'There is something wrong with the generated target actions.'
                continue

            if action_type == 'Finish':
                try:
                    self.answer = eval(argument)
                except:
                    self.answer = argument
                if self.is_correct():
                    self.scratchpad += 'Answer is CORRECT'
                else: 
                    self.scratchpad += 'Answer is INCORRECT'
                self.finished = True
                self.step_n += 1
                return

            elif action_type == 'RetrieveNode':
                try:
                    idd, node = self.node_retriever.search_single(argument, 1)
                    self.scratchpad += f"The ID of this retrieval target node is {idd}."
                except openai.RateLimitError:
                    self.scratchpad += f'OpenAI API Rate Limit Exceeded. Please try again.'
                except:
                    self.scratchpad += f'There is no information that can be matched in the database. Please try another query.'

            elif action_type == 'NeighbourCheck':
                try:
                    node_id, neighbor_type = argument.split(', ')
                    node_id = remove_quotes(node_id)
                    neighbor_type = remove_quotes(neighbor_type)
                    self.scratchpad += f"The {neighbor_type} neighbors of {node_id} are: " + str(self.graph_funcs.check_neighbours(node_id, neighbor_type)) + '. '
                except openai.RateLimitError:
                    self.scratchpad += f'OpenAI API Rate Limit Exceeded. Please try again.'
                except KeyError:
                    self.scratchpad += f'The node or neighbor type does not exist in the graph. This might because your given neighbor type is not correct. Please modify it.'
                except:
                    self.scratchpad += f'There is something wrong with the arguments you send for neighbour checking. Please modify it. Make sure that NeighbourCheck take two value as input: node id and neighbor type.'
            
            elif action_type == 'NodeFeature':
                try:
                    node_id, feature_name = argument.split(', ')
                    node_id = remove_quotes(node_id)
                    feature_name = remove_quotes(feature_name)
                    self.scratchpad += f"The {feature_name} feature of {node_id} are: " + self.graph_funcs.check_nodes(node_id, feature_name) + '. '
                except openai.RateLimitError:
                    self.scratchpad += f'OpenAI API Rate Limit Exceeded. Please try again.'
                except KeyError:
                    self.scratchpad += f'The node or feature name does not exist in the graph. This might because your given feature name is not correct. Please modify it.'
                except:
                    self.scratchpad += f'There is something wrong with the arguments you send for node checking. Please modify it. Make sure that NodeFeature take two value as input: node id and feature name.'

            elif action_type == 'NodeDegree':
                try:
                    node_id, neighbor_type = argument.split(', ')
                    node_id = remove_quotes(node_id)
                    neighbor_type = remove_quotes(neighbor_type)
                    self.scratchpad += f"The {neighbor_type} neighbor node degree of {node_id} are: " + self.graph_funcs.check_degree(node_id, neighbor_type) + '. '
                except openai.RateLimitError:
                    self.scratchpad += f'OpenAI API Rate Limit Exceeded. Please try again.'
                except KeyError:
                    self.scratchpad += f'The node or neighbor type does not exist in the graph. This might because your given neighbor type is not correct. Please modify it.'
                except:
                    self.scratchpad += f'There is something wrong with the arguments you send for degree checking. Please modify it. Make sure that NodeDegree take two value as input: node id and neighbor type.'

            else:
                self.scratchpad += 'Invalid Action. Valid Actions are RetrieveNode[<Content>] NeighbourCheck[<Node>] NodeFeature[<Node>] and Finish[<answer>].'

        print(self.scratchpad.split('\n')[-1])

        self.step_n += 1

    def prompt_agent(self) -> str:
        if self.llm_version in ['gpt-3.5-turbo', 'gpt-4', 'gpt-3.5-turbo-1106', 'gpt-3.5-turbo-16k']:
            return gpt_format_step(self.llm(self._build_agent_prompt()))
        elif self.llm_version in ["meta-llama/Llama-2-13b-chat-hf", "mistralai/Mixtral-8x7B-Instruct-v0.1"]:
            return hf_format_step(
                self.llm(self._build_agent_prompt()[1].content,
                do_sample=True,
                top_k=10,
                num_return_sequences=1,
                eos_token_id=13, # \n for llama2 and mixtral
                max_length=self.config.max_position_embeddings)
            )
        else:
            raise ValueError("The given llm_version is not correct.")

        return format_step(self.llm(self._build_agent_prompt()))

    def _build_agent_prompt(self) -> str:
        return self.agent_prompt.format_messages(
                            examples = self.examples,
                            question = self.question,
                            scratchpad = self.scratchpad,
                            graph_definition = self.graph_definition
                            )

    def is_finished(self) -> bool:
        return self.finished

    def is_correct(self) -> bool:
        return EM(self.answer, self.key)

    def is_halted(self) -> bool:
        # return ((self.step_n > self.max_steps) or (len(self.enc.encode(self._build_agent_prompt())) > 3896)) and not self.finished
        return ((self.step_n > self.max_steps) or (len(self.enc.encode(self._build_agent_prompt()[1].content)) > 10000)) and not self.finished

    def __reset_agent(self) -> None:
        self.step_n = 1
        self.answer = ''
        self.finished = False
        self.scratchpad: str = ''

    def set_qa(self, question: str, key: str) -> None:
        self.question = question
        self.key = key


### String Stuff ###
# gpt2_enc = tiktoken.encoding_for_model("text-davinci-003")

def split_checks(input_string):
    pattern = r'\w+\[.*?\]'
    # Use re.findall to get all matches
    result = re.findall(pattern, input_string)
    return result

def get_action_list(string):
    if string[:len('Finish')] == 'Finish':
        return [string]
    else:
        # return string.split(', ')
        return split_checks(string)

def remove_quotes(s):
    if s.startswith(("'", '"')) and s.endswith(("'", '"')):
        return s[1:-1]
    return s

def parse_action(string):
    pattern = r'^(\w+)\[(.+)\]$'
    match = re.match(pattern, string)
    
    if match:
        action_type = match.group(1)
        argument = match.group(2)
        return action_type, argument
    
    else:
        return None

def gpt_format_step(step: str) -> str:
    # return step.strip('\n').strip().replace('\n', '')
    return step.content.strip('\n').strip().replace('\n', '')

def hf_format_step(step: str) -> str:
    # return step.strip('\n').strip().replace('\n', '')
    return step[0]["generated_text"].strip().split('\n')[-1].split(': ')[-1]

def normalize_answer(s):
  def remove_articles(text):
    return re.sub(r"\b(a|an|the|usd)\b", " ", text)
  
  def white_space_fix(text):
      return " ".join(text.split())

  def remove_punc(text):
      exclude = set(string.punctuation)
      return "".join(ch for ch in text if ch not in exclude)

  def lower(text):
      return text.lower()

  return white_space_fix(remove_articles(remove_punc(lower(s))))

def EM(answer, key) -> bool:
    return normalize_answer(str(answer)) == normalize_answer(str(key))
