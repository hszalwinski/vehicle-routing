import click

from algorithms.simulated_annealing import SimulatedAnnealingSolver
from distance_matrix import create_distance_matrix
from algorithms.ortools_solution import OrtoolsSolver

ORTOOLS = 'ortools'
SIMULATED_ANNEALING = 'simulated_annealing'
TSP_ALGORITHMS = (ORTOOLS, SIMULATED_ANNEALING)


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
    """
    create_distance_matrix(app_key, input_json, output_csv, output_pickle)  # ToDo: define schema for input data


@cli.command()
@click.option('--distance-matrix', '-d', type=click.Path(), required=True)
@click.option('--algorithm', '-a', type=click.Choice(TSP_ALGORITHMS, case_sensitive=False),
              show_default=True, default=ORTOOLS)
def tsp(distance_matrix, algorithm):
    """
    Solves a Travelling Salesman Problem represented by distance matrix.
    """
    if algorithm == ORTOOLS:
        solver = OrtoolsSolver(distance_matrix, depot=0, routes_to_find=1)
    else:
        solver = SimulatedAnnealingSolver(distance_matrix, depot=0, routes_to_find=1)
        click.echo('Algorithm not supported yet')
        return

    solver.solve()


if __name__ == '__main__':
    cli()
