"""
This file defines filing methods for storing, loading,
and traversing files and folders.


(C) 2020 Urdu News Clustering
"""

import os

from unc_document import Document


def read_headlines(root_path: str):
    """
    Reads headlines from `root_path` and returns a dict.
    Folders one level below are considered the source labels.
    Folders two levels below are considered the category labels.
    .doc files three levels below are considered as headlines.

    :param root_path: Folder directory of dataset
    :return: Dictionary containing the headlines
    """
    documents = []

    source_folders = next(os.walk(root_path, '.'))[1]

    for source_folder in source_folders:
        category_folders = next(os.walk(os.path.join(root_path, source_folder)))[1]

        for category_folder in category_folders:
            headlines = next(
                os.walk(
                    os.path.join(
                        os.path.join(root_path, source_folder),
                        category_folder
                    )
                )
            )[2]
            # remove file extensions (something.doc -> something)
            headlines = [headline[:headline.rfind(".")] for headline in headlines]

            for headline in headlines:
                documents.append(Document(source_folder, category_folder, headline))

    documents = {idx: document for idx, document in enumerate(documents)}
    return documents


documents = read_headlines(r'dataset')
# incidence = {idx: {term: True for term in document.features} for idx, document in documents.items()}
#
#
# incidence_matrix = pd.DataFrame.from_dict(data=incidence, orient='index', dtype=bool)
# incidence_matrix.fillna(False, inplace=True)
# print(incidence_matrix.dtypes)
# # incidence_matrix.to_csv('incide.csv')