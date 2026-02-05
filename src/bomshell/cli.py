import sys

import click

from . import __version__
from . import dump_gis
from . import fetch_gis
from . import knobs
from . import settings
from . import visualize


class CookConfig:
    def __init__(self):
        pass


bom_config = click.make_pass_decorator(CookConfig, ensure=True)


@click.group()
@click.version_option(__version__)
@click.option("-v", "--verbose", default=0, count=True, help="Level of verbosity of logs")
@click.option("-c", "--cache-path", default=settings.CACHE, type=click.Path(), help=f"BOM data cache path, Default: {settings.CACHE}")
@bom_config
def main(config, verbose, cache_path):
    """
    Retrieve weather data from the Australian Bureau of Meteorology
    """
    settings.VERBOSE = verbose
    settings.CACHE = cache_path


@main.command("knobs")
@bom_config
def print_knobs(config):
    """Print all known settings and their current defaults"""

    click.echo(knobs.get_knob_defaults())


@main.group("spatial")
@click.option(
    "-o",
    "--overwrite/--no-overwrite",
    default=settings.OVERWRITE,
    help=f"Overwrite existing spatial data, default is: {settings.OVERWRITE}",
)
@click.option("--ftp-timeout", default=settings.FTP_TIMEOUT, help=f"FTP Timeout, default is {settings.FTP_TIMEOUT}s")
@bom_config
def spatial(config, overwrite, ftp_timeout):
    """
    Spatial database management
    """
    settings.OVERWRITE = overwrite
    settings.FTP_TIMEOUT = ftp_timeout


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
    "-s", "--spatial-type", type=click.Choice(fetch_gis.get_gis_types()), help=f"choose a spatial type from {fetch_gis.get_gis_types()}"
)
@bom_config
def csvdump(config, spatial_type):
    """
    Dump spatial data to csv
    """
    if spatial_type is None:
        click.secho("Select one of the spatial types:", fg="yellow")
        for e in fetch_gis.get_gis_types():
            click.secho(f"--spatial-type {e}", fg="yellow")
        sys.exit()

    dump_gis.dump_to_csv(spatial_type)


@spatial.command()
@click.option("-s", "--spatial-type", type=click.Choice(fetch_gis.get_gis_types()), help="choose a spatial type")
@click.option("-f", "--table-format", type=click.Choice(dump_gis.get_table_formats()), help="choose a table type")
@bom_config
def tabledump(config, spatial_type, table_format):
    """
    Dump spatial data to table
    """
    if spatial_type is None:
        click.secho("Select one of the spatial types:", fg="yellow")
        for e in fetch_gis.get_gis_types():
            click.secho(f"--spatial-type {e}", fg="yellow")
        sys.exit()

    dump_gis.dump_to_table(spatial_type, table_format=table_format)


@spatial.command()
@click.option(
    "-s",
    "--spatial-type",
    type=click.Choice(visualize.get_visualizable_types()),
    help="choose a spatial type to visualize",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    help="output HTML file path (default: <spatial-type>.html)",
)
@click.option(
    "--no-open",
    is_flag=True,
    help="don't open the map in a browser",
)
@bom_config
def map(config, spatial_type, output, no_open):
    """
    Generate an interactive map of spatial data
    """
    if spatial_type is None:
        click.secho("Select one of the visualizable spatial types:", fg="yellow")
        for t in visualize.get_visualizable_types():
            click.secho(f"  --spatial-type {t}", fg="yellow")
        sys.exit()

    try:
        output_path = visualize.create_map(spatial_type, output)
        click.secho(f"Map saved to: {output_path}", fg="green")
        if not no_open:
            visualize.open_in_browser(output_path)
    except FileNotFoundError as e:
        click.secho(str(e), fg="red")
        sys.exit(1)
