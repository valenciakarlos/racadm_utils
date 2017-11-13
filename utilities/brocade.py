from utilities.pssh_base import PSSHBase


class BrocadeSwitch(PSSHBase):

    def __init__(self,
                 address,
                 username,
                 password,
                 debug=False):

        PSSHBase.__init__(self, address, username, password, debug)
        self.session.PROMPT = "#"
        self.login()

    def set_vlan(self,
                 interface,
                 vlan_id):

        self.sendline("config term")
        self.session.prompt()
        self.log_conversation()

        self.sendline("interface %s" % interface)
        self.session.prompt()
        self.log_conversation()

        self.sendline("switchport mode access")
        self.session.prompt()
        self.log_conversation()

        self.sendline("switchport access vlan %s" % vlan_id)
        self.session.prompt()
        self.log_conversation()
