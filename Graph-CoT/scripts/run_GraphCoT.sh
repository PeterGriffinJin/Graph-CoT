OPENAI_KEY=xxx
GPT_version=gpt-3.5-turbo-16k
max_steps=10

DATASET=dblp # legal, biomedical, amazon, goodreads, dblp
DATA_PATH=/shared/data3/bowenj4/llm-graph-plugin/data/processed_data/$DATASET
SAVE_FILE=/shared/data3/bowenj4/llm-graph-plugin/Graph-CoT/results/$GPT_version/$DATASET/results.jsonl

DATASET=maple
SUBDATASET=Chemistry # Biology, Chemistry, Materials_Science, Medicine, Physics
DATA_PATH=/shared/data3/bowenj4/llm-graph-plugin/data/processed_data/maple/$SUBDATASET
SAVE_FILE=/shared/data3/bowenj4/llm-graph-plugin/Graph-CoT/results/$GPT_version/maple-$SUBDATASET/results.jsonl

CUDA_VISIBLE_DEVICES=2,3 python ../code/run.py --dataset $DATASET \
                    --path $DATA_PATH \
                    --save_file $SAVE_FILE \
                    --llm_version $GPT_version \
                    --openai_api_key $OPENAI_KEY \
                    --max_steps $max_steps
