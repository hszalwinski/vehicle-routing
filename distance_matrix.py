from pathlib import Path
from math import ceil
from numpy import vstack, hstack, ndarray
from typing import Union

import googlemaps
from jsonschema import validate

from tools.file_operations import load_from_json_file, save_to_pickle_file, save_to_csv_file


class DistanceMatrixManager:
    INPUT_DATA_SCHEMA_PATH = Path('data', 'locations_schema.json')
    MAX_COORDINATES_SIZE_PER_REQUEST = 10

    def __init__(self, app_key):
        self.gmaps = googlemaps.Client(key=app_key)

    def create_distance_matrix(self, input_json: str, output_csv_path: str, output_pickle_path: str = None) -> None:

        schema = load_from_json_file(path=self.INPUT_DATA_SCHEMA_PATH)
        data_dict = load_from_json_file(path=input_json)
        validate(data_dict, schema)

        coordinates = self._extract_coordinates(data_dict)
        distance_matrix, destination_addresses = self._compose_distance_matrix(coordinates)

        save_to_csv_file(path=output_csv_path,
                         header=destination_addresses,
                         rows=distance_matrix)

        if output_pickle_path:
            pickle_file_content = {
                'destination_addresses': destination_addresses,
                'matrix': distance_matrix
            }
            save_to_pickle_file(path=output_pickle_path, content=pickle_file_content)

    @staticmethod
    def _extract_coordinates(data: dict) -> list:
        locations = data['locations']
        coordinates = []
        for location in locations:
            coordinates.append((location['latitude'], location['longitude']))

        return coordinates

    def _compose_distance_matrix(self, coordinates: list) -> (Union[list, ndarray], list):
        """
        In a simple case it just returns a result of Google Distance Matrix API call.
        The API has a limit - returning matrix of maximum size 10x10.
        For more than 10 destinations, this method performs multiple API calls and combines results into one matrix.

        :param coordinates:
        :return: Distance matrix and a list of destination addresses.
        """
        if len(coordinates) <= 10:
            return self._get_distance_matrix_from_gmaps(origins=coordinates, destinations=coordinates)

        distance_matrix = None
        destinations_addresses = []
        addresses_part = []

        parts_count = ceil(len(coordinates) / self.MAX_COORDINATES_SIZE_PER_REQUEST)
        for d in range(0, parts_count):
            destinations = self._get_coordinates_by_part_number(coordinates, part_number=d)
            matrix_vertical_part = None
            for o in range(0, parts_count):
                origins = self._get_coordinates_by_part_number(coordinates, part_number=o)
                matrix_atom_part, addresses_part = self._get_distance_matrix_from_gmaps(origins, destinations)
                matrix_vertical_part = self._stack_matrixes(matrix_vertical_part, matrix_atom_part, vstack)

            destinations_addresses += addresses_part
            distance_matrix = self._stack_matrixes(distance_matrix, matrix_vertical_part, hstack)

        return distance_matrix, destinations_addresses

    def _get_coordinates_by_part_number(self, coordinates: list, part_number: int) -> list:
        coordinates_from = part_number * self.MAX_COORDINATES_SIZE_PER_REQUEST
        coordinates_to = (part_number + 1) * self.MAX_COORDINATES_SIZE_PER_REQUEST

        return coordinates[coordinates_from:coordinates_to]

    def _get_distance_matrix_from_gmaps(self, origins: list, destinations: list) -> (Union[list, ndarray], list):
        distance_matrix_response = self.gmaps.distance_matrix(origins, destinations,
                                                              mode='driving',
                                                              units='metric',
                                                              language='pl',
                                                              region='pl')
        distance_matrix = self._extract_raw_distance_matrix(distance_matrix_response)
        destination_addresses = distance_matrix_response['destination_addresses']

        return distance_matrix, destination_addresses

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
    def _stack_matrixes(base_matrix: Union[None, ndarray],
                        new_matrix: Union[list, ndarray],
                        stack_function: Union[vstack, hstack]) -> ndarray:
        if base_matrix is None:
            return new_matrix
        else:
            return stack_function((base_matrix, new_matrix))
