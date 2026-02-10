from enum import Enum
from typing import Annotated

import typer

from . import __version__
from . import dump_gis
from . import fetch_gis
from . import forecast as forecast_mod
from . import knobs
from . import output
from . import settings
from . import visualize

app = typer.Typer(
    help="Retrieve weather data from the Australian Bureau of Meteorology",
    invoke_without_command=True,
)
spatial_app = typer.Typer(help="Spatial database management")
app.add_typer(spatial_app, name="spatial")


def _version_callback(value: bool) -> None:
    if value:
        print(f"bomshell {__version__}")
        raise typer.Exit()


# Build dynamic enums from runtime data
GisType = Enum("GisType", {t: t for t in fetch_gis.get_gis_types()})
VizType = Enum("VizType", {t: t for t in visualize.get_visualizable_types()})


@app.callback()
def app_callback(
    ctx: typer.Context,
    version: Annotated[
        bool | None,
        typer.Option("--version", callback=_version_callback, is_eager=True, help="Show version and exit."),
    ] = None,
    verbose: Annotated[int, typer.Option("-v", "--verbose", count=True, help="Level of verbosity of logs")] = 0,
    cache_path: Annotated[str, typer.Option("-c", "--cache-path", help=f"BOM data cache path, Default: {settings.CACHE}")] = settings.CACHE,
    json: Annotated[bool, typer.Option("--json", help="Emit JSON output (for widgets / scripting)")] = False,
) -> None:
    settings.VERBOSE = verbose
    settings.CACHE = cache_path
    output.set_json_mode(json)
    if ctx.invoked_subcommand is None:
        ctx.invoke(forecast)


@app.command()
def knobs_cmd() -> None:
    """Print all known settings and their current defaults."""
    if output.is_json_mode():
        output.emit_json(dict(knobs.register))
    else:
        output.print_info(knobs.get_knob_defaults())


# Register the command under the name "knobs"
knobs_cmd.__name__ = "knobs"


@app.command()
def forecast(
    town: Annotated[str, typer.Argument(help="Town name to get forecast for")] = "Roleystone",
) -> None:
    """Show the 7-day weather forecast for a town."""
    try:
        locations = forecast_mod.search_location(town)
    except Exception as e:
        output.print_error(f"Error searching for '{town}': {e}")
        raise typer.Exit(1) from None

    if not locations:
        output.print_warning(f"No locations found for '{town}'")
        raise typer.Exit(1)

    if len(locations) > 1:
        output.print_cyan(f"Found {len(locations)} matches (using first):")
        for i, loc in enumerate(locations, 1):
            output.print_info(f"  {i}. {loc['name']}, {loc['state']} {loc['postcode']}")
        output.print_info("")

    location = locations[0]

    try:
        data = forecast_mod.get_daily_forecast(location["geohash"])
    except Exception as e:
        output.print_error(f"Error fetching forecast: {e}")
        raise typer.Exit(1) from None

    if output.is_json_mode():
        output.emit_json({"location": location, "forecast": data})
    else:
        output.print_info(forecast_mod.format_forecast(location, data))


@spatial_app.callback()
def spatial_callback(
    overwrite: Annotated[
        bool,
        typer.Option(
            "-o",
            "--overwrite/--no-overwrite",
            help=f"Overwrite existing spatial data, default is: {settings.OVERWRITE}",
        ),
    ] = settings.OVERWRITE,
    ftp_timeout: Annotated[
        int, typer.Option("--ftp-timeout", help=f"FTP Timeout, default is {settings.FTP_TIMEOUT}s")
    ] = settings.FTP_TIMEOUT,
) -> None:
    """Spatial database management."""
    settings.OVERWRITE = overwrite
    settings.FTP_TIMEOUT = ftp_timeout


@spatial_app.command()
def fetch() -> None:
    """Fetch spatial data."""
    fetch_gis.fetch_spatial_data()


@spatial_app.command()
def sync() -> None:
    """Sync the local spatial data, overwriting existing files."""
    settings.OVERWRITE = True
    fetch_gis.fetch_spatial_data()


@spatial_app.command()
def build() -> None:
    """Build the local spatial database."""
    fetch_gis.create_spatial_database()


@spatial_app.command()
def csvdump(
    spatial_type: Annotated[GisType | None, typer.Option("-s", "--spatial-type", help="choose a spatial type")] = None,
) -> None:
    """Dump spatial data to csv."""
    if spatial_type is None:
        output.print_warning("Select one of the spatial types:")
        for e in fetch_gis.get_gis_types():
            output.print_warning(f"--spatial-type {e}")
        raise typer.Exit()

    dump_gis.dump_to_csv(spatial_type.value)


@spatial_app.command()
def tabledump(
    spatial_type: Annotated[GisType | None, typer.Option("-s", "--spatial-type", help="choose a spatial type")] = None,
) -> None:
    """Dump spatial data to table."""
    if spatial_type is None:
        output.print_warning("Select one of the spatial types:")
        for e in fetch_gis.get_gis_types():
            output.print_warning(f"--spatial-type {e}")
        raise typer.Exit()

    dump_gis.dump_to_table(spatial_type.value)


@spatial_app.command("map")
def map_cmd(
    spatial_types: Annotated[
        list[VizType] | None,
        typer.Option("-s", "--spatial-type", help="spatial type(s) to visualize (can specify multiple)"),
    ] = None,
    output_path: Annotated[str | None, typer.Option("-o", "--output", help="output HTML file path")] = None,
    no_open: Annotated[bool, typer.Option("--no-open", help="don't open the map in a browser")] = False,
) -> None:
    """Generate an interactive map of spatial data.

    Combine multiple layers by specifying -s multiple times:

        bomshell spatial map -s forecast_districts -s radar_location
    """
    if not spatial_types:
        output.print_warning("Select one or more spatial types:")
        for t in visualize.get_visualizable_types():
            output.print_warning(f"  -s {t}")
        output.print_cyan("\nCombine layers: -s forecast_districts -s radar_location")
        raise typer.Exit()

    type_values = [t.value for t in spatial_types]

    try:
        result_path = visualize.create_map(type_values, output_path)
        output.print_success(f"Map saved to: {result_path}")
        if len(type_values) > 1:
            output.print_cyan("Use layer control (top-right) to toggle layers")
        if not no_open:
            visualize.open_in_browser(result_path)
    except FileNotFoundError as e:
        output.print_error(str(e))
        raise typer.Exit(1) from None


def main() -> None:
    app()
