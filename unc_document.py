"""
This module defines a Document object
which contains the features and the label
of an actual text document.


(C) 2020 Urdu News Clustering
"""

from unc_preprocessing import extract_features


class Document:
    def __init__(
            self,
            source: str,
            category: str,
            text: str
    ):
        self.source = source
        self.category = category
        self.text = text
        self.features = extract_features(text)
