# -*- coding: utf-8 -*-
"""
Utilities

main functions:
    - cossim(): calculates internal cosine similarity from a list of strings
"""

import pandas as pd
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

def cossim(s_list):
    """
    Returns internal cosine similarity
    
    see https://www.machinelearningplus.com/nlp/cosine-similarity/
    for explanation

    Parameters
    ----------
    s_list : list-like
        list of strings

    Returns
    -------
    None.

    """
    count_vectorizer = TfidfVectorizer(stop_words='english')
    sp_mat = count_vectorizer.fit_transform(s_list)
    
    # to actually view, uncomment:
    # doc_term_matrix = sp_mat.todense()
    # df = pd.DataFrame(doc_term_matrix, 
    #               columns=count_vectorizer.get_feature_names(), 
    #               index=np.arange(len(s_list)))
    # df.to_excel("df.xlsx")
    
    cs_mat = cosine_similarity(sp_mat, sp_mat)
    cs_list = cs_mat[np.triu_indices(len(cs_mat), k=1)]
    return sum(cs_list)/len(cs_list)
    