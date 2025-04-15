# data_stream.py

import pandas as pd
import requests
from io import BytesIO

DATASET_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"

'''
def download_dataset():
    print("Downloading dataset...")
    response = requests.get(DATASET_URL)
    if response.status_code != 200:
        raise Exception("Failed to download dataset.")
    return pd.read_excel(BytesIO(response.content))

def preprocess_data(df):
    # Clean and group by InvoiceNo
    df = df.dropna(subset=['InvoiceNo', 'Description'])  # remove missing
    df = df[df['Quantity'] > 0]  # only positive quantity
    df = df[df['InvoiceNo'].apply(lambda x: not str(x).startswith('C'))]  # remove canceled orders

    # Group items by Invoice
    transactions = df.groupby('InvoiceNo')['Description'].apply(list).tolist()
    return transactions
'''

def download_dataset():
    # Skipped for test mode
    return None

def preprocess_data(_):
    return [
        # Pane 1 (milk, bread, butter)
        ['milk', 'bread'],
        ['milk', 'bread'],
        ['milk', 'butter'],
        ['bread', 'butter'],
        ['milk', 'bread'],
        ['bread', 'butter'],
        ['milk', 'bread'],
        ['milk', 'butter'],
        ['milk', 'bread'],
        ['bread', 'butter'],

        # Pane 2 (milk, cereal, bread)
        ['milk', 'cereal'],
        ['bread', 'cereal'],
        ['milk', 'bread'],
        ['cereal', 'butter'],
        ['milk', 'cereal'],
        ['bread', 'butter'],
        ['cereal', 'bread'],
        ['milk', 'cereal'],
        ['milk', 'bread'],
        ['butter', 'cereal'],

        # Pane 3 (shift to coffee, cereal)
        ['coffee', 'cereal'],
        ['milk', 'coffee'],
        ['cereal', 'bread'],
        ['coffee', 'butter'],
        ['coffee', 'cereal'],
        ['coffee', 'milk'],
        ['bread', 'coffee'],
        ['cereal', 'coffee'],
        ['cereal', 'milk'],
        ['butter', 'coffee'],

        # Pane 4 (strong drift: juice, tea, snack)
        ['juice', 'tea'],
        ['snack', 'juice'],
        ['tea', 'juice'],
        ['snack', 'cereal'],
        ['tea', 'snack'],
        ['tea', 'coffee'],
        ['juice', 'coffee'],
        ['juice', 'snack'],
        ['coffee', 'snack'],
        ['tea', 'cereal'],

        # Pane 5 (new pattern: pen, notebook, eraser)
        ['pen', 'notebook'],
        ['notebook', 'eraser'],
        ['pen', 'eraser'],
        ['notebook', 'pencil'],
        ['stapler', 'paper'],
        ['pen', 'notebook'],
        ['eraser', 'paper'],
        ['pen', 'stapler'],
        ['notebook', 'pen'],
        ['notebook', 'paper']
    ]

def get_stream_panes(transactions, pane_size=500):
    """
    Yields transaction panes of given size
    """
    for i in range(0, len(transactions), pane_size):
        yield transactions[i:i + pane_size]

# Example of loading and streaming data

from data_stream import download_dataset, preprocess_data, get_stream_panes

df = download_dataset()
transactions = preprocess_data(df)

for i, pane in enumerate(get_stream_panes(transactions, pane_size=500)):
    print(f"Pane {i+1}: {len(pane)} transactions")
    if i == 1:
        break  # just preview first 2 panes
