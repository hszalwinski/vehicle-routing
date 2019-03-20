import pytest

from ordered_set import OrderedSet
from mock import Mock

from algorithms.genetic import GeneticSolver

SEQUENCE_LEN = 9
SELECTED_SEQUENCES = [[1, 6, 8, 9, 7, 2, 4, 3, 5]]
BEST_SEQUENCE_COST = 88485
POPULATION_WITH_COSTS = [(120810, [2, 8, 6, 7, 4, 1, 5, 3, 9]), (BEST_SEQUENCE_COST, [1, 2, 6, 5, 7, 3, 9, 4, 8]),
                         (123601, [3, 2, 6, 7, 8, 1, 5, 4, 9]), (130978, [3, 8, 6, 4, 1, 9, 5, 7, 2]),
                         (129104, [9, 1, 4, 7, 5, 8, 3, 6, 2]), (118470, [3, 8, 2, 5, 9, 1, 7, 4, 6]),
                         (122043, [7, 4, 8, 5, 6, 3, 9, 1, 2]), (121635, [3, 5, 1, 4, 8, 7, 6, 9, 2]),
                         (111556, [9, 2, 3, 1, 5, 7, 8, 4, 6]), (103951, [5, 1, 6, 4, 3, 8, 2, 9, 7])]
ELITE_SEQUENCES = [[1, 2, 6, 5, 7, 3, 9, 4, 8], [5, 1, 6, 4, 3, 8, 2, 9, 7], [9, 2, 3, 1, 5, 7, 8, 4, 6],
                   [3, 8, 2, 5, 9, 1, 7, 4, 6], [2, 8, 6, 7, 4, 1, 5, 3, 9]]


@pytest.fixture
def genetic_solver():
    solver = GeneticSolver
    solver.__init__ = Mock()
    solver.__init__.return_value = None
    solver = solver()
    solver._tournament_groups_count = 3
    solver._population_size = 10
    solver._elite_count = 5
    solver.sequence_max_index = 8

    return solver


def test_select_elites(genetic_solver):
    elites, best_cost = genetic_solver._select_elites(POPULATION_WITH_COSTS)

    assert elites == ELITE_SEQUENCES
    assert BEST_SEQUENCE_COST == 88485


def test_perform_tournament_selection(genetic_solver):
    result = genetic_solver._perform_tournament_selection(SELECTED_SEQUENCES, POPULATION_WITH_COSTS)

    assert len(result) == 10
    assert result[0] == SELECTED_SEQUENCES[0]

    for sequence in result:
        assert len(sequence) == SEQUENCE_LEN
        assert len(set(sequence)) == SEQUENCE_LEN


sequence_1a = OrderedSet([1, 2, 3, 4, 5, 6, 7, 8, 9])
sequence_1b = OrderedSet([9, 3, 7, 8, 2, 6, 5, 1, 4])
sequence_2a = OrderedSet([7, 9, 5, 2, 8, 6, 4, 3, 1])
sequence_2b = OrderedSet([3, 7, 6, 9, 5, 2, 8, 4, 1])
sequence_3a = OrderedSet([4, 3, 6, 8, 7, 9, 5, 2, 1])  # multiple repeats example
sequence_3b = OrderedSet([9, 3, 7, 6, 5, 2, 4, 8, 1])


@pytest.mark.parametrize('sequence_a, sequence_b, start_index, end_index, expected_result', [
    (sequence_1a, sequence_1b, 3, 7, [9, 3, 2, 4, 5, 6, 7, 1, 8]),
    (sequence_1b, sequence_1a, 3, 7, [1, 7, 3, 8, 2, 6, 5, 4, 9]),
    (sequence_2a, sequence_2b, 0, 3, [7, 9, 5, 3, 6, 2, 8, 4, 1]),
    (sequence_2b, sequence_2a, 0, 3, [3, 7, 6, 2, 8, 5, 4, 9, 1]),
    (sequence_3a, sequence_3b, 2, 5, [9, 3, 6, 8, 7, 2, 4, 5, 1]),
    (sequence_3b, sequence_3a, 2, 5, [4, 3, 7, 6, 5, 9, 8, 2, 1]),
])
def test_get_pmx_crossed_sequence(sequence_a, sequence_b, start_index, end_index, expected_result):
    part_from_a = OrderedSet(sequence_a[start_index:end_index])
    part_from_b = OrderedSet(sequence_b[start_index:end_index])

    result_sequence = GeneticSolver._get_pmx_crossed_sequence(sequence_a, sequence_b,
                                                              part_from_a, part_from_b,
                                                              start_index, end_index)

    assert result_sequence == expected_result
