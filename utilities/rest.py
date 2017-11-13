import requests
import logging
import json


class ReST(object):

    def __init__(self,
                 url):

        self.log = logging.getLogger(__name__)

        self.url = url
        self.base_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    def request(self,
                path='/',
                method='get',
                headers={},
                body=None):

        combined_headers = self.base_headers
        combined_headers.update(headers)

        self.log.debug("ReST: %s %s%s" % (method,
                                          self.url,
                                          path))

        self.log.debug("Headers: %s" % combined_headers)
        if body:
            self.log.debug("Body: %s" % json.dumps(body))

        response = requests.request(method=method,
                                    url=('%s%s' % (self.url, path)),
                                    data=(json.dumps(body) if body
                                          else None),
                                    headers=combined_headers,
                                    verify=False)

        response.raise_for_status()

        content = json.loads(response.content)
        self.log.debug("Response: %s" % content)

        return content
