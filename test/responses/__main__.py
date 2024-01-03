import logging

import click

from .base import _KNOWN_RECORDERS, record_site

GLOBAL_CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help']
)


@click.group(context_settings={**GLOBAL_CONTEXT_SETTINGS}, help='Create responses files')
def cli():
    pass  # pragma: no cover


@cli.command('record', context_settings={**GLOBAL_CONTEXT_SETTINGS},
             help='Operate responses, and save them to yaml file.')
@click.option('-A', '--all', 'record_all', is_flag=True, type=bool, default=False,
              help='Operate for all the websites.', show_default=True)
@click.option('-s', '--site', 'websites', type=click.Choice(list(_KNOWN_RECORDERS.keys())), multiple=True,
              help='Operate on chosen website.')
def record(record_all, websites):
    logging.basicConfig(level=logging.INFO)
    if record_all:
        websites = _KNOWN_RECORDERS.keys()

    websites = tuple(list(websites))
    logging.info(f'The following will be recorded: {websites!r}')
    for site in list(websites):
        logging.info(f'Recording for {site!r} ...')
        record_site(site)


if __name__ == '__main__':
    cli()
