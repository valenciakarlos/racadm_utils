import click
from utilities.rackhd.rackhd import RackHD
import logging


@click.group()
def rackhd():
    pass


@rackhd.command()
@click.option('--address', prompt=True)
@click.option('--email', prompt=True)
@click.option('--password', prompt=True)
@click.option('--debug', '-d', is_flag=True)
def login(**kwargs):

    rack = RackHD(**kwargs)
    print rack.login_token


@rackhd.command()
@click.argument('serialnumber')
@click.option('--address', prompt=True)
@click.option('--email', prompt=True)
@click.option('--password', prompt=True)
@click.option('--debug', '-d', is_flag=True)
def fetch_uuid(**kwargs):

    rack = RackHD(address=kwargs['address'],
                  email=kwargs['email'],
                  password=kwargs['password'],
                  debug=kwargs['debug'])
    print rack.fetch_uuid(kwargs['serialnumber'])

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    rackhd()
