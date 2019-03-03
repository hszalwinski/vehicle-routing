import csv
import json
import pickle

from pathlib import Path


def load_from_pickle_file(path: str):
    path = Path(path)
    with path.open('rb') as f:
        return pickle.load(f)


def load_from_json_file(path: str):
    path = Path(path)
    with path.open('rb') as f:
        file_content = f.read()
        return json.loads(file_content)


def save_to_pickle_file(path: str, content):
    path = Path(path)
    with path.open('wb') as f:
        pickle.dump(content, f)


def save_to_csv_file(path: str, header: list, rows: list):
    path = Path(path)
    with path.open('w', newline='', encoding='UTF-8') as f:
        csv_writer = csv.writer(f, delimiter=',')
        csv_writer.writerow(header)
        for row in rows:
            csv_writer.writerow(row)
