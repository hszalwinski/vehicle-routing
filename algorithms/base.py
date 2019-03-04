import abc
from typing import Union
from pathlib import Path

from tools.file_operations import load_from_pickle_file, load_json_and_validate


class BaseSolverException(Exception):
    pass


class BaseSolver(metaclass=abc.ABCMeta):
    CONFIGURATION_SCHEMA_PATH = Path('data', 'configuration_schema.json')
    VEHICLES_SCHEMA_PATH = Path('data', 'vehicles_schema.json')

    def __init__(self, distance_matrix_path, configuration_path, vehicles_path):
        distance_matrix = load_from_pickle_file(path=distance_matrix_path)

        self.destinations = distance_matrix['destination_addresses']
        self.distance_matrix = distance_matrix['matrix']

        self.destinations_count = len(self.destinations)
        self.distance_matrix_size = len(self.distance_matrix)
        if (self.distance_matrix_size < 2) or (self.destinations_count < 2):
            raise BaseSolverException('Please provide at least 2 destinations in distance matrix.')

        self.configuration = load_json_and_validate(schema_path=self.CONFIGURATION_SCHEMA_PATH,
                                                    file_path=configuration_path)
        self.vehicles = load_json_and_validate(schema_path=self.VEHICLES_SCHEMA_PATH,
                                               file_path=vehicles_path)

    @abc.abstractmethod
    def solve(self):
        pass

    def _arc_cost(self, from_node: int, to_node: int) -> float:
        return int(self.distance_matrix[from_node][to_node])

    def _get_sequence_cost(self, sequence: Union[tuple, list]) -> float:
        sequence = self._update_sequence_with_depot_node(sequence)
        cost = 0
        for i in range(0, len(sequence) - 1):
            cost += self._arc_cost(sequence[i], sequence[i + 1])

        return cost

    def _print_results(self, sequence: Union[tuple, list], cost: float) -> None:
        sequence = self._update_sequence_with_depot_node(sequence)
        route = ''
        for index in sequence:
            route += f'{index}  {self.destinations[index]} \n'
        print("Route:\n" + route)
        print(f"Total distance: {cost} meters")

    @staticmethod
    def _update_sequence_with_depot_node(sequence: Union[tuple, list]) -> Union[tuple, list]:
        if type(sequence) is tuple:
            sequence = (0,) + sequence + (0,)
        else:
            sequence = [0] + sequence + [0]

        return sequence
