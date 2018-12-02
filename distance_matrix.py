import json
import pickle

from io import TextIOWrapper
from pathlib import Path

import googlemaps

from click.utils import LazyFile


def load_data_from_file(file):
    # type: (TextIOWrapper) -> dict

    file_content = file.read()
    return json.loads(file_content)


def extract_coordinates(data_dict):
    # type: (dict) -> list[tuple]

    locations = data_dict['specialRouteTasks']
    coordinates = []
    for location in locations:
        coordinates.append((location['latitude'], location['longitude']))

    return coordinates


def extract_raw_distance_matrix(distance_matrix):
    # type: (dict) -> list
    raw_distance_matrix = []

    for row in distance_matrix['rows']:
        raw_distance_matrix_row = []
        for element in row['elements']:
            raw_distance_matrix_row.append(element['distance']['value'])
        raw_distance_matrix.append(raw_distance_matrix_row)

    return raw_distance_matrix


def save_result_to_file(file, content):
    # type: (Path, object) -> None

    with file.open('wb') as f:
        pickle.dump(content, f)


def create_distance_matrix(input_file, output_file, app_key):
    # type: (TextIOWrapper, LazyFile, str) -> None

    gmaps = googlemaps.Client(key=app_key)
    data_dict = load_data_from_file(input_file)
    coordinates = extract_coordinates(data_dict)
    distance_matrix = gmaps.distance_matrix(coordinates, coordinates,
                                            mode='driving',
                                            units='metric',
                                            language='pl',
                                            region='pl')

    raw_distance_matrix = extract_raw_distance_matrix(distance_matrix)

    distance_matrix_file_content = {
        'destination_addresses': distance_matrix['destination_addresses'],
        'distance_matrix': raw_distance_matrix
    }

    distance_matrix_output_path = Path('data', 'distance_matrix', 'example_distance_matrix')
    save_result_to_file(distance_matrix_output_path, distance_matrix_file_content)
