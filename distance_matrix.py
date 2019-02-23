import json
import pickle
import csv
from pathlib import Path
from math import ceil
from numpy import zeros, vstack, hstack

import googlemaps
from jsonschema import validate


class DistanceMatrixManager:
    INPUT_DATA_SCHEMA_PATH = Path('data', 'input_data_schema.json')
    MAX_COORDINATES_SIZE_PER_REQUEST = 10

    def __init__(self, app_key):
        self.gmaps = googlemaps.Client(key=app_key)

    def create_distance_matrix(self, input_json: str, output_csv_path: str, output_pickle_path: str = None) -> None:

        schema = self.load_data_from_file(path=self.INPUT_DATA_SCHEMA_PATH)
        data_dict = self.load_data_from_file(path=input_json)
        validate(data_dict, schema)

        coordinates = self.extract_coordinates(data_dict)
        distance_matrix, destination_addresses = self._compose_distance_matrix(coordinates)

        self.save_result_to_csv_file(path=output_csv_path,
                                     header=destination_addresses,
                                     rows=distance_matrix)

        if output_pickle_path:
            pickle_file_content = {
                'destination_addresses': destination_addresses,
                'matrix': distance_matrix
            }
            self.save_result_to_pickle_file(path=output_pickle_path, content=pickle_file_content)

    def _compose_distance_matrix(self, coordinates: list[tuple]) -> (list, list):
        if len(coordinates) <= 10:
            distance_matrix_response = self.gmaps.distance_matrix(coordinates, coordinates,
                                                                  mode='driving',
                                                                  units='metric',
                                                                  language='pl',
                                                                  region='pl')
            distance_matrix = self._extract_raw_distance_matrix(distance_matrix_response)
            destination_addresses = distance_matrix_response['destination_addresses']

            return distance_matrix, destination_addresses

        # distance_matrix = zeros((len(coordinates), len(coordinates)))
        # parts_count = ceil(len(coordinates) / self.MAX_COORDINATES_SIZE_PER_REQUEST)
        # for o in range(0, parts_count):
        #     origins_from = o * self.MAX_COORDINATES_SIZE_PER_REQUEST
        #     origins_to = (o + 1) * self.MAX_COORDINATES_SIZE_PER_REQUEST
        #     origins = coordinates[origins_from:origins_to]
        #     for d in range(0, parts_count):
        #         destinations_from = d * self.MAX_COORDINATES_SIZE_PER_REQUEST
        #         destinations_to = (d + 1) * self.MAX_COORDINATES_SIZE_PER_REQUEST
        #         destinations = coordinates[destinations_from:destinations_to]
        #         distance_matrix_part = self.gmaps.distance_matrix(origins, destinations,
        #                                                           mode='driving',
        #                                                           units='metric',
        #                                                           language='pl',
        #                                                           region='pl')
        #         distance_matrix

    @staticmethod
    def load_data_from_file(path: str) -> dict:
        path = Path(path)
        with path.open('rb') as f:
            file_content = f.read()
            return json.loads(file_content)

    @staticmethod
    def extract_coordinates(data: dict) -> list[tuple]:
        locations = data['locations']
        coordinates = []
        for location in locations:
            coordinates.append((location['latitude'], location['longitude']))

        return coordinates

    @staticmethod
    def _extract_raw_distance_matrix(distance_matrix: dict) -> list:
        raw_distance_matrix = []

        for row in distance_matrix['rows']:
            raw_distance_matrix_row = []
            for element in row['elements']:
                raw_distance_matrix_row.append(element['distance']['value'])
            raw_distance_matrix.append(raw_distance_matrix_row)

        return raw_distance_matrix

    @staticmethod
    def save_result_to_csv_file(path: str, header: list, rows: list) -> None:
        path = Path(path)
        with path.open('w', newline='', encoding='UTF-8') as f:
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerow(header)
            for row in rows:
                csv_writer.writerow(row)

    @staticmethod
    def save_result_to_pickle_file(path: str, content: dict) -> None:
        path = Path(path)
        with path.open('wb') as f:
            pickle.dump(content, f)

    @staticmethod
    def load_distance_matrix_from_pickle_file(path: str) -> dict:
        path = Path(path)
        with path.open('rb') as f:
            return pickle.load(f)
