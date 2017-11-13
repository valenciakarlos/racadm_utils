import logging
from utilities.rest import ReST
from datetime import datetime


class RackHD(object):

    def __init__(self,
                 address,
                 email,
                 password,
                 debug=False):

        if debug:
            logging.getLogger('').setLevel(logging.DEBUG)

        self.log = logging.getLogger(__name__)
        self.address = address
        self.email = email
        self.password = password
        self.rest_rackhd = ReST("https://%s" % self.address)
        self.rest_api = ReST("http://%s:8080" % self.address)
        self._login_token = None
        self._last_login = None

        self.fetch_uuid('948BRD2')

    @property
    def login_token(self):
        if self._last_login is None or \
                (datetime.now() - self._last_login).total_seconds() > 600:
            body = {'email': self.email,
                    'password': self.password}
            login_response = self.rest.request(method='post',
                                               path='/login',
                                               body=body)

            self._login_token = login_response['response'] \
                ['user']['authentication_token']
            self.log.debug('Token: %s' % self._login_token)
            self._last_login = datetime.now()
        return self._login_token

    def fetch_uuid(self, name):
        path = '/api/1.1/nodes?name=Enclosure%%20Node%%20%s' % name
        self.log.debug("Path: %s" % path)
        response = self.rest_api.request(path, 'get')
        return response
