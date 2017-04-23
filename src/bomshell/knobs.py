import os
import sys

import click

register = {}


def get_string(env_value, default):
    register[env_value] = default
    try:
        return os.getenv(env_value, default)
    except ValueError:
        click.echo('{} must be a string'.format(env_value))
        sys.exit()


def get_int(env_value, default):
    register[env_value] = default
    try:
        return int(os.getenv(env_value, default))
    except ValueError:
        click.echo('{} must be a integer'.format(env_value))
        sys.exit()


def get_bool(env_value, default):
    register[env_value] = default
    try:
        return bool(os.getenv(env_value, default))
    except ValueError:
        click.echo('{} must be a boolean'.format(env_value))
        sys.exit()


def get_knob_defaults():
    """ Returns a string with defaults """

    return '\n'.join(['#{knob}={default}'.format(knob=knob, default=register[knob]) for knob in sorted(register.keys())])
