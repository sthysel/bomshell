import click


@click.command()
@click.argument('names', nargs=-1)
def main(names):
    """ nameless """
    click.echo(repr(names))
