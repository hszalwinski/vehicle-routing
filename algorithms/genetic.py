from sys import maxsize as max_integer_size
from random import sample, shuffle, randint
from typing import List, Tuple

from ordered_set import OrderedSet
from algorithms.base import BaseSolver


class GeneticSolver(BaseSolver):
    def __init__(self, distance_matrix_path: str, configuration_path: str, vehicles_path: str):
        super(GeneticSolver, self).__init__(distance_matrix_path, configuration_path, vehicles_path)
        conf = self.configuration['genetic']
        self._iterations_count = conf['iterations_count']
        self._population_size = conf['population_size']
        self._max_population_index = self._population_size - 1

        self._elite_count = int(self.sequence_len * conf['elite_sequences_ratio'])
        if self._elite_count == 0:
            self._elite_count = 1
        self._tournament_groups_count = int(self._population_size / conf['tournament_group_size'])
        self._mutated_sequences_per_population = int(self._population_size * conf['mutated_sequences_ratio'])
        self._pmx_crossing_size = int(self.sequence_max_index * conf['pmx_crossing_ratio'])

        self._population = self._generate_initial_population()
        self._best_sequence = None
        self._best_sequence_cost = max_integer_size

    def solve(self):
        for _ in range(0, self._iterations_count):
            population_with_costs = self._get_population_with_costs()
            elite_sequences, best_sequence_cost = self._select_elites(population_with_costs)
            if best_sequence_cost < self._best_sequence_cost:
                self._best_sequence = elite_sequences[0]
                self._best_sequence_cost = best_sequence_cost
            new_population = self._perform_tournament_selection(elite_sequences, population_with_costs)
            new_population = self._perform_crossing(new_population)
            self._population = self._mutate_population(new_population)

        self._print_results(self._best_sequence, self._best_sequence_cost)

    def _generate_initial_population(self) -> List[List[int]]:
        basic_sequence = list(range(1, len(self.destinations)))
        population = [basic_sequence] * self._population_size

        for i in range(0, len(population)):
            population[i] = sample(population[i], k=len(self.destinations) - 1)

        return population

    def _get_population_with_costs(self) -> List[Tuple[float, List[int]]]:
        population_with_costs = []
        for sequence in self._population:
            population_with_costs.append(
                (self._get_sequence_cost(sequence), sequence)
            )

        return population_with_costs

    def _select_elites(self, population_with_costs: List[Tuple[float, List[int]]]) -> Tuple[List[List[int]], float]:
        sorted_population = sorted(population_with_costs)
        elites = [sorted_population[i][1] for i in range(0, self._elite_count)]
        best_sequence_cost = sorted_population[0][0]

        return elites, best_sequence_cost

    def _perform_tournament_selection(self, selected_sequences: List[List[int]],
                                      population_with_costs: List[Tuple[float, List[int]]]) -> List[List[int]]:
        while True:
            shuffle(population_with_costs)
            tournament_groups = [population_with_costs[i::self._tournament_groups_count]
                                 for i in range(self._tournament_groups_count)]
            for group in tournament_groups:
                best_sequence_in_group = sorted(group)[0]
                selected_sequences.append(best_sequence_in_group[1])
                if len(selected_sequences) == self._population_size:
                    return selected_sequences

    def _perform_crossing(self, population: List[List[int]]) -> List[List[int]]:
        shuffle(population)
        for i in range(0, len(population), 2):
            population[i], population[i + 1] = self._pmx_crossing(population[i], population[i + 1])

        return population

    def _pmx_crossing(self, sequence_a: List[int], sequence_b: List[int]) -> Tuple[List[int], List[int]]:
        start_index = randint(0, self.sequence_max_index - self._pmx_crossing_size)
        end_index = start_index + self._pmx_crossing_size

        part_from_a = OrderedSet(sequence_a[start_index:end_index])
        part_from_b = OrderedSet(sequence_b[start_index:end_index])
        os_sequence_a = OrderedSet(sequence_a)
        os_sequence_b = OrderedSet(sequence_b)

        new_sequence_1 = self._get_pmx_crossed_sequence(os_sequence_a, os_sequence_b,
                                                        part_from_a, part_from_b,
                                                        start_index, end_index)
        new_sequence_2 = self._get_pmx_crossed_sequence(os_sequence_b, os_sequence_a,
                                                        part_from_b, part_from_a,
                                                        start_index, end_index)
        return new_sequence_1, new_sequence_2

    @staticmethod
    def _get_pmx_crossed_sequence(sequence_a: OrderedSet, sequence_b: OrderedSet,
                                  part_from_a: OrderedSet, part_from_b: OrderedSet,
                                  start_index: int, end_index: int) -> List[int]:
        """
        Returns a sequence, which base is from 'sequence_b' and 'part_from_a' is copied in
        """
        new_sequence = list(sequence_b)

        elements_requiring_correction = {}

        uniques_from_b_part = part_from_b - part_from_a
        for unique_from_b_part in uniques_from_b_part:
            index_in_part = part_from_b.index(unique_from_b_part)
            elements_requiring_correction[unique_from_b_part] = part_from_a[index_in_part]

        for elem_from_b, elem_from_a in elements_requiring_correction.items():
            while elem_from_a in part_from_b:
                index_of_elem_from_b = sequence_b.index(elem_from_a)
                elem_from_a = sequence_a[index_of_elem_from_b]

            new_index = sequence_b.index(elem_from_a)
            new_sequence[new_index] = elem_from_b

        new_sequence[start_index:end_index] = part_from_a

        sequence_set = set(new_sequence)
        if len(new_sequence) != len(sequence_set):
            print(new_sequence)
            print(sequence_set)
        return new_sequence

    def _mutate_population(self, population: List[List[int]]) -> List[List[int]]:
        sequence_ids_to_mutate = [
            randint(0, self._population_size - 1) for _ in range(0, self._mutated_sequences_per_population)
        ]
        for sequence_id in sequence_ids_to_mutate:
            population[sequence_id] = self._mutate_by_inversion(population[sequence_id])

        return population

    def _mutate_by_inversion(self, sequence: List[int]) -> List[int]:
        index_a = randint(0, self.sequence_max_index)
        index_b = randint(0, self.sequence_max_index)

        if index_a <= index_b:
            sequence[index_a:index_b] = reversed(sequence[index_a:index_b])
        else:
            sequence[index_b:index_a] = reversed(sequence[index_b:index_a])

        return sequence
