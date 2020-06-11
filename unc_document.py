"""
This module defines a Document object
which contains the features and the label
of an actual text document.


(C) 2020 Urdu News Clustering
"""

from typing import Set


class Document:
    def __init__(
            self,
            text: str,
            features: Set[str],
            source: str = 'User',
            category: str = 'User',
    ):
        """
        :param text: sequence of characters forming the news headline
        :param features: set of terms after stopwords and punctuation is removed
        :param source: news source for the article
        :param category: category for the article
        """
        self.source = source
        self.category = category
        self.text = text
        self.features = features

    def __repr__(self):
        return f'{self.category} - {self.text}'
