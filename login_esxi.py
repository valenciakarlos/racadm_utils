import click
import time
from utilities.esxi import Esxi
# So that we can do printf
import sys

@click.group()
def cli():
	pass

@cli.command()
@click.option('--address', prompt=True, help="Address of server on which to collect logs")
@click.option('--username', prompt=True)
@click.option('--password', prompt=True)
def get_hostname(**kwargs):
#    click.echo("Calling Stats collection to folder %s on IP=%s User=%s Pass=%s" %(kwargs['foldername'],kwargs['address'],kwargs['username'],kwargs['password']))
    esxi=Esxi(address=kwargs['address'],
              username=kwargs['username'],
              password=kwargs['password'])
    hostname=esxi.get_host()
    print "Hostname is " + hostname
if __name__ == '__main__':
    cli()
