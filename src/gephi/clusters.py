import pandas as pd
from .constants import *

import logging
log = logging.getLogger(__name__)

def get_cluster_info(exported_nodes, edges):
    columns = [INSIDE_WEIGHT_COL, OUTSIDE_WEIGHT_COL, 
        MEAN_INTERNAL_SIMILARITY_COL, 
        MIN_CLUSTER_SIZE_COL, MAX_CLUSTER_SIZE_COL]

    clusters = pd.DataFrame(columns=columns)
    sizes = exported_nodes[EXPORTED_SIZE_COL]
    groupby = exported_nodes.groupby(CLUSTER_COL)
    
    clusters[MEAN_INTERNAL_SIMILARITY_COL] = groupby.apply(_get_weighted_mean, EXPORTED_INTERNAL_SIMILARITY_COL)
    
    for cluster in clusters.index:
        return_ = _get_nodes_edges_inside_outside(exported_nodes, edges, cluster)
        nodes_in_cluster, edges_in_cluster, nodes_out_cluster, edges_out_cluster = return_
        
        clusters.loc[cluster, [MIN_CLUSTER_SIZE_COL, MAX_CLUSTER_SIZE_COL]] = \
            _get_sizes(clusters, edges_in_cluster, nodes_in_cluster)
        
        inside_weights = _get_weighted_mean_weights(nodes_in_cluster, edges_in_cluster, sizes, skip_one=False)
        outside_weights = _get_weighted_mean_weights(nodes_in_cluster, edges_out_cluster, sizes, skip_one=False)
        
        clusters.loc[cluster, INSIDE_WEIGHT_COL] = (inside_weights*sizes[inside_weights.index]).sum()/sizes[inside_weights.index].sum()
        clusters.loc[cluster, OUTSIDE_WEIGHT_COL] = (outside_weights*sizes[outside_weights.index]).sum()/sizes[outside_weights.index].sum()
        
        ids_in_cluster = exported_nodes.loc[exported_nodes[CLUSTER_COL] == cluster].index
        for cluster2 in sorted(exported_nodes[CLUSTER_COL].unique()):
            if cluster2 == cluster:
                clusters.loc[cluster, WEIGHT_PREFIX_COL+str(cluster2)] = clusters.loc[cluster, INSIDE_WEIGHT_COL]
            ids_in_cluster2 = exported_nodes.loc[exported_nodes[CLUSTER_COL] == cluster2].index
            edges_in_cluster2 = edges[edges[SOURCE_COL].isin(ids_in_cluster.to_list()) & edges[TARGET_COL].isin(ids_in_cluster2.to_list())]
            
            cluster_weights = _get_weighted_mean_weights(nodes_in_cluster, edges_in_cluster2, sizes, skip_one=False)
            clusters.loc[cluster, WEIGHT_PREFIX_COL+str(cluster2)] = \
                (cluster_weights*sizes[cluster_weights.index]).sum()/sizes[cluster_weights.index].sum()
        
    return clusters

def get_cluster_info_nodes(exported_nodes, edges):
    clusters = exported_nodes[CLUSTER_COL].unique()
    sizes = exported_nodes[EXPORTED_SIZE_COL]
    
    for cluster in clusters:
        return_ = _get_nodes_edges_inside_outside(exported_nodes, edges, cluster)
        nodes_in_cluster, edges_in_cluster, nodes_out_cluster, edges_out_cluster = return_
        ids_in_cluster = nodes_in_cluster.index
        
        inside_weights = _get_weighted_mean_weights(nodes_in_cluster, edges_in_cluster, sizes, skip_one=False)
        exported_nodes.loc[ids_in_cluster, INSIDE_WEIGHT_COL] = inside_weights
        
        outside_weights = _get_weighted_mean_weights(nodes_in_cluster, edges_out_cluster, sizes, skip_one=False)
        exported_nodes.loc[ids_in_cluster, OUTSIDE_WEIGHT_COL] = outside_weights
        
    edges = edges.sort_values(by=[WEIGHT_COL], ascending=False)
    for node in exported_nodes.index:
        cluster = exported_nodes.loc[node, CLUSTER_COL]
        
        exported_nodes.loc[node, TOP_5_WEIGHTS_COL] = \
            _format_edges_for_print(edges[edges[SOURCE_COL] == node].iloc[0:5])
        
        for cluster2 in sorted(clusters):
            if cluster2 == cluster:
                exported_nodes.loc[node, WEIGHT_PREFIX_COL+str(cluster2)] = exported_nodes.loc[node, INSIDE_WEIGHT_COL]
            ids_in_cluster2 = exported_nodes.loc[exported_nodes[CLUSTER_COL] == cluster2].index
            edges_in_cluster2 = edges[(edges[SOURCE_COL] == node) & edges[TARGET_COL].isin(ids_in_cluster2.to_list())]
            
            exported_nodes.loc[node, WEIGHT_PREFIX_COL+str(cluster2)] = \
                _get_weighted_mean_weights(exported_nodes.loc[[node]], edges_in_cluster2, sizes, skip_one=False).iloc[0]
            
    exported_nodes = exported_nodes.sort_values(by=[CLUSTER_COL]) 
    
    return exported_nodes


def _format_edges_for_print(edges):
    s= ""
    for index in edges.index:
        target = edges.loc[index, TARGET_COL]
        weight = edges.loc[index, WEIGHT_COL]
        s+= f"{target}: "
        s+= "{:.5f}".format(weight)+"\n"
    return s

def _get_nodes_edges_inside_outside(exported_nodes, edges, cluster):
    ids_in_cluster = exported_nodes.loc[exported_nodes[CLUSTER_COL] == cluster].index
    ids_out_cluster = exported_nodes.loc[exported_nodes[CLUSTER_COL] != cluster].index
    nodes_in_cluster = exported_nodes.loc[ids_in_cluster]
    edges_in_cluster = edges.loc[edges[SOURCE_COL].isin(ids_in_cluster.to_list()) & edges[TARGET_COL].isin(ids_in_cluster.to_list())]
    
    nodes_out_cluster = exported_nodes.loc[ids_out_cluster]
    edges_out_cluster = edges.loc[edges[SOURCE_COL].isin(ids_in_cluster.to_list()) & edges[TARGET_COL].isin(ids_out_cluster.to_list())]
    return nodes_in_cluster, edges_in_cluster, nodes_out_cluster, edges_out_cluster

def _get_sizes(clusters, edges_in_cluster, nodes_in_cluster):
    sizes_of_overlap = _get_overlap_from_weights(edges_in_cluster, nodes_in_cluster[EXPORTED_SIZE_COL])
        
    return max(nodes_in_cluster[EXPORTED_SIZE_COL].sum()-sizes_of_overlap.sum(), 
        nodes_in_cluster[EXPORTED_SIZE_COL].max()), \
        nodes_in_cluster[EXPORTED_SIZE_COL].sum()-sizes_of_overlap.max() 
    
    return clusters
    

def _get_weighted_mean(nodes, column_name, size_col=EXPORTED_SIZE_COL):
    return (nodes[size_col]*nodes[column_name]).sum()/nodes[size_col].sum()

def _get_overlap_from_weights(edges, sizes, skip_one=True):
    if skip_one:
        edges.loc[edges[WEIGHT_COL] == 1, WEIGHT_COL] = 0
        
    overlap = pd.Series(index=edges.index)
    for source in sizes.index:
        mask = edges[SOURCE_COL] == source
        overlap.loc[mask] = edges.loc[mask, WEIGHT_COL]*sizes.loc[source]
    return overlap

def _get_weighted_mean_weights(nodes, edges, sizes, skip_one=True, col=TARGET_COL):
    weights = pd.Series(index=nodes.index, dtype="object")
    for node in nodes.index:
        node_edges = edges.loc[edges[SOURCE_COL] == node]
        weights[node] = _get_weighted_mean_weight(node_edges, sizes, 
            skip_one=skip_one, col=col)
    return weights
        
    

def _get_weighted_mean_weight(one_node_edges, sizes, 
        skip_one=True, col=TARGET_COL):
    if skip_one:
        one_node_edges.loc[one_node_edges[WEIGHT_COL] == 1, WEIGHT_COL] = 0
    one_node_edges = one_node_edges.set_index(col)
    
    overlap_index = [i for i in one_node_edges.index if i in sizes.index]
    
    return (one_node_edges.loc[overlap_index, WEIGHT_COL]*sizes.loc[overlap_index]).sum()/sizes.loc[overlap_index].sum()


    
    