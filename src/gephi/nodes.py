# -*- coding: utf-8 -*-
"""
Data source agnostic function get_nodes() for creating
nodes
"""
import pandas as pd

from .database_specific import scopus as sc
from .database_specific import lens_patent as lp
from .constants import ID_COL, LABEL_COL, SIZE_COL, INTERNAL_SIMILARITY_COL
            
def get_nodes(filenames, database="scopus", 
              includes_internal_similarity=False, **kwargs):

    nodes = _get_empty_nodes_dataframe(includes_internal_similarity)
    get_node_size, get_node_internal_similarity = _get_get_functions(database, 
                                                                     **kwargs)
    
    for filename in filenames:
        print(f"Determining label for '{filename}'...")
        label = get_node_label(filename)
        print(f"  {label}")
        nodes.loc[label, LABEL_COL] = label
        
        print(f"Determining node size for '{filename}'...")
        size = get_node_size(filename)
        print(f"  {size}")
        nodes.loc[label, SIZE_COL] = size
            
        if includes_internal_similarity:
            print(f"Determining node internal similarity for '{filename}'...")
            internal_similarity = get_node_internal_similarity(filename, 
                                                               **kwargs)
            print(f"  {internal_similarity}")
            nodes.loc[label, INTERNAL_SIMILARITY_COL] = internal_similarity

    return nodes

def _get_get_functions(database, **kwargs):
    if database == "scopus":
        node_getter = sc.NodeGetter(**kwargs)
        get_node_size = node_getter.get_node_size
        get_node_internal_similarity = node_getter.get_node_internal_similarity
    elif database == "lens":
        node_getter = lp.NodeGetter(**kwargs)
        get_node_size = node_getter.get_node_size
        get_node_internal_similarity = node_getter.get_node_internal_similarity
    else:
        raise NotImplementedError(f"database {database} not valid.")
        
    return get_node_size, get_node_internal_similarity

def _get_empty_nodes_dataframe(includes_internal_similarity):
    columns = [LABEL_COL, SIZE_COL]
    if includes_internal_similarity: 
        columns.append(INTERNAL_SIMILARITY_COL)
        
    nodes = pd.DataFrame(columns=columns)
    nodes.index.name = ID_COL
    return nodes

def get_node_label(filename):
    only_filename = filename.split("/")[-1]
    label = only_filename.split(".")[0]
    return label


    