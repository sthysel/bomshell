import sys

import click

from . import fetch_gis
from . import settings
from . import dump_gis


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
    settings.VERBOSE = verbose
    settings.CACHE = cache_path


@main.group('spatial')
@click.option('-o', '--overwrite/--no-overwrite',
              default=settings.OVERWRITE,
              help='Overwrite existing spatial data, default is: {}'.format(settings.OVERWRITE))
@bom_config
def spatial(config, overwrite):
    """ 
    Spatial database management
    """
    settings.OVERWRITE = overwrite


@spatial.command()
@bom_config
def fetch(config):
    """
    Fetch spatial data 
    """
    fetch_gis.fetch_spatial_data()


@spatial.command()
@bom_config
def sync(config):
    """
    Sync the local spatial data, overwriting existing files
    """
    settings.OVERWRITE = True
    fetch_gis.fetch_spatial_data()


@spatial.command()
@bom_config
def build(config):
    """
    Build the local spatial database
    """
    fetch_gis.create_spatial_database()


@spatial.command()
@click.option(
    '-s', '--spatial-type',
    type=click.Choice(fetch_gis.get_gis_types()),
    help='choose a spatial type from {}'.format(fetch_gis.get_gis_types()))
@bom_config
def csvdump(config, spatial_type):
    """
    Dump spatial data to csv 
    """
    if spatial_type is None:
        click.secho('Select one of the spatial types:', fg='yellow')
        for e in fetch_gis.get_gis_types():
            click.secho('--spatial-type {}'.format(e), fg='yellow')
        sys.exit()

    dump_gis.dump_to_csv(spatial_type)


@spatial.command()
@click.option(
    '-s', '--spatial-type',
    type=click.Choice(fetch_gis.get_gis_types()),
    help='choose a spatial type')
@click.option(
    '-f', '--table-format',
    type=click.Choice(dump_gis.get_table_formats()),
    help='choose a table type')
@bom_config
def tabledump(config, spatial_type, table_format):
    """
    Dump spatial data to table
    """
    if spatial_type is None:
        click.secho('Select one of the spatial types:', fg='yellow')
        for e in fetch_gis.get_gis_types():
            click.secho('--spatial-type {}'.format(e), fg='yellow')
        sys.exit()

    dump_gis.dump_to_table(spatial_type, table_format=table_format)
