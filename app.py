"""
This file displays a GUI for clustering evaluation.


(C) 2020 Urdu News Clustering
"""

import PySimpleGUI as sg

from unc_clustering import get_similar_documents
from unc_filing import *
from unc_kmeans import evaluate_clustering


def display_clusters(documents: List[Document]):
    """
    Performs k means clustering and returns clusters as a str.

    :param documents: List of headlines
    :return: String containing the clusters and evaluation metrics
    """
    clusters: str = ''

    layout = [
        [sg.Text('Enter A Value For k', font=12),
         sg.Spin([idx for idx in range(2, 400)], initial_value=4, key='-K-', size=(6, 1))],
        [sg.Button('RUN K-MEANS', bind_return_key=True),
         sg.Checkbox(text='Save Results', key='-SAVE-')]
    ]
    event, values = sg.Window(title='IR Course Project',
                              layout=layout, margins=(20, 20)).read(close=True)

    if event == 'RUN K-MEANS':
        k = int(values['-K-'])

        purity, iterations, summary, results = evaluate_clustering(documents, k)
        print(summary)

        if values['-SAVE-'] is True:
            summary = summary.to_csv(index=False, sep='\t')
            clusters += f'{iterations} Iterations\n' \
                        f'{round(purity * 100, 2)}% Purity\n\n' \
                        f'{summary}'

            for cluster_id, documents in results.items():
                clusters += f'Cluster {cluster_id} has {len(documents)} headlines\n'
                for document in documents:
                    clusters += f'{document}\n'
                clusters += '\n'
            clusters += '\n'

        message = [f'{iterations} Iterations', f'{round(purity * 100, 2)}% Purity']
        sg.PopupAutoClose(*message, no_titlebar=True,
                          grab_anywhere=True, keep_on_top=True, font=('Helvetica', 12))

    return clusters


def display_similar_news(documents: List[Document], stopwords: Set[str]):
    """
    Applies Jackard Index to search for similar headlines and returns.

    :param documents: List of headlines
    :param stopwords: Set of stopwords to remove from features
    :return: String containing the similar documents
    """
    results: str = ''

    layout = [
        [sg.Text('Select A Headline (Double Click or Enter)', font=18, pad=(0, 16))],
        [sg.Listbox(values=documents, key='-HEADLINE-',
                    font=('Helvetica', 16), size=(64, 16),
                    bind_return_key=True, pad=(10, 10))],
        [sg.Text('Or Type In Your Own Headline', font=18)],
        [sg.InputText(key='-ENTERED-HEADLINE-', font=('Helvetica', 16)),
         sg.Checkbox(text='Save Results', key='-SAVE-')],
        [sg.Button(key='-ENTER-HEADLINE-', button_text=' SUBMIT ')],
    ]
    window = sg.Window(title='IR Course Project', layout=layout)

    while True:
        event, values = window.read()

        if event in (None, sg.WINDOW_CLOSED):
            break

        elif event == '-HEADLINE-':
            query_document: Document = values['-HEADLINE-'][0]

        elif event == '-ENTER-HEADLINE-':
            query_text: str = values['-ENTERED-HEADLINE-']
            features = extract_features(query_text, stopwords)
            query_document: Document = Document(text=query_text, features=features)

        similar_documents = get_similar_documents(query_document, documents)

        length = len(similar_documents)
        if values['-SAVE-'] is True:
            results += f'{length} Similar Headlines For:\n' \
                       f'{query_document.text} {query_document.category}\n'
            for idx, document in enumerate(similar_documents):
                results += f' {document.text} {document.category} {idx + 1}. \n'
            results += '\n'

        layout2 = [
            [sg.Text('Similar Headlines', font=24, pad=(10, 10))],
            [sg.Listbox(values=similar_documents, font=('Helvetica', 16),
                        size=(64, 8), pad=(10, 10))],
            [sg.Text(f'Number of documents: {length}')]
        ]

        sg.Window(title='IR Course Project', layout=layout2).read(close=True)

    window.close()
    return results


def display_app():
    """
    The main window that asks for dataset and stopwords.
    """
    sg.theme('DarkBlue')
    heading = 'اردو شہ سرخیوں کی جھنڈ بندی'
    image = r'newspaper.png'

    layout = [
        # Title and Icon
        [sg.Text(heading, font=('Helvetica', 20)), sg.Image(filename=image)],
        [sg.Text()],
        # Dataset folder input
        [sg.Button('Select the Dataset Folder', key='-FOLDER-BUTTON-', font=10, size=(24, 1)),
         sg.Text('No folder selected', key='-FOLDER-TEXT-', font=12, size=(36, 1))],
        # Stopwords file input
        [sg.Button('Select the Stopwords File', key='-FILE-BUTTON-', font=10, size=(24, 1)),
         sg.Text('No file selected', key='-FILE-TEXT-', font=12, size=(36, 1))],
        # Padding
        [sg.Text('_' * 84, pad=(0, 10))],
        # Read Button [Goes to next window]
        [
            sg.Button('Evaluate KMeans', button_color=('White', 'Teal'),
                      font=12, size=(20, 2), key='-KMEANS-'),
            sg.Button('Evaluate Jackard', button_color=('White', 'Teal'),
                      font=12, size=(20, 2), key='-JACK-')
        ]
    ]

    window = sg.Window(title='IR Course Project', layout=layout, resizable=True,
                       element_justification='center', margins=(20, 20))

    root_path, stop_path, results, clusters = None, None, '', ''

    while True:
        event, values = window.read()
        if event in (None, sg.WINDOW_CLOSED):

            if results not in (None, ''):
                store_results(results, r'results.txt')
            if clusters not in (None, ''):
                store_results(clusters, r'clusters.txt')
            break

        elif event == '-FOLDER-BUTTON-':
            root_path = sg.popup_get_folder('', no_window=True)
            if root_path not in (None, ''):
                window['-FOLDER-TEXT-'].update(root_path)

        elif event == '-FILE-BUTTON-':
            stop_path = sg.popup_get_file('', no_window=True,
                                          file_types=(('Text Files', '*.txt'),))
            if stop_path not in (None, ''):
                window['-FILE-TEXT-'].update(stop_path)

        elif event == '-JACK-':
            if (root_path in (None, '')) or (stop_path in (None, '')):
                continue
            stopwords = read_stopwords(stop_path)
            documents = read_headlines(root_path, stopwords)

            window.Hide()
            results += display_similar_news(documents, stopwords)
            window.UnHide()

        elif event == '-KMEANS-':
            if (root_path in (None, '')) or (stop_path in (None, '')):
                continue
            stopwords = read_stopwords(stop_path)
            documents = read_headlines(root_path, stopwords)

            window.Hide()
            clusters += display_clusters(documents)
            window.UnHide()

    window.close()


if __name__ == '__main__':
    display_app()
