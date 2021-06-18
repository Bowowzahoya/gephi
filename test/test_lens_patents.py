# -*- coding: utf-8 -*-
"""
Created on Fri May  7 15:18:17 2021

@author: David
"""
import unittest
import pandas as pd

from context import gephi
from gephi.database_specific import lens_patent as lp

FOLD = "res/lens_patent/"


class TestGetEdge(unittest.TestCase):
    def testGetEdgeWeak(self):
        edge_getter = lp.EdgeGetter()
        fname1 = FOLD+"lidar.csv"
        fname2 = FOLD+"intelligent-traffic.csv"
        
        weight = edge_getter.get_edge_weight(fname1, fname2)
        assert weight < 0.001 and weight > 0.0001

    def testGetLimitedEdge(self):
        
        fname1 = FOLD+"autonomous-driving.csv"
        fname_large = FOLD+"neural-network.csv"
        
        lim_node_szs = pd.Series({fname_large:86_748})
        aware_edge_getter = lp.EdgeGetter(limited_node_sizes=lim_node_szs)
        aware_weight = aware_edge_getter.get_edge_weight(fname1, fname_large)
        
        unaware_edge_getter = lp.EdgeGetter()
        unaware_weight = unaware_edge_getter.get_edge_weight(fname1, fname_large)
        
        ratio = aware_weight / unaware_weight
        expected_ratio = 86_748 / 50_000

        assert ratio == expected_ratio 
        
    def testGetEdgeStrong(self):
        edge_getter = lp.EdgeGetter()
        fname1 = FOLD+"lidar.csv"
        fname2 = FOLD+"autonomous-driving.csv"
        
        weight = edge_getter.get_edge_weight(fname1, fname2)
        assert weight > 0.02 and weight < 0.03
   
class TestGetNode(unittest.TestCase):
    def testGetNode(self):
        node_getter = lp.NodeGetter()
        fname = FOLD+"lidar.csv"
        
        size = node_getter.get_node_size(fname)
        assert size == 8575
        
    def testGetLimitedNode(self):
        fname_large = FOLD+"neural-network.csv"
        lim_node_sz = pd.Series({fname_large:86_748})
        node_getter = lp.NodeGetter(limited_node_sizes=lim_node_sz)
        size = node_getter.get_node_size(fname_large)
        assert size == 86_748

class TestGetIntSim(unittest.TestCase):
    def testGetIntSimHigh(self):
        node_getter = lp.NodeGetter()
        fname = FOLD+"lidar.csv"
        
        intsim = node_getter.get_node_internal_similarity(fname)
        assert intsim > 0.02 and intsim < 0.03
        
    def testGetIntSimLow(self):
        node_getter = lp.NodeGetter()
        fname = FOLD+"crust.csv"
        
        intsim = node_getter.get_node_internal_similarity(fname)
        assert intsim > 0.005 and intsim < 0.01


if __name__ == '__main__':
    unittest.main()