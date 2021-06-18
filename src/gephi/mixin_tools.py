# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

def get_internal_cosine_similarity(string_list, save_as=False):
    """
    Returns internal cosine similarity of a list of strings
    
    see https://www.machinelearningplus.com/nlp/cosine-similarity/
    for explanation
    """
    count_vectorizer = TfidfVectorizer(stop_words='english')
    sparse_matrix = count_vectorizer.fit_transform(string_list)
    
    if save_as:
        document_term_matrix = sparse_matrix.todense()
        columns = count_vectorizer.get_feature_names()
        index = np.arange(len(string_list))
        document_term_df = pd.DataFrame(document_term_matrix, 
                                        columns=columns, 
                                        index=index)
        document_term_df.to_excel(save_as)
    
    cossim_matrix = cosine_similarity(sparse_matrix, sparse_matrix)
    cossim_list = cossim_matrix[np.triu_indices(len(cossim_matrix), k=1)]
    return sum(cossim_list)/len(cossim_list)
    