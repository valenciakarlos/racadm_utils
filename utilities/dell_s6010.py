from utilities.pssh_base import PSSHBase


class Dell6010Switch(PSSHBase):

    def __init__(self,
                 address,
                 username,
                 password,
                 debug=False):

        PSSHBase.__init__(self, address, username, password, debug)
        self.session.PROMPT = "#"
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

    def lldp_show(self, interface):
	grep_line="grep \"Remote Chassis ID:|Remote System Name:\""
	#print "Check interface details"
        #self.sendline("show lldp neighbors interface %s detail " %(interface))
	#self.session.prompt()
	#print "Now with the GREP" + grep_line

        self.sendline("show lldp neighbors interface %s detail | %s" %(interface,grep_line))
	self.session.prompt()

	#self.session.prompt()
	self.log_conversation()
	host=self.session.before.split('\n')[2].split(':')[1]
	nic_id=self.session.before.split('\n')[1].split(':')[1]
	print "---"
	print interface 
	print host
	print nic_id

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
