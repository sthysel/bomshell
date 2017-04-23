import csv
import sys

import dbfread
import tabulate

from bomshell.fetch_gis import get_source_file_name


def get_table_formats():
    return sorted(tabulate.tabulate_formats)


def dump_to_csv(data_type):
    """
    Write spatial data to stdout
    :param data_type: 
    :return: 
    """
    source_file = get_source_file_name(data_type)
    table = dbfread.DBF(source_file)
    writer = csv.writer(sys.stdout)

    writer.writerow(table.field_names)
    for record in table:
        writer.writerow(list(record.values()))


def dump_to_table(data_type, table_format=''):
    """
    Write spatial data to fancy table
    :param data_type: 
    :return: 
    """
    source_file = get_source_file_name(data_type)
    table = dbfread.DBF(source_file)
    print(tabulate.tabulate(table, headers='keys', tablefmt=table_format))
