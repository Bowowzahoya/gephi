# -*- coding: utf-8 -*-
"""
Data source agnostic function get_nodes_edges() for creating
edges and nodes
"""
from .nodes import get_nodes
from .edges import get_edges

def get_nodes_edges(fnames, **kwargs):
    nodes = get_nodes(fnames, **kwargs)
    edges = get_edges(fnames, **kwargs)

    return nodes, edges