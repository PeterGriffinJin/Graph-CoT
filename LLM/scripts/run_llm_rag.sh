export TRANSFORMERS_CACHE=/shared/data/bowenj4/hf-cache

MODEL_NAME=meta-llama/Llama-2-13b-chat-hf
# MODEL_NAME=mistralai/Mixtral-8x7B-Instruct-v0.1

arrIN=(${MODEL_NAME//// })
SIMPLE_MODEL_NAME=${arrIN[1]}

hop=0 # 0,1,2
max_len=4096 # 
graph_max_len=3600

DATASET=legal # legal, biomedical, amazon, goodreads, dblp
DATA_PATH=/shared/data3/bowenj4/llm-graph-plugin/data/processed_data/$DATASET
SAVE_FILE=/shared/data3/bowenj4/llm-graph-plugin/LLM/rag-results/$SIMPLE_MODEL_NAME/$DATASET/results_$hop.jsonl

DATASET=maple
DOMAIN=Biology # Biology, Chemistry, Materials_Science, Medicine, Physics
DATA_PATH=/shared/data3/bowenj4/llm-graph-plugin/data/processed_data/maple/$DOMAIN
SAVE_FILE=/shared/data3/bowenj4/llm-graph-plugin/LLM/rag-results/$SIMPLE_MODEL_NAME/maple-$DOMAIN/results_$hop.jsonl

CUDA_VISIBLE_DEVICES=1,2,3,5 python ../code/run_llm_rag.py --dataset $DATASET \
                        --path $DATA_PATH \
                        --save_file $SAVE_FILE \
                        --version $MODEL_NAME \
                        --max_len $max_len \
                        --retrieve_graph_hop $hop \
                        --graph_max_len $graph_max_len
