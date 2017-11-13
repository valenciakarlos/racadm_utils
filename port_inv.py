import click
import time
from utilities.dellswitch import DellSwitch
from utilities.esxi import Esxi
# So that we can do printf
import sys

@click.group()
def cli():
	pass

@cli.command()
@click.option('--address', prompt=True, help="Address of server to which find macs from")
@click.option('--username', prompt=True)
@click.option('--password', prompt=True)
def port_inv(**kwargs):
    click.echo("Calling Port Inventory with these parameters IP=%s User=%s Pass=%s" %(kwargs['address'],kwargs['username'],kwargs['password']))
    esxi=Esxi(address=kwargs['address'],
              username=kwargs['username'],
              password=kwargs['password'])
    mac=esxi.create_vmk()
    print "VMK created with MAC="+mac
    vmnic_list=["vmnic2","vmnic3"]
    esxi.link_port("vmnic2")
    dellswitch = DellSwitch(address="172.16.123.6",
                            username="dellemc",
  			    password="dellemc")
    for vmnic in vmnic_list:
        esxi.link_port(vmnic)
        time.sleep(2)
	port=dellswitch.find_mac(mac)
	sys.stdout.write(vmnic)
	print ","+port
	esxi.unlink_port(vmnic)
    esxi.delete_vmk()


@cli.command()
@click.option('--address', prompt=True, help="Address of switch", default="172.16.123.6")
@click.option('--username', prompt=True, help="user on switch", default="dellemc")
@click.option('--password', prompt=True, help="Paswd on switch", default="dellemc")
@click.argument('mac')
def find_mac(**kwargs):
    click.echo("Searching for MAC %s" %kwargs['mac'])
    dellswitch = DellSwitch(address=kwargs['address'],
                            username=kwargs['username'],
		            password=kwargs['password'])
    port=dellswitch.find_mac(kwargs['mac'])
    click.echo("Found at port %s" %port)



if __name__ == '__main__':
    cli()
