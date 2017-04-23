import os
from xdg.BaseDirectory import xdg_cache_home
from .knobs import get_int, get_bool, get_string

__version__ = '1.0.2'

NAME = 'bomshell'

CACHE = get_string('BOM_CACHE', os.path.join(xdg_cache_home, NAME))

SPATIAL_CACHE = os.path.join(CACHE, 'spatial_cache/')
SPATIAL_DB = os.path.join(CACHE, 'spatial.sqlite')

OVERWRITE = get_bool('BOM_OVERWRITE_EXISTING_SPATIAL_DATA', False)
VERBOSE = 0

FTP_TIMEOUT = get_int('BOM_FTP_TIMEOUT', 5)
