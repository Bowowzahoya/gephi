# -*- coding: utf-8 -*-
"""
Created on Fri May  7 15:18:17 2021

@author: David
"""
import unittest
import pandas as pd

from context import gephi
from gephi import mixin_tools as to

import os

THIS_FOLDER = os.path.dirname(__file__)
FOLD = THIS_FOLDER+"/res/scopus/"

class TestCosSim(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = ["drug delivery system.csv", "nanosphere nursery.csv",
            "space.csv"]

    def testCosSim(self):
        expected_outcomes = [0.01110, 0.00657, 0.00450]
        for file_, expected_outcome in zip(self.files, expected_outcomes):
            df = pd.read_csv(FOLD+file_)
            ti = df.iloc[:10000]["Title"]
            ics = to.get_internal_cosine_similarity(ti)
            print(file_, ics)
            assert round(ics, 5) == expected_outcome

        
if __name__ == '__main__':
    unittest.main()