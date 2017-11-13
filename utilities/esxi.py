from utilities.pssh_base import PSSHBase


class Esxi(PSSHBase):

    def __init__(self,
                 address,
                 username,
                 password,
                 debug=False):

        PSSHBase.__init__(self, address, username, password, debug)
        #Prompt looks like = [root@edge-server23:~]
        self.session.PROMPT = "\[\w+@\w+-\w+:~]"
        self.login()
        self.session.prompt()
        self.address=address
        self.sendline("hostname")
        self.session.prompt()
        self.hostname=self.session.before.split('\n')[1]
        self.hostname=self.hostname.rstrip()
        print "Successfully logged into " + self.address + " (" + self.hostname+")"

    def list_nics(self):
        #print "Linking TestVS to "+vmnic
	self.sendline("esxcfg-nics -l")
	self.session.prompt()
	print self.session.before

    def get_host(self):
        return self.hostname

    def list_routes(self):
        #print "Linking TestVS to "+vmnic
	self.sendline("esxcfg-route -l")
	self.session.prompt()
	print self.session.before

    def list_vswitch(self):
        #print "Linking TestVS to "+vmnic
	self.sendline("esxcli network vswitch dvs vmware list | egrep 'Name|Uplinks'")
	#self.sendline("esxcfg-vswitch -l")
	self.session.prompt()
	print self.session.before

    def list_vxlan(self):
        #print "Linking TestVS to "+vmnic
	self.sendline("esxcli network vswitch dvs vmware vxlan list")
	self.session.prompt()
	print self.session.before

    def list_sriov(self):
        #print "Linking TestVS to "+vmnic
	self.sendline("esxcli network sriovnic list")
	self.session.prompt()
	print self.session.before

    def link_port(self,vmnic):
        #print "Linking TestVS to "+vmnic
	self.sendline("esxcfg-vswitch TestVS --link %s" %vmnic)
	self.session.prompt()
	#print self.session.before


    def unlink_port(self,vmnic):
        #print "Unlinking TestVS to "+vmnic
	self.sendline("esxcfg-vswitch TestVS --unlink %s" %vmnic)
	self.session.prompt()
	#print self.session.before

    def log_stats(self,foldername):
        header=self.address +"("+self.hostname+"): "
        print header + "Creating stats folder "+foldername
	self.sendline("mkdir /%s" %foldername)
        self.session.prompt()
	self.sendline("cd /%s" %foldername)
        self.session.prompt()
	print header + "Logging netstats. wait 2mins"
	self.sendline("net-stats -i 120 -t WicQv -A >>/%s/`hostname`_netstats.logs" %foldername)
        self.session.prompt()
	print header + "Sched stats"
	self.sendline("sched-stats -t pcpu-stats >>/%s/`hostname`_schedstats.logs" %foldername)
        self.session.prompt()
	print header + "Stats per port. Wait for 15 seconds"
	self.sendline("net-stats -i 5 -t icWqQ -S DvsPortset-1 | grep used | grep -v vcpu | grep name | grep -v 'net-stats' >>/%s/`hostname`_vmnic5_netstats.log" %foldername)
        self.session.prompt()
	self.sendline("net-stats -i 5 -t icWqQ -S DvsPortset-2 | grep used | grep -v vcpu | grep name | grep -v 'net-stats' >> /%s/`hostname`_vmnic6_netstats.log" %foldername)
        self.session.prompt()
	self.sendline("net-stats -i 5 -t icWqQ -S DvsPortset-3 | grep used | grep -v vcpu | grep name | grep -v 'net-stats' >> /%s/`hostname`_vmnic9_netstats.log" %foldername)
        self.session.prompt()
        print header + "All stats created on folder " + foldername
	#self.sendline("esxtop -b -n 5 -d 10 > /%s/`hostname`_esxtop_5_captures_10sinterval.log" %foldername)
        #self.session.prompt()

    def delete_vmk(self):
        #print "Delete VMK"
	self.sendline("esxcfg-vmknic  -d TestPG")
	self.session.prompt()
	#print self.session.before
	self.sendline("esxcfg-vswitch -d TestVS")
	self.session.prompt()
	#print self.session.before

    def create_vmk(self): 
	#print "Creating VMK"
        #Checking that VS does not exists
	self.sendline("esxcfg-vswitch -c TestVS")
        self.session.prompt()
        result= self.session.before.split('\n')[1]
	result=result.split()
        result=result[0]
	print "Result="
        print result
        if (result=="1"):
           print "Switch Exists, delete manually and retry"
	   return 0
        #print "Creating the vSwitch"
	self.sendline("esxcfg-vswitch -a TestVS")
	self.session.prompt()
	#print "Creating the PG"
	self.sendline("esxcfg-vswitch TestVS --add-pg TestPG")
	self.session.prompt()
	#print "Adding VLANId"
	self.sendline("esxcfg-vswitch TestVS -v 2124 -p TestPG")
	self.session.prompt()
	#print "Adding the vmk"
	self.sendline("esxcfg-vmknic -a -i DHCP -p TestPG")
	self.session.prompt()
	# Capturing MAC
	self.sendline("esxcfg-vmknic -l | grep TestPG | grep IPv4")
	self.session.prompt()
	result= self.session.before.split('\n')[1]
	result=result.split()
	result=result[6]
        self.log_conversation()
	return result


