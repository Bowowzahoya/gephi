# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 15:30:43 2020

@author: david
"""

import os
import sys
package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                            '../src'))
if package_path not in sys.path:
    sys.path.insert(0, package_path)

import gephi