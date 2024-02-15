
## GPT3.5-turbo / GPT-4
Remember to change ``DATASET`` to your domain name.

### Direct Inference
```
cd scripts
bash run_GPT.sh
```

### Text RAG Inference
Remember to change ``hop`` to 0.

``max_len`` is to set up the max len input for the LLM.
``graph_max_len`` is to truncate the retrieved context and to guarantee that the input to LLM does not reach its max_len.
We can adjust ``graph_max_len`` if there are any warnings that the total sequence length is over the LLM max len.

```
cd scripts
bash run_GPT_rag.sh
```

### Graph RAG Inference
Remember to change ``hop`` to 1.

``max_len`` is to set up the max len input for the LLM.
``graph_max_len`` is to truncate the retrieved context and to guarantee that the input to LLM does not reach its max_len.
We can adjust ``graph_max_len`` if there are any warnings that the total sequence length is over the LLM max len.

```
cd scripts
bash run_GPT_rag.sh
```
