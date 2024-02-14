OPENAI_KEY=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
gpt_version=gpt-3.5-turbo-16k

for hop in 0 1 2
do
max_len=2500 # 2300, 
graph_max_len=2300 # 2100

# DATASET=amazon
# DATA_PATH=/shared/data3/bowenj4/llm-graph-plugin/data/processed_data/$DATASET
# SAVE_FILE=/shared/data3/bowenj4/llm-graph-plugin/GPT/rag-results/$gpt_version/$DATASET/results_$hop.jsonl

# CUDA_VISIBLE_DEVICES=3 python ../code/run_GPT_rag.py --dataset $DATASET \
#                             --path $DATA_PATH \
#                             --save_file $SAVE_FILE \
#                             --gpt_version $gpt_version \
#                             --openai_key $OPENAI_KEY \
#                             --max_len $max_len \
#                             --retrieve_graph_hop $hop \
#                             --graph_max_len $graph_max_len

DATASET=maple
# DOMAIN=Biology
    for DOMAIN in Biology Chemistry Materials_Science Medicine Physics
    do
    DATA_PATH=/shared/data3/bowenj4/llm-graph-plugin/data/processed_data/maple/$DOMAIN
    SAVE_FILE=/shared/data3/bowenj4/llm-graph-plugin/GPT/rag-results/$gpt_version/maple-$DOMAIN/results_$hop.jsonl

    CUDA_VISIBLE_DEVICES=3 python ../code/run_GPT_rag.py --dataset $DATASET \
                            --path $DATA_PATH \
                            --save_file $SAVE_FILE \
                            --gpt_version $gpt_version \
                            --openai_key $OPENAI_KEY \
                            --max_len $max_len \
                            --retrieve_graph_hop $hop \
                            --graph_max_len $graph_max_len
    done
done
