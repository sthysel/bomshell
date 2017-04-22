import click
from . import settings
import requests

class CookConfig:
    def __init__(self):
        pass


cook_config = click.make_pass_decorator(CookConfig, ensure=True)


@click.group()
@click.version_option(settings.__version__)
@click.option('-v', '--verbose', default=0, count=True, help='Level of verbosity of logs')
@click.option('-c', '--cache-path',
              default=settings.CACHE,
              type=click.Path(),
              help='Image cache path, Default: {}'.format(settings.CACHE))
@cook_config
@click.command()
def main(verbose, cache_path):
    """ 
    Retrieve weather data from the Australian Bureau of Meteorology'
    """

