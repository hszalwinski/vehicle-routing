import csv
import json
import pickle

from pathlib import Path
from typing import Union, Any, Iterable, List, Tuple, Sequence

from jsonschema import validate


def load_from_pickle_file(path: Union[Path, str]) -> Any:
    path = Path(path)
    with path.open('rb') as f:
        return pickle.load(f)


def load_from_json_file(path: Union[Path, str]) -> Any:
    path = Path(path)
    with path.open('rb') as f:
        file_content = f.read()
        return json.loads(file_content)


def load_json_and_validate(schema_path: Union[Path, str], file_path: Union[Path, str]) -> Any:
    schema = load_from_json_file(path=schema_path)
    data = load_from_json_file(path=file_path)
    validate(data, schema)

    return data


def save_to_pickle_file(path: Union[Path, str], content: Any) -> None:
    path = Path(path)
    with path.open('wb') as f:
        pickle.dump(content, f)


def save_to_csv_file(path: Union[Path, str], header: Iterable[Any], rows: Iterable[Any], delimiter: str = ';') -> None:
    path = Path(path)
    with path.open('w', newline='', encoding='UTF-8') as f:
        csv_writer = csv.writer(f, delimiter=delimiter)
        csv_writer.writerow(header)
        for row in rows:
            csv_writer.writerow(row)


def append_to_csv_file(path: Union[Path, str], rows: Iterable[Any], delimiter: str = ';') -> None:
    path = Path(path)
    with path.open('a', newline='', encoding='UTF-8') as f:
        csv_writer = csv.writer(f, delimiter=delimiter)
        for row in rows:
            csv_writer.writerow(row)


def load_csv_file(path: Union[Path, str], delimiter: str = ';') -> Tuple[Sequence[str], List[dict]]:
    path = Path(path)
    with path.open(mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=delimiter)
        return csv_reader.fieldnames, list(csv_reader)
