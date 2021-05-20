Package for creating Gephi nodes and edges .csv/.xlsx files from scientific publication/patent data.

----------------
----------------
BACKGROUND
Gephi can create force-directed graphs of nodes and edges. When using keywords, scientific journals or patent categories, this can be used to distill clusters of keywords that define an area of research/R&D. 

Clusters can be identified by eye, or with the use of the Leiden algorithm available in Gephi.

See the example/ folder for an example of such a graph.

----------------
----------------
USAGE
Main function is get_nodes_edges(), or the separate versions get_nodes(), get_edges()

import os
import pandas as pd
import gephi as gph

folder = "scopus exports"
fnames = os.listdir(folder)
real_ams = pd.read_excel("real_ams.xlsx", squeeze=True, header=False, index_col=0) # real_ams.xlsx has first row filename (without folder), second row amounts

nodes = gph.get_nodes(fnames, fold=folder, real_ams=real_ams)
edges = gph.get_edges(fnames, fold=folder, real_ams=real_ams)

nodes.to_excel("nodes.xlsx")
edges.to_excel("edges.xlsx")

There is also the option to calculate the internal similarity within a node, though this will take a bit longer. Use:
nodes = get_nodes(fnames, fold=folder, int_sim=True)

