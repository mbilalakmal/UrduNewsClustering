"""
This file defines filing methods for storing, loading,
and traversing files and folders.


(C) 2020 Urdu News Clustering
"""

import os
from typing import Set, Optional, List

from unc_document import Document
from unc_preprocessing import extract_features


def read_stopwords(file_path: str):
    with open(file_path, mode='r', encoding='utf-8') as file:
        stopwords = set(file.read().split())
    return stopwords


def read_headlines(root_path: str, stopwords: Optional[Set[str]]):
    """
    Reads headlines from `root_path` and returns a dict.
    Folders one level below are considered the source labels.
    Folders two levels below are considered the category labels.
    .doc files three levels below are considered as headlines.

    :param stopwords: Set of stop words
    :param root_path: Folder directory of dataset
    :return: List of Documents
    """
    documents: List[Document] = []

    # get source names [bbc dataset etc]
    source_folders = next(os.walk(root_path))[1]

    for source_folder in source_folders:
        # get category label [sports etc]
        category_folders = next(os.walk(os.path.join(root_path, source_folder)))[1]

        for category_folder in category_folders:
            # get individual headlines
            headlines = next(
                os.walk(
                    os.path.join(
                        os.path.join(root_path, source_folder), category_folder
                    )
                )
            )[2]

            # remove file extensions (something.doc -> something)
            headlines = [headline[:headline.rfind(".")] for headline in headlines]

            # Create document object from each headline
            for headline in headlines:
                features = extract_features(headline, stopwords)
                document = Document(
                    text=headline, features=features,
                    source=source_folder, category=category_folder
                )
                documents.append(document)

    return documents
