"""
This file defines the vector space model created
for the headlines. It uses TF-IDF for scaling and
cosine similarity measure.


(C) 2020 Urdu News Clustering
"""

from collections import Counter
from typing import List

import numpy as np
import pandas as pd

from unc_document import Document


def create_vsm_matrix(documents: List[Document]):
    """
    Creates a vector space model matrix from the given headlines.

    :param documents: List of headlines
    :return: vsm as a pandas dataframe
    """
    # count frequencies of features in every document
    term_frequencies = {doc_id: Counter(doc.features) for doc_id, doc in enumerate(documents)}

    # create vsm_matrix (DataFrame)
    vsm_matrix = pd.DataFrame.from_dict(data=term_frequencies, orient='index')
    vsm_matrix.fillna(0, inplace=True)

    # drop features present in single documents only
    vsm_matrix.drop(axis=1, inplace=True,
                    columns=[col for col, val in vsm_matrix.sum().iteritems() if val < 2]
                    )

    vsm_matrix = _apply_tfidf(vsm_matrix)
    vsm_matrix = _apply_normalization(vsm_matrix)

    return vsm_matrix


def _apply_tfidf(vsm_matrix):
    # sum nonzero values along vertical axis
    document_frequencies = (vsm_matrix != 0).sum(0)
    idf_vector = np.log(vsm_matrix.shape[0] / document_frequencies)

    vsm_matrix = np.log(vsm_matrix + 1)
    vsm_matrix *= idf_vector

    return vsm_matrix


def _apply_normalization(vsm_matrix):
    row_magnitudes = np.sqrt(np.square(vsm_matrix).sum(axis=1))
    vsm_matrix = vsm_matrix.div(row_magnitudes, axis=0)
    vsm_matrix.fillna(value=0, inplace=True)

    return vsm_matrix


def _measure_cos_sim(columns_set: pd.DataFrame, rows_set: pd.DataFrame):
    similarity_matrix = rows_set.dot(columns_set.transpose())
    return similarity_matrix
