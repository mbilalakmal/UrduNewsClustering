"""
This file defines the preprocessing method.
For now, it removes punctuation and stopwords.


(C) 2020 Urdu News Clustering
"""
from typing import Optional


def extract_features(text: str, stopwords: Optional[set]) -> set:
    """
    Returns set of terms from a string.

    :param stopwords: set of stop words
    :param text: original string
    :return: set of tokens after removing punctuation and stop words.
    """
    punctuation_marks = ['\'', '\"', '.', '،', ',', '!', '؟', '’', '۔', '‘']

    # remove punctuation marks
    for pm in punctuation_marks:
        if pm in text:
            text = text.replace(pm, ' ')

    terms = set(text.split())  # split into tokens

    if stopwords:  # remove stopwords
        terms.difference_update(stopwords)

    return terms
