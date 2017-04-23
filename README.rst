========
Overview
========


Retrieve weather data from the Australian  Bureau of Meteorology


Installation
============

::

    pip install bomshell

Overview
========


::

    $ bomshell                                                                                                                                                                                                                                   master       bomshell 
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

    $ bomshell spatial tabledump
    Usage: bomshell spatial tabledump [OPTIONS]

      Dump spatial data to table

    Options:
      -s, --spatial-type [cyclone_areas|fire_districts|forecast_districts|high_sea_areas|marine_zones|metros|ocean_wind_warning|point_places|radar_coverage|radar_location|rainfall_districts]
                                      choose a spatial type from ['cyclone_areas',
                                      'fire_districts', 'forecast_districts',
                                      'high_sea_areas', 'marine_zones', 'metros',
                                      'ocean_wind_warning', 'point_places',
                                      'radar_coverage', 'radar_location',
                                      'rainfall_districts']
      -f, --table-format [fancy_grid|grid|html|jira|latex|latex_booktabs|mediawiki|moinmoin|orgtbl|pipe|plain|psql|rst|simple|textile|tsv]
                                      choose a table type from ['fancy_grid',
                                      'grid', 'html', 'jira', 'latex',
                                      'latex_booktabs', 'mediawiki', 'moinmoin',
                                      'orgtbl', 'pipe', 'plain', 'psql', 'rst',
                                      'simple', 'textile', 'tsv']
      --help                          Show this message and exit.

