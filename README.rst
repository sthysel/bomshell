========
Overview
========

.. image:: https://readthedocs.org/projects/bomshell/badge/?version=latest
   :target: http://bomshell.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


``bomshell`` is used to retrieve weather data from the `Australian Bureau of Meteorology's (BOM) <http://www.bom.gov.au/>`_
public FTP site, and display the result in the shell or as interactive maps.

``bomshell`` retrieves spatial data (shapefiles) from BOM's public FTP site and packs it into a local SQLite database.
Tools are provided to build and maintain the local database, export data to various formats, and generate interactive
maps for visualization.


Installation
============

Using uv (recommended):

.. code::

    $ uv tool install bomshell

Using pip:

.. code::

    $ pip install bomshell


Config
======

``bomshell`` is configured using CLI options and a ``.bomshell`` settings file.
To see the valid knobs that can be tuned use the ``knobs`` command:

.. code::

    $ bomshell knobs

To create a fresh ``.bomshell`` config file:

.. code::

    $ bomshell knobs > ~/.bomshell


Initial Setup
=============

Fetch the spatial data (shapefiles) from BOM:

.. code::

   $ bomshell spatial fetch

This downloads all shapefile components (.dbf, .shp, .shx, .prj) to ``~/.cache/bomshell/spatial_cache/``.

Build the local SQLite database (optional, for database queries):

.. code::

   $ bomshell spatial build


Interactive Maps
================

Generate interactive HTML maps of BOM spatial data. Maps open automatically in your browser.

**Point data** (markers on map):

.. code::

   # Radar locations across Australia
   $ bomshell spatial map -s radar_location

   # All 1,475 weather observation points
   $ bomshell spatial map -s point_places

   # Radar coverage areas
   $ bomshell spatial map -s radar_coverage

**Polygon data** (district/zone boundaries with hover highlighting):

.. code::

   # Weather forecast districts
   $ bomshell spatial map -s forecast_districts

   # Fire weather districts
   $ bomshell spatial map -s fire_districts

   # Marine forecast zones
   $ bomshell spatial map -s marine_zones

   # Rainfall districts
   $ bomshell spatial map -s rainfall_districts

   # Metropolitan areas
   $ bomshell spatial map -s metros

   # Tropical cyclone warning areas
   $ bomshell spatial map -s cyclone_areas

   # High seas forecast areas
   $ bomshell spatial map -s high_sea_areas

   # Ocean wind warning areas
   $ bomshell spatial map -s ocean_wind_warning

Map options:

.. code::

   # Save to custom location
   $ bomshell spatial map -s radar_location -o ~/maps/radars.html

   # Don't open browser automatically
   $ bomshell spatial map -s forecast_districts --no-open

Maps are saved to ``~/.cache/bomshell/`` by default.


Data Export
===========

Export spatial data to tables or CSV:

.. code::

   # View as formatted table
   $ bomshell spatial tabledump -s radar_coverage -f fancy_grid

   # Export to CSV
   $ bomshell spatial csvdump -s point_places > places.csv

Available table formats: ``fancy_grid``, ``grid``, ``html``, ``jira``, ``latex``, ``pipe``, ``plain``, ``psql``, ``rst``, ``simple``, ``tsv``, and more.


Sample Usage
============

All ``bomshell`` command line options are available from the ``--help`` option:

.. code:: shell

    $ bomshell --help
    Usage: bomshell [OPTIONS] COMMAND [ARGS]...

      Retrieve weather data from the Australian Bureau of Meteorology

    Options:
      --version              Show the version and exit.
      -v, --verbose          Level of verbosity of logs
      -c, --cache-path PATH  BOM data cache path
      --help                 Show this message and exit.

    Commands:
      knobs    Print all known settings and their current defaults
      spatial  Spatial database management

.. code:: shell

    $ bomshell spatial --help
    Usage: bomshell spatial [OPTIONS] COMMAND [ARGS]...

      Spatial database management

    Options:
      -o, --overwrite / --no-overwrite
                                      Overwrite existing spatial data
      --ftp-timeout INTEGER           FTP Timeout in seconds
      --help                          Show this message and exit.

    Commands:
      build      Build the local spatial database
      csvdump    Dump spatial data to csv
      fetch      Fetch spatial data
      map        Generate an interactive map of spatial data
      sync       Sync the local spatial data, overwriting existing files
      tabledump  Dump spatial data to table


Available Spatial Types
=======================

===================  ===========  =====================================================
Type                 Data Format  Description
===================  ===========  =====================================================
forecast_districts   Polygon      Weather forecast districts by state
marine_zones         Polygon      Marine and coastal forecast zones
fire_districts       Polygon      Fire weather forecast districts
rainfall_districts   Polygon      Rainfall reporting districts
cyclone_areas        Polygon      Tropical cyclone warning areas
high_sea_areas       Polygon      High seas forecast areas
metros               Polygon      Metropolitan forecast areas
ocean_wind_warning   Polygon      Ocean wind warning zones
radar_location       Point        BOM radar station locations
radar_coverage       Point        Radar coverage information
point_places         Point        Weather observation stations (1,475 locations)
===================  ===========  =====================================================


Development
===========

.. code::

   # Clone and install
   $ git clone https://github.com/sthysel/bomshell
   $ cd bomshell
   $ uv sync --all-extras

   # Run tests
   $ just test

   # Run linting
   $ just lint

   # See all available commands
   $ just
