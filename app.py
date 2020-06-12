"""
This file displays a GUI for clustering evaluation.

The first window asks fro the dataset folder and the stopwords file.
The second window asks for a query headline and whether to save results.
The third window displays the headlines similar to the query headline.


(C) 2020 Urdu News Clustering
"""

import PySimpleGUI as sg

from unc_clustering import get_similar_documents
from unc_filing import *

sg.theme('DarkBlue')

layout = [[
    sg.Text('اردو خبروں کی جھنڈ بندی', font=('Helvetica', 21), tooltip='Sorting of Urdu news'),
    sg.Image(filename=r'newspaper.png')
]]
layout += [[sg.Text()]]

layout += [[sg.Button(
    'Select The Dataset Folder',
    key='-FOLDER-BUTTON-',
    size=(26, 2),
    font=12,
),
    sg.Text(
        ' No folder selected',
        key='-FOLDER-TEXT-',
        font=('Helvetica', 12),
        size=(36, 1),
    )]]
layout += [[sg.Button(
    'Select The Stopwords File',
    key='-FILE-BUTTON-',
    size=(26, 2),
    font=12,
),
    sg.Text(
        ' No file selected'.ljust(64),
        key='-FILE-TEXT-',
        font=('Helvetica', 12),
        size=(36, 1),
    )]]

layout += [[sg.Text('_'*70, pad=(0, 10))]]

layout += [[sg.Button(
    'PROCESS DATASET',
    key='-READ-',
    button_color=('White', 'Teal'),
    font=('Helvetica', 12),
    size=(20, 2)
)]]

window = sg.Window(
    title='IR Course Project', layout=layout,
    resizable=True, element_justification='center',
    margins=(20, 20)
)

stop_path = root_path = None
results = ''

while True:
    event, values = window.read()
    if event is None:
        # write results to file here
        if results != '':
            store_results(results)
        break

    elif event == '-FOLDER-BUTTON-':
        # add dataset folder
        root_path = sg.popup_get_folder('', no_window=True)
        if root_path not in (None, ''):
            window['-FOLDER-TEXT-'].update(root_path)

    elif event == '-FILE-BUTTON-':
        # add stopwords txt file
        stop_path = sg.popup_get_file(
            '', no_window=True,
            file_types=(('Text Files', '*.txt'),)
        )
        if stop_path not in (None, ''):
            window['-FILE-TEXT-'].update(stop_path)

    elif event == '-READ-':
        # read stopwords & documents
        if (root_path in (None, '')) or (stop_path in (None, '')):
            continue
        stopwords = read_stopwords(stop_path)
        documents = read_headlines(root_path, stopwords)

        # open new window with all documents in a listbox?
        layout2 = [
            [sg.Text('Select A News Headline (Double Click or Enter)', font=18, pad=(0, 16))],
            [sg.Listbox(
                values=documents, key='-HEADLINE-',
                size=(72, 16), font=30,
                bind_return_key=True,
            )],
            [sg.Text()],
            [sg.Text('OR Enter Your Own', font=18)],
            [sg.InputText(key='-ENTERED-HEADLINE-'),
             sg.Checkbox(text='Save Results', key='-SAVE-',
                         tooltip='If checked, results will be saved to results.txt')
             ],
            [sg.Button(key='-ENTER-HEADLINE-', button_text=' SUBMIT ')],
            [sg.Text()],
        ]

        event2, values2 = sg.Window(title='IR Course Project', layout=layout2).read(close=True)

        if event2 is None:
            continue

        elif event2 == '-HEADLINE-':
            # user selected a headline
            query_document: Document = values2['-HEADLINE-'][0]

        elif event2 == '-ENTER-HEADLINE-':
            # user entered their own headline
            query_text = values2['-ENTERED-HEADLINE-']
            query_document: Document = Document(
                text=query_text,
                features=extract_features(query_text, stopwords)
            )

        result_documents = get_similar_documents(query_document, documents)

        if values2['-SAVE-'] is True:
            results += f'{len(result_documents)} Similar Headlines For:\n'
            results += f'{query_document.text} {query_document.category}\n\n'
            for doc in result_documents:
                results += f'{doc.text} {doc.category}\n'
            results += '\n'

        layout3 = [
            [sg.Text()],
            [sg.Text('Similar Articles', font=26)],
            [sg.Text()],
            [sg.Listbox(
                values=result_documents,
                size=(72, len(result_documents) + 2 if len(result_documents) < 12 else 10),
                font=60,
            )],
            [sg.Text()],
            [sg.Text(f'Number of documents: {len(result_documents)}')]
        ]
        sg.Window(title='IR Course Project', layout=layout3).read(close=True)

window.close()
