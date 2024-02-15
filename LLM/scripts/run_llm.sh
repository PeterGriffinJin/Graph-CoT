export TRANSFORMERS_CACHE=/shared/data/bowenj4/hf-cache

MODEL_NAME=meta-llama/Llama-2-13b-chat-hf
# MODEL_NAME=mistralai/Mixtral-8x7B-Instruct-v0.1

arrIN=(${MODEL_NAME//// })
SIMPLE_MODEL_NAME=${arrIN[1]}

DATASET=amazon # legal, biomedical, amazon, goodreads, dblp
DATA_FILE=/shared/data3/bowenj4/llm-graph-plugin/data/processed_data/$DATASET/data.json
SAVE_FILE=/shared/data3/bowenj4/llm-graph-plugin/LLM/results/$SIMPLE_MODEL_NAME/$DATASET/results.jsonl

DOMAIN=Biology # Biology Chemistry Materials_Science Medicine Physics
DATA_FILE=/shared/data3/bowenj4/llm-graph-plugin/data/processed_data/maple/$DOMAIN/data.json
SAVE_FILE=/shared/data3/bowenj4/llm-graph-plugin/LLM/results/$SIMPLE_MODEL_NAME/maple-$DOMAIN/results.jsonl

CUDA_VISIBLE_DEVICES=0,2,3,6 python ../code/run_llm.py --data_file $DATA_FILE \
                        --save_file $SAVE_FILE \
                        --version $MODEL_NAME
