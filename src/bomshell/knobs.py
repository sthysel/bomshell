import os
import sys

import click

register = {}


def get_string(env_value, default):
    register[env_value] = default
    try:
        return os.getenv(env_value, default)
    except ValueError:
        click.echo(f"{env_value} must be a string")
        sys.exit()


def get_int(env_value, default):
    register[env_value] = default
    try:
        return int(os.getenv(env_value, default))
    except ValueError:
        click.echo(f"{env_value} must be a integer")
        sys.exit()


def get_bool(env_value, default):
    register[env_value] = default
    try:
        return bool(os.getenv(env_value, default))
    except ValueError:
        click.echo(f"{env_value} must be a boolean")
        sys.exit()


def get_knob_defaults():
    """Returns a string with defaults"""

    return "\n".join([f"#{knob}={register[knob]}" for knob in sorted(register.keys())])
