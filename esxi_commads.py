import click
import time
from utilities.esxi import Esxi
# So that we can do printf
import sys

@click.group()
def cli():
	pass

@cli.command()
@click.option('--address', prompt=True, help="Address of server on which to get inventory")
@click.option('--username', default="root", help="ESXi SSH username")
@click.option('--password', default="dellemc", help="ESXi SSH password")
def inventory(**kwargs):
#    click.echo("Calling Stats collection to folder %s on IP=%s User=%s Pass=%s" %(kwargs['foldername'],kwargs['address'],kwargs['username'],kwargs['password']))
    esxi=Esxi(address=kwargs['address'],
              username=kwargs['username'],
              password=kwargs['password'])
    hostname=esxi.get_host()
    print "-----------------------------------------------"
    print "Hostname is " + hostname
    print "-----------------------------------------------"
    print "NICs:"
    esxi.list_nics()
    print "----"
    print "Vswitch"
    esxi.list_vswitch()
    print "----"
    print "Configured vxlan"
    esxi.list_vxlan()
    print "----"
    print "Configure sriov"
    esxi.list_sriov()

@cli.command()
@click.option('--address', prompt=True, help="Address of server on which to get hostname")
@click.option('--username', default="root", help="ESXi SSH username")
@click.option('--password', default="dellemc", help="ESXi SSH password")
def get_hostname(**kwargs):
#    click.echo("Calling Stats collection to folder %s on IP=%s User=%s Pass=%s" %(kwargs['foldername'],kwargs['address'],kwargs['username'],kwargs['password']))
    esxi=Esxi(address=kwargs['address'],
              username=kwargs['username'],
              password=kwargs['password'])
    hostname=esxi.get_host()
    print "Hostname is " + hostname

@cli.command()
@click.option('--address', prompt=True, help="Address of server on which to list nics ")
@click.option('--username', prompt=True)
@click.option('--password', prompt=True)
def list_nics(**kwargs):
#    click.echo("Calling Stats collection to folder %s on IP=%s User=%s Pass=%s" %(kwargs['foldername'],kwargs['address'],kwargs['username'],kwargs['password']))
    esxi=Esxi(address=kwargs['address'],
              username=kwargs['username'],
              password=kwargs['password'])
    esxi.list_nics()

@cli.command()
@click.option('--address', prompt=True, help="Address of server on which to list routes ")
@click.option('--username', prompt=True)
@click.option('--password', prompt=True)
def list_routes(**kwargs):
#    click.echo("Calling Stats collection to folder %s on IP=%s User=%s Pass=%s" %(kwargs['foldername'],kwargs['address'],kwargs['username'],kwargs['password']))
    esxi=Esxi(address=kwargs['address'],
              username=kwargs['username'],
              password=kwargs['password'])
    esxi.list_routes()

@cli.command()
@click.option('--address', prompt=True, help="Address of server on which to list vswitch ")
@click.option('--username', prompt=True)
@click.option('--password', prompt=True)
def list_vswitch(**kwargs):
#    click.echo("Calling Stats collection to folder %s on IP=%s User=%s Pass=%s" %(kwargs['foldername'],kwargs['address'],kwargs['username'],kwargs['password']))
    esxi=Esxi(address=kwargs['address'],
              username=kwargs['username'],
              password=kwargs['password'])
    esxi.list_vswitch()

@cli.command()
@click.option('--address', prompt=True, help="Address of server on which to list vxlan ")
@click.option('--username', prompt=True)
@click.option('--password', prompt=True)
def list_vxlan(**kwargs):
#    click.echo("Calling Stats collection to folder %s on IP=%s User=%s Pass=%s" %(kwargs['foldername'],kwargs['address'],kwargs['username'],kwargs['password']))
    esxi=Esxi(address=kwargs['address'],
              username=kwargs['username'],
              password=kwargs['password'])
    esxi.list_vxlan()



if __name__ == '__main__':
    cli()
