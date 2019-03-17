import click

from algorithms.genetic import GeneticSolver
from algorithms.scan_all import ScanAllSolver
from algorithms.simulated_annealing import SimulatedAnnealingSolver
from algorithms.ortools_solution import OrtoolsSolver
from tools.distance_matrix import DistanceMatrixManager
from tools.timer import timer


@click.group()
def cli():
    """
    This CLI is an entrypoint for utilities and all simulations used to analyze
    different vehicle routing problem solutions.
    """


@cli.command()
@click.option('--app-key', '-a', envvar='APP_KEY', type=click.STRING, required=True)
@click.option('--locations-json', '-i', type=click.Path(exists=True, readable=True, resolve_path=True), required=True)
@click.option('--output-csv', '-oc', type=click.Path(writable=True, resolve_path=True), required=True)
@click.option('--output-pickle', '-op', type=click.Path(writable=True, resolve_path=True))
def distance_matrix(app_key, locations_json, output_csv, output_pickle):
    """
    Creates distance matrix files (CSV, pickle) from input JSONs using Google Distance Matrix API.
    """
    DistanceMatrixManager(app_key).create_distance_matrix(locations_json, output_csv, output_pickle)


@cli.command()
@click.option('--distance-matrix', '-d', type=click.Path(), required=True)
@click.option('--configuration', '-c', type=click.Path(), required=False)
@click.option('--vehicles', '-v', type=click.Path(), required=False)
@timer
def scan_all(distance_matrix, configuration, vehicles):
    """
    Solves VRP scanning all results.
    """
    ScanAllSolver(distance_matrix, configuration, vehicles).solve()


@cli.command()
@click.option('--distance-matrix', '-d', type=click.Path(), required=True)
@click.option('--configuration', '-c', type=click.Path(), required=False)
@click.option('--vehicles', '-v', type=click.Path(), required=False)
@timer
def ortools(distance_matrix, configuration, vehicles):
    """
    Solves VRP using Google ORTools algorithms.
    """
    OrtoolsSolver(distance_matrix, configuration, vehicles).solve()


@cli.command()
@click.option('--distance-matrix', '-d', type=click.Path(), required=True)
@click.option('--configuration', '-c', type=click.Path(), required=False)
@click.option('--vehicles', '-v', type=click.Path(), required=False)
@timer
def simulated_annealing(distance_matrix, configuration, vehicles):
    """
    Solves VRP using simulated annealing.
    """
    SimulatedAnnealingSolver(distance_matrix, configuration, vehicles).solve()


@cli.command()
@click.option('--distance-matrix', '-d', type=click.Path(), required=True)
@click.option('--configuration', '-c', type=click.Path(), required=False)
@click.option('--vehicles', '-v', type=click.Path(), required=False)
@timer
def genetic(distance_matrix, configuration, vehicles):
    """
    Solves VRP using genetic algorithm.
    """
    GeneticSolver(distance_matrix, configuration, vehicles).solve()


if __name__ == '__main__':
    cli()
