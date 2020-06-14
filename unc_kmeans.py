"""
This file defines the k means clustering using
vector space model with TF-IDF.


(C) 2020 Urdu News Clustering
"""

from collections import Counter
from typing import List

import numpy as np
import pandas as pd

from unc_document import Document
from unc_vsm_indexer import _measure_cos_sim, create_vsm_matrix


def evaluate_clustering(documents: List[Document], k: int = 4):
    """
    Performs KMeans clustering with the given value of k.

    :param documents: List of headlines
    :param k: Number of clusters
    :return: Purity, number of iterations, and the clusters formed
    """
    # create the vector space model
    vsm_matrix = create_vsm_matrix(documents)

    # select k centroids at random
    centroids = pd.DataFrame.copy(vsm_matrix.sample(n=k), deep=True)
    centroids.reset_index(drop=True, inplace=True)

    clusters = {}  # k clusters [0.. k-1]

    iterations = 0
    while True:  # centroids are changing
        iterations += 1
        similarity_matrix = _measure_cos_sim(centroids, vsm_matrix)
        cluster_vector = _create_cluster_vector(similarity_matrix)

        # map documents to clusters {cluster_id: [doc_id1 .. doc_idk]}
        clusters = cluster_vector.groupby(cluster_vector).groups
        clusters = {idx: vsm_matrix.loc[indices] for idx, indices in clusters.items()}

        old_centroids = centroids
        centroids = _calculate_centroids(clusters)

        if centroids.equals(old_centroids):
            break  # stop if centroids and clusters are not changing

    results = {idx: vectors.index for idx, vectors in clusters.items()}

    # Cluster X Category Matrix used for purity measure
    summary = {}
    for idx, doc_ids in results.items():
        summary[idx] = [documents[doc_id].category for doc_id in doc_ids]

    summary = {cluster_id: Counter(categories) for cluster_id, categories in summary.items()}
    summary = pd.DataFrame.from_dict(data=summary, orient='index')
    summary.fillna(0, inplace=True)

    # purity is 1/N * (sum of count of most common class in each cluster)
    purity = summary.max(axis=1).sum()
    purity /= summary.values.sum()

    results = {idx: [documents[doc_id] for doc_id in doc_ids] for idx, doc_ids in results.items()}

    return purity, iterations, summary, results


def _create_cluster_vector(similarity_matrix: pd.DataFrame) -> pd.Series:
    return similarity_matrix.idxmax(axis=1)  # max because similarity measure


def _calculate_centroids(clusters: dict):
    # average of all vectors within the cluster

    #                               | collapse index
    centroids = {idx: vectors.mean(axis=0) for idx, vectors in clusters.items()}
    centroids = pd.DataFrame.from_dict(centroids, orient='index')

    # normalize
    row_magnitudes = np.sqrt(np.square(centroids).sum(axis=1))
    centroids = centroids.div(row_magnitudes, axis=0)

    return centroids
