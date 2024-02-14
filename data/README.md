### Raw data
Download raw data with wget
```
cd data/raw_data/{data_name}
wget web_data_dir
```

### Processing data
```
cd data/raw_data/{data_name}
```
Run the cells in raw_process.ipynb

The script will process the raw data and save it as a graph.pkl file.
```
graph.pkl:{
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
graph.pkl:{
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
Write question templates
```
cd data/processed_data/{data_name}
design_questions.ipynb
```

Enrich the question expression with GPT
```
cd ..
generate_sample.ipynb
```
