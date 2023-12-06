import requests
import logging

class UserAgent():
    def __init__(self, headers={}):
            """
            Initializes a UserAgent object.

            Args:
                headers (dict): A dictionary of headers to be used in the HTTP requests.

            Returns:
                None
            """
            self.create_session(headers)

    def create_session(self, headers={}):
        self._session = requests.Session()
        self._session.headers.update(headers)
        proxies = {
            'http': 'socks5://localhost:9050',
            'https': 'socks5://localhost:9050'
        }
        #self._session.proxies.update(proxies)


    def get(self, url, headers={}):
        logging.debug(f"GET {url}")
        response = self._session.get(url, headers=headers)
        return response
    
    def post(self, url, headers={}, data={}):
        logging.debug(f"POST {url}\n{data}")
        response = self._session.post(url, headers=headers, json=data)
        return response

    
