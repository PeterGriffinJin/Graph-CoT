
## Open-source LLMs
Remember to change ``TRANSFORMERS_CACHE`` to your hf cache dir, change ``MODEL_NAME`` to the target model (here we will only test llama-13b and mixtral 8*7b), change ``DATASET`` to your domain name.

### Direct Inference
```
cd scripts
bash run_llm.sh
```

### Text RAG Inference
Remember to change ``hop`` to 0.

``max_len`` is to set up the max len input for the LLM.
``graph_max_len`` is to truncate the retrieved context and to guarantee that the input to LLM does not reach its max_len.
We can adjust ``graph_max_len`` if there are any warnings that the total sequence length is over the LLM max len.

```
cd scripts
bash run_llm_rag.sh
```

### Graph RAG Inference
Remember to change ``hop`` to 1.

``max_len`` is to set up the max len input for the LLM.
``graph_max_len`` is to truncate the retrieved context and to guarantee that the input to LLM does not reach its max_len.
We can adjust ``graph_max_len`` if there are any warnings that the total sequence length is over the LLM max len.

```
cd scripts
bash run_llm_rag.sh
```

### Some comments referring ``./code/retriever.py``
``NODE_TEXT_KEYS``: A dictionary to point out what text feature for each node types is used for infering its embedding in preparation for *semantic search*.

``RELATION_NODE_TYPE_MAP``: A dictionary to point out what type of neighbor nodes (value) is connected to the center node with the edge type (key).

``FEATURE_NODE_TYPE``: A dictionary to point out what feature for each node types is used for graph linearization when doing the retrieval.
