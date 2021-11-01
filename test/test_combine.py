# -*- coding: utf-8 -*-
"""
Created on Fri May  7 15:18:17 2021

@author: David
"""
import unittest
import pandas as pd
import os

from context import gephi
from gephi import combine as cb

FOLD = "res/scopus/"

class TestGetNodesEdges(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.known_ams = pd.read_excel(FOLD+"True Amounts.xlsx", header=None, 
                                    index_col=0, squeeze=True)
        cls.fnames = ["drug delivery system.csv", "journals_nanomedicine.csv",
                    "journals_journal of controlled release.csv",
                    "medical nanotechnology.csv",
                    "nanomedicine.csv", "nanoprobe.csv"]
        cls.fnames = [FOLD+f for f in cls.fnames]
    
    @unittest.skip
    def testNodes(self):
        dfn = cb.get_nodes(self.fnames, limited_node_sizes=self.known_ams)
        dfn.to_excel("out/nodes.xlsx")
        assert dfn.loc["drug delivery system", "Size"] == 110301
        
    def testNodesLimitedAmounts(self):
        dfn = cb.get_nodes(self.fnames, includes_internal_similarity = True,
                        limited_node_sizes=self.known_ams,
                        max_length_to_calc=10)
        dfn.to_excel("out/nodes_limited.xlsx")
        assert round(dfn.loc["drug delivery system", "Internal similarity"],3) == 0.024

    @unittest.skip
    def testNodesIntSim(self):
        dfn = cb.get_nodes(self.fnames, limited_node_sizes=self.known_ams, 
                        includes_internal_similarity = True)
        dfn.to_excel("out/nodes_int_sim.xlsx")
        assert dfn.loc["drug delivery system", "Size"] == 110301
        
    @unittest.skip
    def testEdges(self):
        dfe = cb.get_edges(self.fnames, limited_node_sizes=self.known_ams)
        dfe.to_excel("out/edges.xlsx")
        assert round(dfe.loc[8, "Weight"], 3) == 0.168
        

        
    
if __name__ == '__main__':
    unittest.main()