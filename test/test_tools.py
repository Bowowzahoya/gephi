# -*- coding: utf-8 -*-
"""
Created on Fri May  7 15:18:17 2021

@author: David
"""
import unittest
import pandas as pd

from context import gephi
from gephi import tools as to

FOLD = "res/"

class TestCosSim(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fs = ["drug delivery system.csv", "nanosphere nursery.csv",
                  "space.csv"]

    def testCosSim(self):
        for f in self.fs:
            df = pd.read_csv(FOLD+f)
            ti = df.iloc[:10000]["Title"]
            ics = to.cossim(ti)
            print(f, ics)
        
if __name__ == '__main__':
    unittest.main()