import click
import time
from utilities.dell_s6010 import Dell6010Switch
# So that we can do printf
import sys

@click.group()
def cli():
	pass

@cli.command()
@click.option('--address', prompt=True, help="Address of swtich")
@click.option('--interface', prompt=True, help="Interface to check")
@click.option('--username', prompt=True)
@click.option('--password', prompt=True)
def lldp_show(**kwargs):
    #click.echo("Calling lldp show with these parameters IP=%s User=%s Pass=%s port=%s" %(kwargs['address'],kwargs['username'],kwargs['password'],kwargs['interface']))
    dellswitch = Dell6010Switch(address=kwargs['address'],
                            username=kwargs['username'],
  			    password=kwargs['password'])
    dellswitch.lldp_show(interface=kwargs['interface'])

if __name__ == '__main__':
    cli()
