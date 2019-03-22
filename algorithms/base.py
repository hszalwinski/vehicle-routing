import abc

from time import time
from typing import Sequence, Tuple
from pathlib import Path

from tools.file_operations import load_from_pickle_file, load_json_and_validate, save_to_csv_file, append_to_csv_file


class SolverException(Exception):
    pass


class BaseSolver(metaclass=abc.ABCMeta):
    CONFIGURATION_SCHEMA_PATH = Path('data', 'configuration_schema.json')
    VEHICLES_SCHEMA_PATH = Path('data', 'vehicles_schema.json')
    DEFAULT_OUTPUT_PATH = Path('data', 'results', 'default.csv')
    OUTPUT_HEADER = ['destinations_count', 'cost', 'execution_time', 'sequence']

    def __init__(self, distance_matrix_path: str, configuration_path: str, vehicles_path: str, output_path: str):
        distance_matrix = load_from_pickle_file(path=distance_matrix_path)

        self.destinations = distance_matrix['destination_addresses']
        self.destinations_count = len(self.destinations)
        self.sequence_len = self.destinations_count - 1  # Depot destination is outside of sequence
        self.sequence_max_index = self.destinations_count - 2

        self.distance_matrix = distance_matrix['matrix']
        self.distance_matrix_size = len(self.distance_matrix)
        if (self.distance_matrix_size < 2) or (self.destinations_count < 2):
            raise SolverException('Please provide at least 2 destinations in distance matrix.')

        self.configuration = load_json_and_validate(schema_path=self.CONFIGURATION_SCHEMA_PATH,
                                                    file_path=configuration_path)
        self.vehicles = load_json_and_validate(schema_path=self.VEHICLES_SCHEMA_PATH,
                                               file_path=vehicles_path)
        self.output_path = Path(output_path) if output_path else self.DEFAULT_OUTPUT_PATH

    def solve(self):
        start = time()
        sequence, sequence_cost = self._solve()
        end = time()
        execution_time = end - start

        self._print_results(sequence, sequence_cost, execution_time)
        self._save_results(sequence, sequence_cost, execution_time)

    @abc.abstractmethod
    def _solve(self) -> Tuple[Sequence, float]:
        pass

    def _arc_cost(self, from_node: int, to_node: int) -> float:
        return self.distance_matrix[from_node][to_node]

    def _get_sequence_cost(self, sequence: Sequence) -> float:
        cost = self._arc_cost(0, sequence[0])
        for i in range(0, len(sequence) - 1):
            cost += self._arc_cost(sequence[i], sequence[i + 1])
        cost += self._arc_cost(sequence[-1], 0)

        return cost

    def _print_results(self, sequence: Sequence, sequence_cost: float, execution_time: float) -> None:
        route = f'0  {self.destinations[0]} \n'
        for index in sequence:
            route += f'{index}  {self.destinations[index]} \n'
        route += f'0  {self.destinations[0]} \n'

        print("Route:\n" + route)
        print(f"Total distance: {sequence_cost} meters")
        print(f'Algorithm took {execution_time} seconds to perform.')

    def _save_results(self, sequence, sequence_cost, execution_time):
        row = (self.destinations_count, sequence_cost, f'{execution_time:.20f}', sequence)
        if self.output_path.exists():
            append_to_csv_file(self.output_path, rows=[row])
        else:
            save_to_csv_file(self.output_path, self.OUTPUT_HEADER, rows=[row])
