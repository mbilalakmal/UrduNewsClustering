"""
This file defines clustering methods fo the documents.
Jackard similarity index is used to form clusters.


(C) 2020 Urdu News Clustering
"""
from typing import List

from unc_document import Document


def get_similar_documents(query_doc_id: int, documents: dict, threshold: float = 0.25) -> List[int]:
    """
    Returns list of documents similar to the given document.
    Documents with similarity below `threshold` will not be included.

    :param threshold: lower bound on similarity index
    :param documents: The collection of documents to search from.
    :param query_doc_id: The original document selected by the user.
    :return: list of documents similar to the query document.
    """
    query_document: Document = documents[query_doc_id]
    similar_doc_ids: List[int] = list()

    for doc_id, document in documents.items():
        jackard_index: float = _get_jackard_index(query_document, document)
        if jackard_index >= threshold:
            similar_doc_ids.append(doc_id)

    return similar_doc_ids


def _get_jackard_index(document1: Document, document2: Document) -> float:
    # ji = (d1 intersection d2) / (d1 union d2)
    common: set = document1.features.intersection(document2.features)
    union: set = document1.features.union(document2.features)
    ji: float = len(common) / len(union)
    return ji
