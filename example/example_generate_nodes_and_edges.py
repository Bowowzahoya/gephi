# -*- coding: utf-8 -*-
"""
Created on Mon May 10 10:41:51 2021
An example script for using the Gephi module, using Scopus
@author: David
"""
import os
import gephi as gp
import pandas as pd

# where all keyword exports are located
folder = "scopus exports/"
fnames = [folder+f for f in os.listdir(folder)]

# the true amounts for keywords with more publications than the
# maximum limit of 20,000 (Scopus) / 50,000 (Lens) for downloading
limited_node_sizes_fname = "True Amounts.xlsx"
limited_node_sizes = pd.read_excel(limited_node_sizes_fname,
                                   header=None, index_col=0, squeeze=True)

# calculate nodes
# includes_internal_similarity=True to calculate internal similarity
# set False for faster performance
# if using Lens exports (patents or scholarly both work) instead of 
# Scopus, set database="lens"
nodes = gp.get_nodes(fnames, limited_node_sizes=limited_node_sizes, 
                     includes_internal_similarity=True)
nodes.to_excel("out/nodes.xlsx")

# calculate edges
# if using Lens exports (patents or scholarly both work) instead of 
# Scopus, set database="lens"
edges = gp.get_edges(fnames, limited_node_sizes=limited_node_sizes)
edges.to_excel("out/edges.xlsx")