"""
This module defines a Document object
which contains the features and the label
of an actual text document.


(C) 2020 Urdu News Clustering
"""


class Document:
    def __init__(
            self,
            text: str,
            features: str,
            source: str = 'User',
            category: str = 'User',
    ):
        self.source = source
        self.category = category
        self.text = text
        self.features = features

    def __repr__(self):
        return f'{self.category} - {self.text}'
