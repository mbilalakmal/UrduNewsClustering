"""
This file defines clustering methods fo the documents.
Jackard similarity index is used to form clusters.


(C) 2020 Urdu News Clustering
"""
from typing import List

from unc_document import Document


def get_similar_documents(
        query_document: Document,
        documents: List[Document],
        threshold: float = 0.20
):
    """
    Returns list of documents similar to the given document.
    Documents with similarity below `threshold` will not be included.
    """
    similar_documents: List[Document] = list()

    for document in documents:
        jackard_index: float = _get_jackard_index(query_document, document)
        if jackard_index >= threshold:
            similar_documents.append(document)

    return similar_documents


def _get_jackard_index(document1: Document, document2: Document):
    """
    Calculates and returns the jackard index between two documents
    represented as sets of features.
    :param document1: First Document
    :param document2: Second Document
    :return: jackard index value defined as intersection/union
    """
    common: set = document1.features.intersection(document2.features)
    union: set = document1.features.union(document2.features)
    ji: float = len(common) / len(union) if len(union) > 0 else 0
    return ji
