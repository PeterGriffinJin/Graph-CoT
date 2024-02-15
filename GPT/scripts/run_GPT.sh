OPENAI_KEY=xxx
gpt_version=gpt-3.5-turbo

DATASET=amazon # legal, biomedical, amazon, goodreads, dblp
DATA_FILE=/shared/data3/bowenj4/llm-graph-plugin/data/processed_data/$DATASET/data.json
SAVE_FILE=/shared/data3/bowenj4/llm-graph-plugin/GPT/results/$gpt_version/$DATASET/results.jsonl

DATASET=maple
DOMAIN=Biology # Biology, Chemistry, Materials_Science, Medicine, Physics
DATA_FILE=/shared/data3/bowenj4/llm-graph-plugin/data/processed_data/maple/$DOMAIN/data.json
SAVE_FILE=/shared/data3/bowenj4/llm-graph-plugin/GPT/results/$gpt_version/maple-$DOMAIN/results.jsonl

python ../code/run_GPT.py --dataset $DATASET \
                        --gpt_version $gpt_version \
                        --data_file $DATA_FILE \
                        --save_file $SAVE_FILE \
                        --openai_key $OPENAI_KEY
