"""
This module defines a Document object
which contains the features and the label
of an actual text document.


(C) 2020 Urdu News Clustering
"""


class Document:
    def __init__(
            self,
            source: str,
            category: str,
            text: str,
            features: str
    ):
        self.source = source
        self.category = category
        self.text = text
        self.features = features

    def __repr__(self):
        return f'{self.features}\n' \
               f'{self.text}\n' \
               f'{self.source}\n'
