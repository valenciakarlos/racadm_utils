from pexpect import pxssh
import logging
import StringIO


class PSSHBase(object):

    def __init__(self,
                 address,
                 username,
                 password,
                 debug=False):

        if debug:
            logging.getLogger('').setLevel(logging.DEBUG)

        self.log = logging.getLogger(__name__)

        self.address = address
        self.username = username
        self.password = password

        self.logstring = StringIO.StringIO()
        self.session = pxssh.pxssh(options={
            "StrictHostKeyChecking": "no",
            "UserKnownHostsFile": "/dev/null"},
            logfile=self.logstring)

        self.prompt = self.session.PROMPT

    def login(self):
        self.log.debug("ssh %s@%s" % (self.username, self.address))
        self.session.login(self.address,
                           self.username,
                           self.password,
                           auto_prompt_reset=False)
        self.log_conversation()

    def log_conversation(self):
        self.log.debug('%s\n%s' % ("Conversation", self.logstring.getvalue()))
        self.logstring.truncate(0)

    def sendline(self, line):
        self.log.info(line)
        self.session.sendline(line)
