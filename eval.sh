openai_key=xxx

## LLM
# MODEL_NAME=meta-llama/Llama-2-13b-chat-hf # mistralai/Mixtral-8x7B-Instruct-v0.1
for MODEL_NAME in meta-llama/Llama-2-13b-chat-hf mistralai/Mixtral-8x7B-Instruct-v0.1
do
    arrIN=(${MODEL_NAME//// })
    SIMPLE_MODEL_NAME=${arrIN[1]}

    DATASET=dblp
    RESULT_FILE=/shared/data3/bowenj4/llm-graph-plugin/LLM/results/$SIMPLE_MODEL_NAME/$DATASET/results.jsonl
    # DOMAIN=Biology
    # RESULT_FILE=/shared/data3/bowenj4/llm-graph-plugin/LLM/results/$SIMPLE_MODEL_NAME/maple-$DOMAIN/results.jsonl
    python eval.py --result_file $RESULT_FILE --model $SIMPLE_MODEL_NAME --openai_key $openai_key
done

# ## LLM RAG
# MODEL_NAME=meta-llama/Llama-2-13b-chat-hf # mistralai/Mixtral-8x7B-Instruct-v0.1
for MODEL_NAME in meta-llama/Llama-2-13b-chat-hf mistralai/Mixtral-8x7B-Instruct-v0.1
do
    arrIN=(${MODEL_NAME//// })
    SIMPLE_MODEL_NAME=${arrIN[1]}

    DATASET=dblp
    RESULT_FILE=/shared/data3/bowenj4/llm-graph-plugin/LLM/rag-results/$SIMPLE_MODEL_NAME/$DATASET/results_0.jsonl
    # DOMAIN=Biology
    # RESULT_FILE=/shared/data3/bowenj4/llm-graph-plugin/LLM/rag-results/$SIMPLE_MODEL_NAME/maple-$DOMAIN/results_0.jsonl
    python eval.py --result_file $RESULT_FILE --model $SIMPLE_MODEL_NAME-RAG-hop0 --openai_key $openai_key

    RESULT_FILE=/shared/data3/bowenj4/llm-graph-plugin/LLM/rag-results/$SIMPLE_MODEL_NAME/$DATASET/results_1.jsonl
    # RESULT_FILE=/shared/data3/bowenj4/llm-graph-plugin/LLM/rag-results/$SIMPLE_MODEL_NAME/maple-$DOMAIN/results_1.jsonl
    python eval.py --result_file $RESULT_FILE --model $SIMPLE_MODEL_NAME-RAG-hop1 --openai_key $openai_key

    RESULT_FILE=/shared/data3/bowenj4/llm-graph-plugin/LLM/rag-results/$SIMPLE_MODEL_NAME/$DATASET/results_2.jsonl
    # RESULT_FILE=/shared/data3/bowenj4/llm-graph-plugin/LLM/rag-results/$SIMPLE_MODEL_NAME/maple-$DOMAIN/results_2.jsonl
    python eval.py --result_file $RESULT_FILE --model $SIMPLE_MODEL_NAME-RAG-hop2 --openai_key $openai_key
done

## GPT
gpt_version=gpt-3.5-turbo
DATASET=dblp
RESULT_FILE=/shared/data3/bowenj4/llm-graph-plugin/GPT/results/$gpt_version/$DATASET/results.jsonl
# DOMAIN=Biology
# RESULT_FILE=/shared/data3/bowenj4/llm-graph-plugin/GPT/results/$gpt_version/maple-$DOMAIN/results.jsonl
python eval.py --result_file $RESULT_FILE --model $gpt_version --openai_key $openai_key


# GPT RAG
gpt_version=gpt-3.5-turbo-16k
DATASET=dblp
RESULT_FILE=/shared/data3/bowenj4/llm-graph-plugin/GPT/rag-results/$gpt_version/$DATASET/results_0.jsonl
# DOMAIN=Biology
# RESULT_FILE=/shared/data3/bowenj4/llm-graph-plugin/GPT/rag-results/$gpt_version/maple-$DOMAIN/results_0.jsonl
python eval.py --result_file $RESULT_FILE --model $gpt_version-RAG-hop0 --openai_key $openai_key

RESULT_FILE=/shared/data3/bowenj4/llm-graph-plugin/GPT/rag-results/$gpt_version/$DATASET/results_1.jsonl
# RESULT_FILE=/shared/data3/bowenj4/llm-graph-plugin/GPT/rag-results/$gpt_version/maple-$DOMAIN/results_1.jsonl
python eval.py --result_file $RESULT_FILE --model $gpt_version-RAG-hop1 --openai_key $openai_key

RESULT_FILE=/shared/data3/bowenj4/llm-graph-plugin/GPT/rag-results/$gpt_version/$DATASET/results_2.jsonl
# RESULT_FILE=/shared/data3/bowenj4/llm-graph-plugin/GPT/rag-results/$gpt_version/maple-$DOMAIN/results_2.jsonl
python eval.py --result_file $RESULT_FILE --model $gpt_version-RAG-hop2 --openai_key $openai_key


## Graph CoT
gpt_version=gpt-3.5-turbo-16k
DATASET=dblp
RESULT_FILE=/shared/data3/bowenj4/llm-graph-plugin/Graph-CoT/results/$gpt_version/$DATASET/results.jsonl
# DOMAIN=Physics
# RESULT_FILE=/shared/data3/bowenj4/llm-graph-plugin/Graph-CoT/results/$gpt_version/maple-$DOMAIN/results.jsonl
python eval.py --result_file $RESULT_FILE --model Graph-CoT-$gpt_version --openai_key $openai_key
