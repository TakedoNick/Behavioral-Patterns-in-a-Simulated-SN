# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 07:41:09 2017

@author: Nick
"""


import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from community import community_louvain


def generate_random_connection_matrix(density=0.1, shape=10, loc=1, scale=2):
    res = np.zeros(shape=(shape, shape), dtype=int)
    for i in range(res.shape[0]):
        for j in range(i+1, res.shape[1]):
            if density > np.random.rand():
                weight = abs(int(np.round(np.random.normal(loc, scale))))
                res[i, j] = weight
                res[j, i] = weight
    return res


def get_node_colors(graph, partition):
    if not isinstance(partition, dict):
        raise Exception
    if not isinstance(graph, nx.Graph):
        raise Exception
    res = []
    for n in graph.nodes_iter():
        comm_n = partition[n]
        res.append(comm_n)
    return res


def infer_connections(cm, partition):
    if not isinstance(partition, dict):
        raise Exception
    for com in set(partition.values()):
        nodes_in_com = [n for n in partition.keys() if partition[n] == com]
        com_cm = cm[nodes_in_com, :][:, nodes_in_com]
        com_conns = com_cm[np.triu_indices_from(com_cm, k=1)]
        com_median_conn = np.median(com_conns[com_conns > 0])
        for i in nodes_in_com:
            for j in nodes_in_com:
                if i < j:
                    if cm[i, j] == 0:
                        cm[i, j] = com_median_conn
                        cm[j, i] = com_median_conn
    return cm


def plot_graph(graph, partition=None):
    if partition is not None:
        node_colors = get_node_colors(graph, partition)
    else:
        node_colors = None
    pos = nx.shell_layout(graph)
    nx.draw_networkx_nodes(graph, pos, node_color=node_colors)
    nx.draw_networkx_edges(graph, pos)
    nx.draw_networkx_edge_labels(graph, pos,
                                 edge_labels=nx.get_edge_attributes(graph, "weight"),
                                 font_size=10)
    nx.draw_networkx_labels(graph, pos)


def main():
    density = 0.15
    shape = 10
    loc = 1
    scale = 2
    rcm = generate_random_connection_matrix(density, shape, loc, scale)

    graph = nx.from_numpy_matrix(rcm)
    partition = community_louvain.best_partition(graph)

    plt.figure()
    plt.subplot(2, 1, 1)
    plot_graph(graph, partition)

    rcm_add = infer_connections(rcm, partition)
    graph_add = nx.from_numpy_matrix(rcm_add)

    plt.subplot(2, 1, 2)
    plot_graph(graph_add, partition)
    plt.show()


if __name__ == '__main__':
    main()