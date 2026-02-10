import os

from dotenv import find_dotenv
from dotenv import load_dotenv
from xdg.BaseDirectory import xdg_cache_home

from .knobs import get_bool
from .knobs import get_int
from .knobs import get_string

load_dotenv(find_dotenv(filename=".bomshell", usecwd=True))

NAME = "bomshell"

CACHE = get_string("BOM_CACHE", os.path.join(xdg_cache_home, NAME))

SPATIAL_CACHE = os.path.join(CACHE, "spatial_cache/")
SPATIAL_DB = os.path.join(CACHE, "spatial.sqlite")

OVERWRITE = get_bool("BOM_OVERWRITE_EXISTING_SPATIAL_DATA", False)
VERBOSE: int = 0

FTP_TIMEOUT = get_int("BOM_FTP_TIMEOUT", 5)
