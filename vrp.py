import click

from algorithms.genetic import GeneticSolver, SELECTION_METHODS, RANK_SELECTION_METHOD
from algorithms.scan_all import ScanAllSolver
from algorithms.simulated_annealing import SimulatedAnnealingSolver, DEFAULT_TEMPERATURE_FACTOR
from algorithms.ortools_solution import OrtoolsSolver
from distance_matrix import DistanceMatrixManager
from tools.timer import timer

ORTOOLS = 'ortools'
SIMULATED_ANNEALING = 'simulated_annealing'
GENETIC = 'genetic'
SCAN_ALL = 'scan_all'
TSP_ALGORITHMS = (ORTOOLS, SIMULATED_ANNEALING, GENETIC, SCAN_ALL)


@click.group()
def cli():
    """
    This CLI is an entrypoint for utilities and all simulations used to analyze
    different vehicle routing problem solutions.
    """


@cli.command()
@click.option('--app-key', '-a', envvar='APP_KEY', type=click.STRING, required=True)
@click.option('--input-json', '-i', type=click.Path(exists=True, readable=True, resolve_path=True), required=True)
@click.option('--output-csv', '-oc', type=click.Path(writable=True, resolve_path=True), required=True)
@click.option('--output-pickle', '-op', type=click.Path(writable=True, resolve_path=True))
def distance_matrix(app_key, input_json, output_csv, output_pickle):
    """
    Creates distance matrix files (CSV, pickle) from input JSONs using Google Distance Matrix API.
    Max matrix size: 10x10.
    """
    DistanceMatrixManager(app_key).create_distance_matrix(input_json, output_csv, output_pickle)


@cli.command()
@click.option('--distance-matrix', '-d', type=click.Path(), required=True)
@click.option('--algorithm', '-a', type=click.Choice(TSP_ALGORITHMS, case_sensitive=False),
              show_default=True, default=ORTOOLS)
@click.option('--iterations', '-i', type=click.IntRange(min=1, max=1_000_000_000), show_default=True, default=1_000)
@click.option('--temperature-factor', '-t', type=click.IntRange(min=1, max=1_000), required=False, show_default=True,
              default=DEFAULT_TEMPERATURE_FACTOR)
@click.option('--population-size', '-p', type=click.IntRange(min=5, max=1_000), show_default=True, default=100)
@click.option('--selection-method', '-s', type=click.Choice(SELECTION_METHODS, case_sensitive=False),
              show_default=True, default=RANK_SELECTION_METHOD)
@timer
def tsp(distance_matrix, algorithm, iterations, temperature_factor, population_size, selection_method):
    """
    Solves a Travelling Salesman Problem represented by distance matrix.
    """
    if algorithm == ORTOOLS:
        solver = OrtoolsSolver(distance_matrix, routes_to_find=1)
    elif algorithm == SIMULATED_ANNEALING:
        solver = SimulatedAnnealingSolver(distance_matrix,
                                          routes_to_find=1,
                                          temperature_factor=temperature_factor,
                                          iterations_count=iterations)
    elif algorithm == GENETIC:
        solver = GeneticSolver(distance_matrix,
                               routes_to_find=1,
                               population_size=population_size,
                               iterations_count=iterations,
                               selection_method=selection_method)
    elif algorithm == SCAN_ALL:
        solver = ScanAllSolver(distance_matrix, routes_to_find=1)
    else:
        click.echo('Algorithm not supported.')
        return

    solver.solve()


if __name__ == '__main__':
    cli()
