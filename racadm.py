import click
from utilities.racadm.racadm import Racadm
import logging


@click.group()
def racadm():
    pass


@racadm.command()
@click.argument('key_file')
@click.option('--address', prompt=True)
@click.option('--username', prompt=True)
@click.option('--password', prompt=True)
@click.option('--debug', '-d', is_flag=True)
def apply_key(**kwargs):
    racadm = Racadm(address=kwargs['address'],
                    username=kwargs['username'],
                    password=kwargs['password'],
                    debug=kwargs['debug'])

    racadm.apply_key(kwargs['key_file'])


@racadm.command()
@click.argument('options_file')
@click.option('--address', prompt=True)
@click.option('--username', prompt=True)
@click.option('--password', prompt=True)
@click.option('--debug', '-d', is_flag=True)
def set_bios(**kwargs):
    racadm = Racadm(address=kwargs['address'],
                    username=kwargs['username'],
                    password=kwargs['password'],
                    debug=kwargs['debug'])

    racadm.set_bios(kwargs['options_file'])


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    racadm()
