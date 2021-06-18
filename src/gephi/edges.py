# -*- coding: utf-8 -*-
"""
Data source agnostic function get_edges() for creating
edges
"""
import pandas as pd

from .database_specific import scopus as sc
from .database_specific import lens_patent as lp
from .constants import ID_COL, SOURCE_COL, TARGET_COL, WEIGHT_COL
from .nodes import get_node_label

def get_edges(filenames, database="scopus", **kwargs):
    edges = _get_empty_edges_dataframe()
    edge_getter = EdgeGetter(database)
        
    for filename1 in filenames:
        print(f"Reading edges for '{filename1}'")
        for filename2 in filenames:
            if filename1==filename2:
                continue
            print(f"\twith '{filename2}'...")
            new_edge = edge_getter.get_edge(filename1, filename2, **kwargs)
            edges = edges.append(new_edge, ignore_index=True)
    return edges

def _get_empty_edges_dataframe():
    columns = [SOURCE_COL, TARGET_COL, WEIGHT_COL]
    edges = pd.DataFrame(columns=columns)
    edges.index.name = ID_COL
    return edges

class EdgeGetter():
    def __init__(self, database, **kwargs):
        self.get_edge_weight = _get_get_function(database, **kwargs)
        
    def get_edge(self, filename1, filename2, **kwargs):
        edge = {}
                
        label1 = get_node_label(filename1)
        label2 = get_node_label(filename2)
        edge[SOURCE_COL] = label1
        edge[TARGET_COL] = label2

        print(f"\t  Determining weight for '{filename1}' and '{filename2}'...")
        weight = self.get_edge_weight(filename1, filename2)
        print(f"\t  {weight}")
        edge[WEIGHT_COL] = weight
    
        return edge
    
def _get_get_function(database, **kwargs):
    if database == "scopus":
        edge_getter = sc.EdgeGetter(**kwargs)
        get_edge_weight = edge_getter.get_edge_weight
    elif database == "lens":
        edge_getter = lp.EdgeGetter(**kwargs)
        get_edge_weight = edge_getter.get_edge_weight
    else:
        raise NotImplementedError(f"Database {database} not valid.")
        
    return get_edge_weight
    