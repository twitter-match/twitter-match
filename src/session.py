import os
import json
from types import MethodType
from requests_oauthlib import OAuth1Session

import api
from api import consts


class Session:

    def __init__(self):

        self.API_KEY = os.getenv('API_KEY')
        self.API_SECRET_KEY = os.getenv('API_SECRET_KEY')
        self.ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
        self.ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
        self.session = OAuth1Session(
            self.API_KEY,
            self.API_SECRET_KEY,
            self.ACCESS_TOKEN,
            self.ACCESS_TOKEN_SECRET)
        
        for API_NAME, API_CONSTS in consts.APIS_CONSTS.items():
            api_name = API_NAME.lower()
            self.__dict__[api_name] = MethodType(
                self.api_name2method(api_name), self)

    def api_name2method(self, api_name):
        
        api_module = api.__dict__[api_name]

        def method(self, **kwargs):
            return api_module(self.session, **kwargs)

        def modify_doc(doc):
            doc_lines = doc.split('\n')
            doc_lines.pop(2) # remove `session` from Args.
            doc = '\n'.join(doc_lines)
            return doc

        method.__name__ = api_name
        method.__doc__ = modify_doc(api_module.__doc__)
        return method