import json
import pickle
import csv

from pathlib import Path
from jsonschema import validate

import googlemaps


class DistanceMatrixManager:
    INPUT_DATA_SCHEMA_PATH = Path('data', 'input_data_schema.json')

    def __init__(self, app_key):
        self.gmaps = googlemaps.Client(key=app_key)

    def create_distance_matrix(self, input_json, output_csv, output_pickle=None):
        # type: (str, str, str or None) -> None

        schema = self.load_data_from_file(path=self.INPUT_DATA_SCHEMA_PATH)
        data_dict = self.load_data_from_file(path=input_json)
        validate(data_dict, schema)

        coordinates = self.extract_coordinates(data_dict)
        distance_matrix = self._compose_distance_matrix(coordinates)
        raw_distance_matrix = self._extract_raw_distance_matrix(distance_matrix)

        self.save_result_to_csv_file(path=output_csv,
                                     header=distance_matrix['destination_addresses'],
                                     rows=raw_distance_matrix)

        if output_pickle:
            pickle_file_content = {
                'destination_addresses': distance_matrix['destination_addresses'],
                'matrix': raw_distance_matrix
            }
            self.save_result_to_pickle_file(path=output_pickle, content=pickle_file_content)

    def _compose_distance_matrix(self, coordinates):
        # type: (list[tuple]) -> dict
        if len(coordinates) <= 10:
            return self.gmaps.distance_matrix(coordinates[:2], coordinates[2:],
                                              mode='driving',
                                              units='metric',
                                              language='pl',
                                              region='pl')

    @staticmethod
    def load_data_from_file(path):
        # type: (str) -> dict

        path = Path(path)
        with path.open('rb') as f:
            file_content = f.read()
            return json.loads(file_content)

    @staticmethod
    def extract_coordinates(data_dict):
        # type: (dict) -> list[tuple]

        locations = data_dict['locations']
        coordinates = []
        for location in locations:
            coordinates.append((location['latitude'], location['longitude']))

        return coordinates

    @staticmethod
    def _extract_raw_distance_matrix(distance_matrix):
        # type: (dict) -> list
        raw_distance_matrix = []

        for row in distance_matrix['rows']:
            raw_distance_matrix_row = []
            for element in row['elements']:
                raw_distance_matrix_row.append(element['distance']['value'])
            raw_distance_matrix.append(raw_distance_matrix_row)

        return raw_distance_matrix

    @staticmethod
    def save_result_to_csv_file(path, header, rows):
        # type: (str, list, list) -> None

        path = Path(path)
        with path.open('w', newline='', encoding='UTF-8') as f:
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerow(header)
            for row in rows:
                csv_writer.writerow(row)

    @staticmethod
    def save_result_to_pickle_file(path, content):
        # type: (str, dict) -> None

        path = Path(path)
        with path.open('wb') as f:
            pickle.dump(content, f)

    @staticmethod
    def load_distance_matrix_from_pickle_file(path):
        # type: (str) -> dict

        path = Path(path)
        with path.open('rb') as f:
            return pickle.load(f)
