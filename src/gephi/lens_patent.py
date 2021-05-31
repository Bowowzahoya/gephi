# -*- coding: utf-8 -*-
"""
Functions for dealing with Lens patent data
all on the basis of filename

- get_node()
- get_edge()
- get_int_sim(): internal cosine similarity
"""

import pandas as pd

from .tools import cossim

LID_COL = "Lens ID"
TI_COL = "Title"

def read(fname):
    """
    Reads an export from Lens

    Parameters
    ----------
    fname : str
        Content filename for node

    Returns
    -------
    df : pd.DataFrame
        Content of file in dataframe format
    """
    
    return pd.read_csv(fname, error_bad_lines=False, warn_bad_lines=False)

def get_node(fname, known_ams=pd.Series(), fold=""):
    """
    Returns amount size for node
    
    Takes care of fact that might be only partly downloaded
    by using known_ams
    
    Parameters
    ----------
    fname : str
        Content filename for node
    known_ams : Series
        Dictionary of known amounts per filename

    Returns
    -------
    sz : int
        Size of node
    """
    if fname in known_ams.index:
        return known_ams[fname]
    # else
    df = read(fold+fname)
    if len(df) >= 50000-10:
        print(f"  WARNING: export file '{fname}' at or over max amount of "+\
              "50,000, but no amount provided.")
    return len(df)

def get_edge(fname1, fname2, known_ams=pd.Series(), fold=""):
    """
    Returns edge strength between two nodes
    
    Takes care of fact that might be only partly downloaded
    by using known_ams

    Parameters
    ----------
    fname1 : str
        Content filename for node 1
    fname2 : str
        Content filename for node 2
    known_ams : Series
        Dictionary of known amounts per filename

    Returns
    -------
    strgth : Series
        edges of node, with index node pair, value strength
    """
    df1 = read(fold+fname1)
    df2 = read(fold+fname2)
    
    am1 = known_ams.get(fname1, len(df1))
    am2 = known_ams.get(fname2, len(df2))

    min_cov = min(len(df1)/am1, len(df2)/am2)
    
    overlap = df1[df1[LID_COL].isin(df2[LID_COL])]
    return (len(overlap)/am1)/min_cov

def get_int_sim(fname, fold="", max_=20000):
    """
    Returns internal similarity of a node
    
    will calculate based on cosine similarity of titles

    Parameters
    ----------
    fname : str
        Content filename for node


    Returns
    -------
    int_sim : float
        internal similarity

    """
    df = read(fold+fname)
    df = df.iloc[:max_]
    ti = df[TI_COL]
    ics = cossim(ti)
    return ics
    

