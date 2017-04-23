import ftputil
import os
import sys

import click
from . import settings


def remove_existing_file(cache_file_name, overwrite):
    if os.path.isfile(cache_file_name):
        if overwrite:
            os.remove(cache_file_name)
        else:
            click.secho('{} already exists. Use the --override option to re-download'.format(cache_file_name), fg='red')
            sys.exit()


def get_file(directory, filename, ftp_server, ftp_user='anonymous', ftp_password=''):
    """
    :param config: 
    :param directory: 
    :param filename: 
    :param ftp_server: 
    :param ftp_user: 
    :param ftp_password: 
    :return: 
    """

    os.makedirs(settings.SPATIAL_CACHE, exist_ok=True)
    target_file = os.path.join(settings.SPATIAL_CACHE, filename)

    remove_existing_file(target_file, settings.OVERWRITE)

    with ftputil.FTPHost(host=ftp_server, user=ftp_user, passwd=ftp_password, timeout=settings.FTP_TIMEOUT) as ftp_host:
        ftp_host.chdir(directory)
        ftp_host.download(filename, target_file)
