# -*- coding: utf-8 -*-
"""
Created on Mon May 10 10:41:51 2021
An example script for using the Gephi module
@author: David
"""
import os
import gephi as gp
import pandas as pd

# where all keyword exports are located
folder = "scopus exports/"
fnames = [folder+f for f in os.listdir(folder)]

# the true amounts for keywords with more publications than the
# maximum limit of 20,000 for downloading
ams_fname = "True Amounts.xlsx"
known_ams = pd.read_excel(ams_fname,
                          header=None, index_col=0, squeeze=True)

# calculate
# int_sim=True to calculate internal similarity
# set False for faster performance
nodes = gp.get_nodes(fnames, limited_node_sizes=known_ams, 
                     includes_internal_similarity=True)
edges = gp.get_edges(fnames, limited_node_sizes=known_ams)

# export
nodes.to_excel("out/nodes.xlsx")
edges.to_excel("out/edges.xlsx")