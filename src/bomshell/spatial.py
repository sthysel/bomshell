from . import settings
import click
from . import fetch

# spatial database directives, from here a single sqllite db is built
bom_source = {
    'forecast_districts': ('IDM00001', 'forecast districts'),
    'marine_zones': ('IDM00003', 'marine zones'),
    'rainfall_districts': ('IDM00004', 'rainfall districts'),
    'cyclone_areas': ('IDM00005', 'tropical cyclone service areas'),
    'high_sea_areas': ('IDM00006', 'high seas forecast areas'),
    'fire_districts': ('IDM00007', 'fire weather districts'),
    'point_places': ('IDM00013', 'point places (precis, fire, marine)'),
    'metros': ('IDM00014', 'metropolitan and other forecast areas)'),
    'ocean_wind_warning': ('IDM00015', 'ocean wind warning areas'),
    'radar_coverage': ('IDR00006', 'radar coverage'),
    'radar_location': ('IDR00007', 'radar location'),
}

ftp_server = 'ftp.bom.gov.au'
spatial_root = '/anon/home/adfd/spatial/'


def __fetch_file(file_name, file_extention='.dbf', cache=settings.SPATIAL_CACHE):
    """
    :param file_name: Fetch file
    """

    file_name = file_name + file_extention
    fetch.get_file(filename=file_name, directory=spatial_root, ftp_server=ftp_server)


def fetch_spatial_data(lookup_source=bom_source, cache=settings.SPATIAL_CACHE):
    """
    Fetches the spatial data from BOM 
    
    :param cache: Where to drop the file
    :param lookup_source: A lookup dict specifying where on BOM's site the lookups are
    """
    for name, (file_name, description) in lookup_source.items():
        click.echo('Fetching {}'.format(description))
        __fetch_file(file_name, cache=cache)


def create_spatial_database(destination=settings.SPATIAL_DB):
    """
    Create a SQL spatial database from the BOM lookups
    
    :param: destination 
    """
