import os
from xdg.BaseDirectory import xdg_cache_home

__version__ = '0.1.0'
NAME = 'bomshell'

sources = {
    'catalogs': 'ftp://ftp.bom.gov.au/anon/sample/catalogue/',
    'observations': 'ftp://ftp.bom.gov.au/anon/sample/catalogue/Observations/',
    'forecasts': 'ftp://ftp.bom.gov.au/anon/sample/catalogue/Forecasts/',
    'tides': 'ftp://ftp.bom.gov.au/anon/sample/catalogue/Tide/',
}
CACHE = os.getenv('BOM_CACHE', os.path.join(xdg_cache_home, NAME))
