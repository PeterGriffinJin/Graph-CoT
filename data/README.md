## Use GRBench directly
You can directly download the graph environement files [here](https://drive.google.com/drive/folders/1DJIgRZ3G-TOf7h0-Xub5_sE4slBUEqy9?usp=share_link) and save them to `data/processed_data/{data_name}`.

You can access the question answering dataset for each domain [here](https://huggingface.co/datasets/PeterJinGo/GRBench). They can also be found in `data/processed_data/{data_name}/data.json`.

If you are interested in how GRBench is constructed from raw data, you can read the following instructions.

## (Optional) The construction process of GRBench
### Raw data
Download raw data with wget. ``web_data_dir`` for each dataset can be found [here](https://github.com/PeterGriffinJin/Graph-CoT/tree/main/data/raw_data).
```
cd data/raw_data/{data_name}
wget web_data_dir
```

### Processing data
```
cd data/raw_data/{data_name}
```
Run the cells in raw_process.ipynb

The script will process the raw data and save it as a graph.json file.
```
graph.json:{
    type1_nodes (Dict),
    type2_nodes (Dict),
    ...
}
type1_nodes:{
    features (Dict, key: feature_name (str), value: feature_value (str, Dict)),
    neighbors (Dict, key: neighbor_type (str), value: neighbor_ids (list, Dict))
}
```
E.g., for the DBLP academic graph:
```
graph.json:{
    paper_nodes (Dict),
    author_nodes (Dict),
    venue_nodes (Dict),
}
paper_nodes:{
    features: {title: xxx, abstract: xxx, keywords: xxx, lang: xxx, year: xxx},
    neighbors: {author: [xxx, ...], venue: [xxx], reference: [xxx, ...], cited_by: [xxx, ...]}
}
author_nodes:{
    features: {name: xxx, org: xxx},
    neighbors: {paper: [xxx, ...]}
}
venue_nodes:{
    features: {name: xxx},
    neighbors: {paper: [xxx, ...]}
}
```

### Design question answering pairs for each dataset
Manually designed question templates and automatic answer generation.
```
cd data/processed_data/{data_name}
design_questions.ipynb
```

Diversify the question expressions with GPT4.
```
cd ..
generate_sample.ipynb
```
