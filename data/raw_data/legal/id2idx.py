import os
import json
from tqdm import tqdm

from IPython import embed

data_dir=f"/home/ec2-user/quic-efs/user/bowenjin/llm-graph-plugin/data/processed_data/legal"
graph = json.load(open(os.path.join(data_dir, 'graph_raw.json')))

# filter features
feature_dict = {"opinion": ["plain_text"],
                "opinion_cluster": ["syllabus", "judges", "case_name", "attorneys"],
                "court": ["full_name", "start_date", "end_date", "citation_string"],
                "docket": ["pacer_case_id", "case_name"]}

opinion_nodes = {}
opinion_cluster_nodes = {}
docket_nodes = {}
court_nodes = {}

# opinion
for idd in tqdm(graph['opinion_nodes']):
    tmp = graph['opinion_nodes'][idd]
    for i in range(len(tmp['neighbors']['opinion_cluster'])):
        tmp['neighbors']['opinion_cluster'][i] = 'opc-' + tmp['neighbors']['opinion_cluster'][i]

    for depth in tmp['neighbors']['reference']:
        for i in range(len(tmp['neighbors']['reference'][depth])):
            tmp['neighbors']['reference'][depth][i] = 'op-' + tmp['neighbors']['reference'][depth][i]
    tmp['neighbors']['reference'] = sum([tmp['neighbors']['reference'][depth] for depth in tmp['neighbors']['reference']], [])

    for depth in tmp['neighbors']['cited_by']:
        for i in range(len(tmp['neighbors']['cited_by'][depth])):
            tmp['neighbors']['cited_by'][depth][i] = 'op-' + tmp['neighbors']['cited_by'][depth][i]
    tmp['neighbors']['cited_by'] = sum([tmp['neighbors']['cited_by'][depth] for depth in tmp['neighbors']['cited_by']], [])

    tmp['features'] = {k: v for k, v in tmp['features'].items() if k in feature_dict["opinion"]}

    opinion_nodes['op-'+idd] = tmp

# opinion cluster
for idd in tqdm(graph['opinion_cluster_nodes']):
    tmp = graph['opinion_cluster_nodes'][idd]
    for i in range(len(tmp['neighbors']['opinion'])):
        tmp['neighbors']['opinion'][i] = 'op-' + tmp['neighbors']['opinion'][i]
    for i in range(len(tmp['neighbors']['docket'])):
        tmp['neighbors']['docket'][i] = 'd-' + tmp['neighbors']['docket'][i]
    
    tmp['features'] = {k: v for k, v in tmp['features'].items() if k in feature_dict["opinion_cluster"]}
    
    opinion_cluster_nodes['opc-'+idd] = tmp

# docket
for idd in tqdm(graph['docket_nodes']):
    tmp = graph['docket_nodes'][idd]
    for i in range(len(tmp['neighbors']['opinion_cluster'])):
        tmp['neighbors']['opinion_cluster'][i] = 'opc-' + tmp['neighbors']['opinion_cluster'][i]
    
    tmp['features'] = {k: v for k, v in tmp['features'].items() if k in feature_dict["docket"]}
    
    docket_nodes['d-'+idd] = tmp

# court
for idd in tqdm(graph['court_nodes']):
    tmp = graph['court_nodes'][idd]
    tmp['features'] = {k: v for k, v in tmp['features'].items() if k in feature_dict["court"]}

    court_nodes[idd] = tmp

json.dump({
    'opinion_nodes': opinion_nodes,
    'opinion_cluster_nodes': opinion_cluster_nodes,
    'docket_nodes': docket_nodes,
    'court_nodes': court_nodes
}, open(os.path.join(data_dir, 'graph.json'),"w"), indent = 4)
