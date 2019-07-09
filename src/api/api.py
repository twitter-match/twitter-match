import os
import yaml
import json
import requests


yaml_path = os.path.join(
    os.path.dirname(__file__), 'params.yml')
with open(yaml_path, 'r') as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)


class APIBase():
    
    def __init__(self, api_name):
        
        self.CONFIG = CONFIG[api_name]
        
    def make_docstr(self):
        
        doc = 'Args:\n'
        for k, v in self.CONFIG['PARAMETERS'].items():
            dscs = v['description'].split('\n')
            doc += '    {}: '.format(k)
            for idx, dsc in enumerate(dscs):
                dsc = dsc.strip() + '\n'
                doc += dsc if idx == 0 else '        {}'.format(dsc)
        self.__call__.__func__.__doc__ = doc
    
    def check_params(self, **params):
        
        for param in params:
            if param not in self.CONFIG['PARAMETERS']:
                raise ValueError('Invalid parameter.')
    
    def check_response(self, response):

        if response.status_code != 200:
            raise ConnectionError('Failed: {}'.format(response.status_code))        
    

class GetBase(APIBase):
    
    def __init__(self, api_name):
        
        super().__init__(api_name)
        self.make_docstr()

    def __call__(self, session, **params):
        
        self.check_params(**params)
        response = session.get(self.CONFIG['URL'], params=dict(**params))
        self.check_response(response)
        result = json.loads(response.text)
        
        return result


class GetFriendsIds(GetBase):
    
    def __init__(self):
        
        super().__init__('GET_FRIENDS_IDS')

class GetFavorites(GetBase):
    
    def __init__(self):
        
        super().__init__('GET_FAVORITES')