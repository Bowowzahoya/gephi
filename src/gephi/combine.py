# -*- coding: utf-8 -*-
"""
Data source agnostic functions for creating
all edges and nodes

Main functions:
    - get_nodes_edges()
    - get_nodes()
    - get_edges()
"""
import pandas as pd

from .scopus import get_node, get_edge, get_int_sim

LB_COL = "Label"
SR_COL = "Strength"
SZ_COL = "Size"
IS_COL = "Internal similarity"
ID_COL = "Id"
SC_COL = "Source"
TG_COL = "Target"
W_COL = "Weight"

def get_nodes_edges(fnames, known_ams=pd.Series(), db="scopus", 
                    int_sim=False, fold="", **kwargs):
    """
    Create nodes and edges in Gephi format from filenames

    Parameters
    ----------
    fnames : list-like
        List of filename strings
    known_ams : Series
        Dictionary of known amounts per filename
    db (Optional): string, default "scopus"
        database used (for now only "scopus" possible)
    int_sim (Optional): bool, default False
        whether to calculate internal similarity or not (will take more time)

    Returns
    -------
    nodes : DataFrame
        nodes in Gephi format
    edges : DataFrame
        edges in Gephi format

    """
    nodes = get_nodes(fnames, known_ams=pd.Series(), db=db, int_sim=int_sim, 
                      fold=fold, **kwargs)
    
    edges = get_edges(fnames, known_ams=pd.Series(), db=db, fold=fold,
                      **kwargs)

    return nodes, edges
            
def get_nodes(fnames, known_ams=pd.Series(), db="scopus", 
              int_sim=False, fold="", **kwargs):
    columns = [LB_COL, SZ_COL]
    if int_sim: columns.append(IS_COL)
    nodes = pd.DataFrame(columns=columns)
    

    for i, fname in enumerate(fnames):
        name = fname[:-4]
        nodes.loc[name, LB_COL] = name
        nodes.loc[name, SZ_COL] = get_node(fname, known_ams, fold=fold)
        if int_sim:
            nodes.loc[name, IS_COL] = get_int_sim(fname, fold=fold)
    nodes.index.name = ID_COL
    return nodes

def get_edges(fnames, known_ams=pd.Series(), db="scopus", 
              fold="", **kwargs):
    columns = [SC_COL, TG_COL, W_COL]
    edges = pd.DataFrame(columns=columns)
    
    i = 0
    for j, fname1 in enumerate(fnames):
        for k, fname2 in enumerate(fnames):
            if fname1==fname2:
                continue
            
            name1 = fname1[:-4]
            name2 = fname2[:-4]
            edges.loc[i, SC_COL] = name1
            edges.loc[i, TG_COL] = name2
            edges.loc[i, W_COL] = get_edge(fname1, fname2, known_ams, fold=fold)

            i +=  1
    return edges
    
    