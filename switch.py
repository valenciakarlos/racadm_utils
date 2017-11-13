import click
from utilities.brocade import BrocadeSwitch


@click.group()
def switch():
    pass


@switch.command()
@click.argument('interface')
@click.argument('vlan_id')
@click.option('--address', prompt=True)
@click.option('--username', prompt=True)
@click.option('--password', prompt=True)
def set_vlan(**kwargs):
    brocade = BrocadeSwitch(address=kwargs['address'],
                            username=kwargs['username'],
                            password=kwargs['password'])
    brocade.set_vlan(kwargs['interface'],
                     kwargs['vlan_id'])

if __name__ == '__main__':
    switch()
