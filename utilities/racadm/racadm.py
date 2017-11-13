from pexpect import pxssh
import logging
import StringIO
from pexpect.exceptions import TIMEOUT
from utilities.pssh_base import PSSHBase


class Racadm(PSSHBase):

    def __init__(self,
                 address,
                 username,
                 password,
                 debug):
        PSSHBase.__init__(self, address, username, password, debug)

        self.session.PROMPT = 'admin->'
        self.login()

        self.sendline('racadm')
        self.session.PROMPT = 'racadm>>'
        self.session.prompt()
        self.log_conversation()

    def log_conversation(self):
        self.log.debug('%s\n%s' % ("Conversation", self.logstring.getvalue()))
        self.logstring.truncate(0)

    def sendline(self, line):
        self.log.info(line)
        self.session.sendline(line)

    def apply_key(self, key_path):
        with open(key_path, 'r') as key_contents:
            key = key_contents.read().replace('\n', '')

        self.session.sendline('sshpkauth -i 2 -k 1 -t "%s"' % key)
        self.session.prompt()
        self.log_conversation()

    def set_value_and_get_key(self, command):
        key = None
        self.sendline(command)
        try:
            match = self.session.expect(['RAC1017:',
                                         'Key=',
                                         'ERROR:'], 5)

            if match == 0:
                # No key, just keep going
                self.session.prompt()

            if match == 1:
                # We have a key in the output
                self.session.expect('RAC1017:', 5)
                key = self.session.before.split('#')[0]
                self.session.prompt()

            if match == 2:
                # We got an error message, display it
                self.session.prompt()
                self.log.error('Error:\n%s' % self.session.before)

        except TIMEOUT:
            self.log.error('Error:\n%s' % self.session.before)
            self.session.prompt()

        self.log_conversation()
        return key

    def get_bios(self, bios_file):
      with open(bios_file, 'r') as bios_file_contents:
        for option in bios_file_contents:
	  option = option.strip()
	  if option.startswith('#') or len(option) == 0:
	     continue
	  if option.startswith('*'):
	     iter_option = option.split('*')[1]
	     attribute_to_check=option.split('*')[2]
	     self.sendline("get %s" % iter_option)
	     self.session.prompt()
             for nic in self.session.before.split('\n'):
                 if nic.startswith(iter_option):
                    nic_to_check = nic.split(' ')[0]
                    command = "get %s%s" % (nic_to_check,attribute_to_check)
		    self.sendline(command)
		    self.session.prompt()
          else:
                command = 'get %s' % option.strip()
		self.sendline(command)
		self.session.prompt()
          self.log_conversation()

    def set_bios(self, bios_file):

        job_keys = set()

        with open(bios_file, 'r') as bios_file_contents:
            for option in bios_file_contents:
                key = None
                option = option.strip()
                if option.startswith('#') or len(option) == 0:
                    continue

                if option.startswith('*'):
                    iter_option = option.split('*')[1]
                    value_to_set = option.split('*')[2].strip()
                    self.sendline("get %s" % iter_option)
                    self.session.prompt()

                    for nic in self.session.before.split('\n'):
                        if nic.startswith(iter_option):
                            nic_to_config = nic.split(' ')[0]
                            command = "set %s%s" % (nic_to_config,
                                                    value_to_set)
                            key = self.set_value_and_get_key(command)
                            if key is not None:
                                job_keys.add(key)
                else:
                    command = 'set %s' % option.strip()
                    key = self.set_value_and_get_key(command)
                    if key is not None:
                        job_keys.add(key)

        print job_keys

        for key in job_keys:
            retry = True

            while retry:
                retry = False
                command = "jobqueue create %s" % key
                self.sendline(command)
                try:
                    match = self.session.expect(['RAC1024:',
                                                 'ERROR:'], 30)
                    self.session.prompt()
                    if match == 1:
                        if 'currently in use' in self.session.before:
                            retry = True
                            self.log.info("Retrying operation")
                        else:
                            self.log.error('%s' % self.session.before)

                except TIMEOUT:
                    self.log.error('Timeout:\n[[%s]]' % self.session.before)
                    self.session.prompt()

        if len(job_keys) > 0:
            self.sendline("serveraction powercycle")
            self.session.prompt()
