# -*- coding: utf-8 -*-
"""
Created on Fri May  7 15:18:17 2021

@author: David
"""
import unittest
import pandas as pd

from context import gephi
from gephi import scopus as sc

FOLD = "res/"

class TestGetEdge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.known_ams = pd.read_excel(FOLD+"True Amounts.xlsx", header=None, 
                                      index_col=0, squeeze=True)
        cls.fname1 = "drug delivery system.csv"
        cls.fname2 = "journals_nanomedicine.csv"

    def testGetEdge(self):
        strgth = sc.get_edge(self.fname1, self.fname2, self.known_ams,
                             fold=FOLD)
        assert round(strgth, 3) == 0.281
        
class TestGetEdge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.known_ams = pd.read_excel(FOLD+"True Amounts.xlsx", header=None, 
                                      index_col=0, squeeze=True)
        cls.fname = "drug delivery system.csv"
        
    def testGetNode(self):
        sz = sc.get_node(self.fname, self.known_ams, fold=FOLD)
        assert sz == 110301

class TestGetIntSim(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.known_ams = pd.read_excel(FOLD+"True Amounts.xlsx", header=None, 
                                      index_col=0, squeeze=True)
        cls.fname = "drug delivery system.csv"
        
    def testGetIntSim(self):
        sz = sc.get_node(self.fname, self.known_ams, fold=FOLD)
        assert sz == 110301
        
if __name__ == '__main__':
    unittest.main()