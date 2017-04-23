import click

from . import settings
from . import spatial


class CookConfig:
    def __init__(self):
        pass


bom_config = click.make_pass_decorator(CookConfig, ensure=True)


@click.group()
@click.version_option(settings.__version__)
@click.option('-v', '--verbose', default=0, count=True, help='Level of verbosity of logs')
@click.option('-c', '--cache-path',
              default=settings.CACHE,
              type=click.Path(),
              help='BOM data cache path, Default: {}'.format(settings.CACHE))
@bom_config
def main(config, verbose, cache_path):
    """ 
    Retrieve weather data from the Australian Bureau of Meteorology
    """
    config.verbose = verbose
    settings.CACHE = cache_path


@main.command()
@bom_config
def update(config):
    """
    Update the local spatial database 
    """

    spatial.fetch_spatial_data()
