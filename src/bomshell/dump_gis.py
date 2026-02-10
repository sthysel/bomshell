import csv
import sys

import dbfread
from rich.console import Console
from rich.table import Table

from .fetch_gis import get_source_file_name
from .output import emit_json
from .output import is_json_mode


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


def dump_to_table(data_type):
    """
    Write spatial data as a Rich table, or JSON in --json mode.
    :param data_type:
    :return:
    """
    source_file = get_source_file_name(data_type)
    dbf = dbfread.DBF(source_file)

    if is_json_mode():
        emit_json([dict(record) for record in dbf])
        return

    rich_table = Table(show_header=True, header_style="bold cyan")
    for name in dbf.field_names:
        rich_table.add_column(name)
    for record in dbf:
        rich_table.add_row(*[str(v) for v in record.values()])

    Console().print(rich_table)
