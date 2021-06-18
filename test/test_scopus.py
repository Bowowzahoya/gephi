# -*- coding: utf-8 -*-
"""
Created on Fri May  7 15:18:17 2021

@author: David
"""
import unittest
import pandas as pd

from context import gephi
from gephi.database_specific import scopus as sc

FOLD = "res/scopus/"

class TestGetEdge(unittest.TestCase):
    def testGetEdgeWeak(self):
        edge_getter = sc.EdgeGetter()
        fname1 = FOLD+"nanoprobe.csv"
        fname2 = FOLD+"medical nanotechnology.csv"
        
        weight = edge_getter.get_edge_weight(fname1, fname2)
        assert weight > 0.01 and weight < 0.02

    def testGetLimitedEdge(self):
        
        fname1 = FOLD+"nanoprobe.csv"
        fname_large = FOLD+"drug delivery system.csv"
        
        lim_node_szs = pd.Series({fname_large:110_301})
        aware_edge_getter = sc.EdgeGetter(limited_node_sizes=lim_node_szs)
        aware_weight = aware_edge_getter.get_edge_weight(fname1, fname_large)
        
        unaware_edge_getter = sc.EdgeGetter()
        unaware_weight = unaware_edge_getter.get_edge_weight(fname1, fname_large)
        
        ratio = aware_weight / unaware_weight
        expected_ratio = 110_301 / 20_000

        assert round(ratio,3) == round(expected_ratio,3)
        
    def testGetEdgeStrong(self):
        edge_getter = sc.EdgeGetter()
        fname1 = FOLD+"nanoprobe.csv"
        fname2 = FOLD+"journals_journal of controlled release.csv"

        
        weight = edge_getter.get_edge_weight(fname1, fname2)
        assert weight > 0.001 and weight < 0.003
 
@unittest.skip
class TestGetNode(unittest.TestCase):
    def testGetNode(self):
        node_getter = sc.NodeGetter()
        fname = FOLD+"nanoprobe.csv"
        
        size = node_getter.get_node_size(fname)
        assert size == 4772
        
    def testGetLimitedNode(self):
        fname_large = FOLD+"drug delivery system.csv"
        lim_node_sz = pd.Series({fname_large:110_301})
        node_getter = sc.NodeGetter(limited_node_sizes=lim_node_sz)
        size = node_getter.get_node_size(fname_large)
        assert size == 110_301

@unittest.skip
class TestGetIntSim(unittest.TestCase):
    def testGetIntSimHigh(self):
        node_getter = sc.NodeGetter()
        fname = FOLD+"nanoprobe.csv"
        
        intsim = node_getter.get_node_internal_similarity(fname)
        assert intsim < 0.1 and intsim > 0.01
        
    def testGetIntSimLow(self):
        node_getter = sc.NodeGetter()
        fname = FOLD+"space.csv"
        
        intsim = node_getter.get_node_internal_similarity(fname)
        assert intsim <  0.01 and intsim > 0.001


if __name__ == '__main__':
    unittest.main()