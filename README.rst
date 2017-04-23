========
Overview
========


`bomshell` is used to retrieve weather data from the Australian Bureau of Meteorology's (BOM)
public website, and display the result in the shell, where it belongs, as God intended it.
Not this silly web clownsuit bullshit the kids are all agog about.




Installation
============

::

    pip install bomshell

Sample Usage
========

`bomshell` command line options
::

    $ bomshell
    Usage: bomshell [OPTIONS] COMMAND [ARGS]...

      Retrieve weather data from the Australian Bureau of Meteorology

    Options:
      --version              Show the version and exit.
      -v, --verbose          Level of verbosity of logs
      -c, --cache-path PATH  BOM data cache path, Default:
                             /home/thys/.cache/bomshell
      --help                 Show this message and exit.

    Commands:
      spatial  Spatial database management

::

    $ bomshell spatial
    Usage: bomshell spatial [OPTIONS] COMMAND [ARGS]...

      Spatial database management

    Options:
      -o, --overwrite / --no-overwrite
                                      Overwrite existing spatial data, default is:
                                      False
      --help                          Show this message and exit.

    Commands:
      build      Build the local spatial database
      csvdump    Dump spatial data to csv
      fetch      Fetch spatial data
      sync       Sync the local spatial data, overwriting...
      tabledump  Dump spatial data to table

::

    bomshell spatial tabledump --help
    Usage: bomshell spatial tabledump [OPTIONS]

      Dump spatial data to table

    Options:
      -s, --spatial-type [cyclone_areas|fire_districts|forecast_districts|high_sea_areas|marine_zones|metros|ocean_wind_warning|point_places|radar_coverage|radar_location|rainfall_districts]
                                      choose a spatial type
      -f, --table-format [fancy_grid|grid|html|jira|latex|latex_booktabs|mediawiki|moinmoin|orgtbl|pipe|plain|psql|rst|simple|textile|tsv]
                                      choose a table type
      --help                          Show this message and exit.


Examples
========

::

    $ bomshell spatial tabledump --spatial-type forecast_districts --table-format fancy_grid                                                                                                                                              master      bomshell 
    ╒═══════════╤════╤════════════════════════════════════════╤═════╤══════════════════════════╕
    │ NSW_PW001 │  1 │ Northern Rivers                        │ NSW │                          │
    ├───────────┼────┼────────────────────────────────────────┼─────┼──────────────────────────┤
    │ NSW_PW002 │  2 │ Mid North Coast                        │ NSW │                          │
    ├───────────┼────┼────────────────────────────────────────┼─────┼──────────────────────────┤
    │ NSW_PW003 │  3 │ Hunter                                 │ NSW │                          │
    ├───────────┼────┼────────────────────────────────────────┼─────┼──────────────────────────┤
    │ NSW_PW004 │  4 │ Northern Tablelands                    │ NSW │                          │
    ├───────────┼────┼────────────────────────────────────────┼─────┼──────────────────────────┤
    │ NSW_PW005 │  5 │ Metropolitan                           │ NSW │                          │
    ├───────────┼────┼────────────────────────────────────────┼─────┼──────────────────────────┤
    │ NSW_PW006 │  6 │ Illawarra                              │ NSW │                          │
    ├───────────┼────┼────────────────────────────────────────┼─────┼──────────────────────────┤
    │ NSW_PW007 │  7 │ South Coast                            │ NSW │                          │
    ├───────────┼────┼────────────────────────────────────────┼─────┼──────────────────────────┤
    │ NSW_PW008 │  8 │ Central Tablelands                     │ NSW │                          │
    ├───────────┼────┼────────────────────────────────────────┼─────┼──────────────────────────┤
