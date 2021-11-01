# -*- coding: utf-8 -*-
"""
Created on Mon May 10 10:41:51 2021
An example script for using the Gephi module, using Scopus
@author: David
"""

import gephi as gp
import pandas as pd

nodes = pd.read_excel("nodes_to_analyze/Nodes_clustered.xlsx", index_col=0)
edges = pd.read_excel("nodes_to_analyze/edges.xlsx", index_col=0)

clusters = gp.get_cluster_info(nodes, edges)
clusters.to_excel("out/Clusters.xlsx")

nodes_out = gp.get_cluster_info_nodes(nodes, edges)
nodes_out.to_excel("out/Nodes_with_cluster_info.xlsx")