from utilities.pssh_base import PSSHBase


class DellSwitch(PSSHBase):

    def __init__(self,
                 address,
                 username,
                 password,
                 debug=False):

        PSSHBase.__init__(self, address, username, password, debug)
        self.session.PROMPT = "s3048#"
        self.login()


    def find_mac(self,
    		mac):
	#print "Looking for MAC= " + mac
	self.sendline("show mac-address-table | grep %s" %mac)
        self.session.prompt()
        result= self.session.before.split('\n')[1]
	# 2123    14:18:77:0f:83:2a       Dynamic         Gi 3/47         Active
	result=result.split()
	#['2123', '14:18:77:0f:83:2a', 'Dynamic', 'Gi', '3/47', 'Active']
	port=result[4]
	#print "Found at port " +port
        self.log_conversation()
	return port

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
