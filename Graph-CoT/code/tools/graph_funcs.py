import networkx as nx
import numpy as np
import pandas as pd
import pickle
import os

from IPython import embed

class graph_funcs():
    # init
    def __init__(self, graph):
        self._reset(graph)

    def _reset(self, graph):
        graph_index = {}
        nid_set = set()
        for node_type in graph:
            for nid in graph[node_type]:
                assert nid not in nid_set
                nid_set.add(nid)
                graph_index[nid] = graph[node_type][nid]
        self.graph_index = graph_index

    def check_neighbours(self, node, neighbor_type=None):
        if neighbor_type:
            return str(self.graph_index[node]['neighbors'][neighbor_type])
        else:
            return str(self.graph_index[node]['neighbors'])

    # check the attributes of the nodes
    def check_nodes(self, node, feature=None):
        if feature:
            return str(self.graph_index[node]['features'][feature])
        else:
            return str(self.graph_index[node]['features'])

    def check_degree(self, node, neighbor_type):
        return str(len(self.graph_index[node]['neighbors'][neighbor_type]))
