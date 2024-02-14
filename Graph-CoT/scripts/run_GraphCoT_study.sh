
# ## zero-shot study

# OPENAI_KEY=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
# GPT_version=gpt-3.5-turbo-16k
# max_steps=10
# zero_shot=True

# for DATASET in legal biomedical amazon goodreads # legal, biomedical, amazon, goodreads, dblp
# do
# DATA_PATH=/shared/data3/bowenj4/llm-graph-plugin/data/processed_data/$DATASET
# SAVE_FILE=/shared/data3/bowenj4/llm-graph-plugin/Graph-CoT/results/$GPT_version/$DATASET/zero_shot/results.jsonl

# CUDA_VISIBLE_DEVICES=2 python ../code/run.py --dataset $DATASET \
#                     --path $DATA_PATH \
#                     --save_file $SAVE_FILE \
#                     --llm_version $GPT_version \
#                     --openai_api_key $OPENAI_KEY \
#                     --max_steps $max_steps \
#                     --zero_shot $zero_shot
# done

# DATASET=maple
# for SUBDATASET in Biology Chemistry Materials_Science Medicine Physics
# do
# DATA_PATH=/shared/data3/bowenj4/llm-graph-plugin/data/processed_data/maple/$SUBDATASET
# SAVE_FILE=/shared/data3/bowenj4/llm-graph-plugin/Graph-CoT/results/$GPT_version/maple-$SUBDATASET/zero_shot/results.jsonl

# CUDA_VISIBLE_DEVICES=2 python ../code/run.py --dataset $DATASET \
#                     --path $DATA_PATH \
#                     --save_file $SAVE_FILE \
#                     --llm_version $GPT_version \
#                     --openai_api_key $OPENAI_KEY \
#                     --max_steps $max_steps \
#                     --zero_shot $zero_shot
# done


# ## Base LLM for Graph CoT study

# ### gpt-4
# OPENAI_KEY=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
# GPT_version=gpt-4
# max_steps=10

# for DATASET in legal # dblp biomedical amazon goodreads legal
# do
# DATA_PATH=/shared/data3/bowenj4/llm-graph-plugin/data/processed_data/$DATASET
# SAVE_FILE=/shared/data3/bowenj4/llm-graph-plugin/Graph-CoT/results/$GPT_version/$DATASET/results.jsonl

# CUDA_VISIBLE_DEVICES=2,3 python ../code/run.py --dataset $DATASET \
#                     --path $DATA_PATH \
#                     --save_file $SAVE_FILE \
#                     --llm_version $GPT_version \
#                     --openai_api_key $OPENAI_KEY \
#                     --max_steps $max_steps
# done

# DATASET=maple
# for SUBDATASET in Biology Chemistry Materials_Science Medicine Physics
# do
# DATA_PATH=/shared/data3/bowenj4/llm-graph-plugin/data/processed_data/maple/$SUBDATASET
# SAVE_FILE=/shared/data3/bowenj4/llm-graph-plugin/Graph-CoT/results/$GPT_version/maple-$SUBDATASET/results.jsonl

# CUDA_VISIBLE_DEVICES=2,3 python ../code/run.py --dataset $DATASET \
#                     --path $DATA_PATH \
#                     --save_file $SAVE_FILE \
#                     --llm_version $GPT_version \
#                     --openai_api_key $OPENAI_KEY \
#                     --max_steps $max_steps
# done


### open LLM

export TRANSFORMERS_CACHE=/shared/data/bowenj4/hf-cache

for MODEL_NAME in mistralai/Mixtral-8x7B-Instruct-v0.1 # meta-llama/Llama-2-13b-chat-hf     mistralai/Mixtral-8x7B-Instruct-v0.1
do
    max_steps=10

    arrIN=(${MODEL_NAME//// })
    SIMPLE_MODEL_NAME=${arrIN[1]}

    for DATASET in dblp biomedical amazon goodreads legal # dblp biomedical amazon goodreads legal
    do
    DATA_PATH=/shared/data3/bowenj4/llm-graph-plugin/data/processed_data/$DATASET
    SAVE_FILE=/shared/data3/bowenj4/llm-graph-plugin/Graph-CoT/results/$SIMPLE_MODEL_NAME/$DATASET/results.jsonl

    CUDA_VISIBLE_DEVICES=0,1,2,4 python ../code/run.py --dataset $DATASET \
                        --path $DATA_PATH \
                        --save_file $SAVE_FILE \
                        --llm_version $MODEL_NAME \
                        --max_steps $max_steps
    done

    # DATASET=maple
    # for SUBDATASET in Biology Chemistry Materials_Science Medicine Physics
    # do
    # DATA_PATH=/shared/data3/bowenj4/llm-graph-plugin/data/processed_data/maple/$SUBDATASET
    # SAVE_FILE=/shared/data3/bowenj4/llm-graph-plugin/Graph-CoT/results/$SIMPLE_MODEL_NAME/maple-$SUBDATASET/results.jsonl

    # CUDA_VISIBLE_DEVICES=0,1,2,4 python ../code/run.py --dataset $DATASET \
    #                     --path $DATA_PATH \
    #                     --save_file $SAVE_FILE \
    #                     --llm_version $MODEL_NAME \
    #                     --max_steps $max_steps
    # done
done


# ## cross domain study

# OPENAI_KEY=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
# GPT_version=gpt-3.5-turbo-16k
# max_steps=10


# DATASET=dblp
# for REF_DATASET in biomedical amazon goodreads legal
# do
# DATA_PATH=/shared/data3/bowenj4/llm-graph-plugin/data/processed_data/$DATASET
# SAVE_FILE=/shared/data3/bowenj4/llm-graph-plugin/Graph-CoT/results/$GPT_version/cross-domain/$DATASET-$REF_DATASET/results.jsonl

# CUDA_VISIBLE_DEVICES=2,3 python ../code/run.py --dataset $DATASET \
#                         --path $DATA_PATH \
#                         --save_file $SAVE_FILE \
#                         --llm_version $GPT_version \
#                         --openai_api_key $OPENAI_KEY \
#                         --max_steps $max_steps \
#                         --ref_dataset $REF_DATASET
# done


# DATASET=biomedical
# for REF_DATASET in dblp amazon goodreads legal
# do
# DATA_PATH=/shared/data3/bowenj4/llm-graph-plugin/data/processed_data/$DATASET
# SAVE_FILE=/shared/data3/bowenj4/llm-graph-plugin/Graph-CoT/results/$GPT_version/cross-domain/$DATASET-$REF_DATASET/results.jsonl

# CUDA_VISIBLE_DEVICES=2,3 python ../code/run.py --dataset $DATASET \
#                         --path $DATA_PATH \
#                         --save_file $SAVE_FILE \
#                         --llm_version $GPT_version \
#                         --openai_api_key $OPENAI_KEY \
#                         --max_steps $max_steps \
#                         --ref_dataset $REF_DATASET
# done


# DATASET=amazon
# for REF_DATASET in dblp biomedical goodreads legal
# do
# DATA_PATH=/shared/data3/bowenj4/llm-graph-plugin/data/processed_data/$DATASET
# SAVE_FILE=/shared/data3/bowenj4/llm-graph-plugin/Graph-CoT/results/$GPT_version/cross-domain/$DATASET-$REF_DATASET/results.jsonl

# CUDA_VISIBLE_DEVICES=2,3 python ../code/run.py --dataset $DATASET \
#                         --path $DATA_PATH \
#                         --save_file $SAVE_FILE \
#                         --llm_version $GPT_version \
#                         --openai_api_key $OPENAI_KEY \
#                         --max_steps $max_steps \
#                         --ref_dataset $REF_DATASET
# done


# DATASET=goodreads
# for REF_DATASET in dblp biomedical amazon legal
# do
# DATA_PATH=/shared/data3/bowenj4/llm-graph-plugin/data/processed_data/$DATASET
# SAVE_FILE=/shared/data3/bowenj4/llm-graph-plugin/Graph-CoT/results/$GPT_version/cross-domain/$DATASET-$REF_DATASET/results.jsonl

# CUDA_VISIBLE_DEVICES=2,3 python ../code/run.py --dataset $DATASET \
#                         --path $DATA_PATH \
#                         --save_file $SAVE_FILE \
#                         --llm_version $GPT_version \
#                         --openai_api_key $OPENAI_KEY \
#                         --max_steps $max_steps \
#                         --ref_dataset $REF_DATASET
# done


# DATASET=legal
# for REF_DATASET in dblp biomedical amazon goodreads
# do
# DATA_PATH=/shared/data3/bowenj4/llm-graph-plugin/data/processed_data/$DATASET
# SAVE_FILE=/shared/data3/bowenj4/llm-graph-plugin/Graph-CoT/results/$GPT_version/cross-domain/$DATASET-$REF_DATASET/results.jsonl

# CUDA_VISIBLE_DEVICES=2,3 python ../code/run.py --dataset $DATASET \
#                         --path $DATA_PATH \
#                         --save_file $SAVE_FILE \
#                         --llm_version $GPT_version \
#                         --openai_api_key $OPENAI_KEY \
#                         --max_steps $max_steps \
#                         --ref_dataset $REF_DATASET
# done
