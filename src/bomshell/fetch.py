import os

import ftputil
import ftputil.error

from . import settings
from .output import print_error
from .output import print_warning


def remove_existing_file(cache_file_name, overwrite):
    """Check if file exists and handle accordingly.

    Returns True if we should proceed with download, False to skip.
    """
    if os.path.isfile(cache_file_name):
        if overwrite:
            os.remove(cache_file_name)
            return True
        else:
            if settings.VERBOSE:
                print_warning(f"Skipping {cache_file_name} (already exists)")
            return False
    return True


def get_file(directory, filename, ftp_server, ftp_user="anonymous", ftp_password=""):
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

    if not remove_existing_file(target_file, settings.OVERWRITE):
        return True  # File exists and we're not overwriting, skip

    try:
        with ftputil.FTPHost(host=ftp_server, user=ftp_user, passwd=ftp_password, timeout=settings.FTP_TIMEOUT) as ftp_host:
            ftp_host.chdir(directory)
            if not ftp_host.path.exists(filename):
                if settings.VERBOSE:
                    print_warning(f"File not found on server: {filename}")
                return False
            ftp_host.download(filename, target_file)
            return True
    except ftputil.error.FTPOSError:
        print_error(f"FTP timeout fetching {filename}")
        print_error("Consider using the --ftp-timeout option")
        print_error("or increasing the FTP_TIMEOUT value in .bomshell")
        return False
