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

FOLD = "res/"

class TestGetNodesEdges(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.known_ams = pd.read_excel(FOLD+"True Amounts.xlsx", header=None, 
                                      index_col=0, squeeze=True)
        cls.fnames = ["drug delivery system.csv", "journals_nanomedicine.csv",
                      "journals_journal of controlled release.csv",
                      "medical nanotechnology.csv",
                      "nanomedicine.csv", "nanoprobe.csv"]
                      
    @unittest.skip
    def testNodes(self):
        dfn = cb.get_nodes(self.fnames, self.known_ams, fold=FOLD)
        dfn.to_excel("out/nodes.xlsx")
        assert dfn.loc["drug delivery system", "Size"] == 110301
        
    def testNodesIntSim(self):
        dfn = cb.get_nodes(self.fnames, self.known_ams, 
                           int_sim = True, fold=FOLD)
        dfn.to_excel("out/nodes_int_sim.xlsx")
        assert dfn.loc["drug delivery system", "Size"] == 110301
        
    @unittest.skip
    def testEdges(self):
        dfe = cb.get_edges(self.fnames, self.known_ams, fold=FOLD)
        dfe.to_excel("out/edges.xlsx")
        assert round(dfe.loc[8, "Weight"], 3) == 0.240
        

        
    
if __name__ == '__main__':
    unittest.main()