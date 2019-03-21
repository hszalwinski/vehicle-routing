import abc

from typing import Sequence
from pathlib import Path

from tools.file_operations import load_from_pickle_file, load_json_and_validate


class BaseSolverException(Exception):
    pass


class BaseSolver(metaclass=abc.ABCMeta):
    CONFIGURATION_SCHEMA_PATH = Path('data', 'configuration_schema.json')
    VEHICLES_SCHEMA_PATH = Path('data', 'vehicles_schema.json')

    def __init__(self, distance_matrix_path: str, configuration_path: str, vehicles_path: str):
        distance_matrix = load_from_pickle_file(path=distance_matrix_path)

        self.destinations = distance_matrix['destination_addresses']
        self.destinations_count = len(self.destinations)
        self.sequence_len = self.destinations_count - 1  # Depot destination is outside of sequence
        self.sequence_max_index = self.destinations_count - 2

        self.distance_matrix = distance_matrix['matrix']
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
        return self.distance_matrix[from_node][to_node]

    def _get_sequence_cost(self, sequence: Sequence) -> float:
        cost = self._arc_cost(0, sequence[0])
        for i in range(0, len(sequence) - 1):
            cost += self._arc_cost(sequence[i], sequence[i + 1])
        cost += self._arc_cost(sequence[-1], 0)

        return cost

    def _print_results(self, sequence: Sequence, cost: float) -> None:
        route = f'0  {self.destinations[0]} \n'
        for index in sequence:
            route += f'{index}  {self.destinations[index]} \n'
        route += f'0  {self.destinations[0]} \n'

        print("Route:\n" + route)
        print(f"Total distance: {cost} meters")
