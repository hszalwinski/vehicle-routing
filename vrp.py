import click

from distance_matrix import create_distance_matrix


@click.group()
def cli():
    """
    This CLI is an entrypoint for utilities and all simulations used to analyze
    different vehicle routing problem solutions.
    """


@cli.command()
@click.option('--input-file', '-i', type=click.File('rb'), required=True)
@click.option('--output-file', '-o', type=click.File('wb'), required=True)   # ToDo: add not required pickle output file
@click.option('--app-key', '-a', envvar='APP_KEY', type=click.STRING, required=True)
def distance_matrix(input_file, output_file, app_key):
    """
    Creates a CSV and pickle distance matrix files from input JSONs using Google Distance Matrix API.
    """
    create_distance_matrix(input_file, output_file, app_key)    # ToDo: define schema for input data


if __name__ == '__main__':
    cli()
