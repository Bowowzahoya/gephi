# -*- coding: utf-8 -*-

import pandas as pd

from .mixin_tools import get_internal_cosine_similarity

import logging
log = logging.getLogger(__name__)

class NodeGetterMixin():
    def __init__(self, limited_node_sizes=pd.Series(dtype="object"), *args, **kwargs):
        # supplied for nodes with more documents than the export maximum
        self.limited_node_sizes = limited_node_sizes
        
    def get_node_size(self, filename):
        if filename in self.limited_node_sizes.index:
            return self.limited_node_sizes[filename]
        
        doc_export = _read(filename)
        
        max_export_length = self.MAX_EXPORT_LENGTH-self.MARGIN
        if len(doc_export) >= max_export_length:
            log.warning(f"Export '{filename}' at max length"+\
                f" of {self.MAX_EXPORT_LENGTH}, "+\
                " but no node size provided.")
        return len(doc_export)
    
    def get_node_internal_similarity(self, filename, 
            max_length_to_calc=20_000, 
            **kwargs):
        doc_export = _read(filename)
        doc_export = doc_export.iloc[:max_length_to_calc]
        
        contents = doc_export[self.CONTENT_COL].copy()
        contents = contents.dropna()
        
        internal_cossim = get_internal_cosine_similarity(contents)
        return internal_cossim
    
class EdgeGetterMixin():
    def __init__(self, limited_node_sizes=pd.Series(dtype="object"), *args, **kwargs):
        # supplied for nodes with more documents than the export maximum
        self.limited_node_sizes = limited_node_sizes
        
        # will accumulate as get_edge gets run
        # stores information that makes it possible to avoid costly 
        # recalculating for reverse edges
        self.overlap_sizes = pd.Series()
        self.node_sizes = pd.Series()
        self.min_coverages = pd.Series()
        
    def get_edge_weight(self, filename1, filename2):
        edge_name = _unify_edge_name(filename1, filename2)
        if edge_name in self.overlap_sizes.index:
            log.info("\t  Loading from cache...")
            return self.get_edge_from_cache(filename1, filename2)
        else:
            log.info("\t  Calculating...")
            return self.calculate_and_cache_edge(filename1, filename2)
        
    def calculate_and_cache_edge(self, filename1, filename2):
        doc_export1 = _read(filename1)
        doc_export2 = _read(filename2)
        
        node1_size = self.limited_node_sizes.get(filename1, len(doc_export1))
        node2_size = self.limited_node_sizes.get(filename2, len(doc_export2))
    
        node1_coverage = len(doc_export1)/node1_size
        node2_coverage = len(doc_export2)/node2_size
        min_coverage = min(node1_coverage, node2_coverage)
        
        overlap_msk = doc_export1[self.ID_COL].isin(doc_export2[self.ID_COL])
        overlap = doc_export1[overlap_msk]
        overlap_size = len(overlap)
        
        # cache
        edge_name = _unify_edge_name(filename1, filename2)
        self.overlap_sizes[edge_name] = overlap_size
        self.node_sizes[filename1] = node1_size
        self.node_sizes[filename2] = node2_size
        self.min_coverages[edge_name] = min_coverage
        
        return (overlap_size/node1_size)/min_coverage
    
    def get_edge_from_cache(self, filename1, filename2):
        edge_name = _unify_edge_name(filename1, filename2)
        overlap_size = self.overlap_sizes[edge_name]
        node1_size = self.node_sizes[filename1]
        min_coverage = self.min_coverages[edge_name]
        
        return (overlap_size/node1_size)/min_coverage
        
    
def _read(filename):
    if filename[-min(len(filename), 4):] == ".csv":
        return pd.read_csv(filename, 
            on_bad_lines="skip")
    elif filename[-min(len(filename), 5):] == ".xlsx":
        return pd.read_excel(filename, 
            on_bad_lines="skip")
    else:
        raise Exception(f"filename extension of '{filename}' not recognized.")

def _unify_edge_name(filename1, filename2):
    # need same name regardless of order
    sorted_filenames = sorted([filename1, filename2])
    return "-".join(sorted_filenames)






    
    

