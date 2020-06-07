"""
This file defines the preprocessing method.
For now, it removes punctuation and stopwords.


(C) 2020 Urdu News Clustering
"""
from typing import Optional, Set


def extract_features(text: str, stopwords: Optional[Set[str]], truncate: int = 7):
    """
    Returns set of terms from a string.

    :param truncate: terms longer than this will be truncated to this length
    :param stopwords: set of stop words
    :param text: original string
    :return: set of tokens after removing punctuation and stop words.
    """
    punctuation_marks = ['\'', '\"', '.', '،', ',', '!', '؟', '’', '۔', '‘', '-', 'ء', '؛']

    # remove punctuation marks
    for pm in punctuation_marks:
        if pm in text:
            text = text.replace(pm, ' ')

    terms = set(text.split())  # split into tokens

    if stopwords is not None:  # remove stopwords
        terms.difference_update(stopwords)

    trunc_terms: Set[str] = set()
    for term in terms:
        if len(term) > truncate:
            trunc_terms.add(term[:truncate])
        else:
            trunc_terms.add(term)

    return trunc_terms
