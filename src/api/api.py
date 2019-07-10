import json
import requests
import textwrap

class APIBase():
    
    def __init__(self, API_CONSTS):
        
        self.API_CONSTS = API_CONSTS
        self.__call__.__func__.__doc__ = self.make_docstr()
        
    def make_docstr(self):

        docstr = '\nArgs:\n'
        for k, v in self.API_CONSTS['PARAMETERS'].items():
            dscs = textwrap.wrap(
                '{}: {}'.format(k, v['description']), width=70)
            for idx, dsc in enumerate(dscs):
                spaces = ' '*4 if idx == 0 else ' '*8
                docstr += '{}{}\n'.format(spaces, dsc)
                
        return docstr
    
    def check_params(self, **params):
        
        for param in params:
            if param not in self.API_CONSTS['PARAMETERS']:
                raise ValueError('Invalid parameter: {}'.format(param))
    
    def check_response(self, response):

        if response.status_code != 200:
            raise ConnectionError('Failed: {}'.format(response.status_code))        
    

class GetAPIBase(APIBase):
    
    def __init__(self, API_CONSTS):
        
        super().__init__(API_CONSTS)

    def __call__(self, session, **params):
        
        self.check_params(**params)
        response = session.get(self.API_CONSTS['URL'], params=dict(**params))
        self.check_response(response)
        result = json.loads(response.text)
        
        return result


class PostAPIBase(APIBase):
    
    def __init__(self, API_CONSTS):
        
        super().__init__(API_CONSTS)
    
    def __call__(self, session, **params):
        
        self.check_params(**params)
        response = session.post(self.API_CONSTS['URL'], params=dict(**params))
        self.check_response(response)


# The following classes are only defined so that
# distinct docstrings can be assigned to each api function.


class GetFriendsIds(GetAPIBase):
          
    def __call__(self, session, **params):
        
        return super().__call__(session, **params)
        

class GetFollowersIds(GetAPIBase):

    def __call__(self, session, **params):
        
        return super().__call__(session, **params)


class GetFriendsList(GetAPIBase):
    
    def __call__(self, session, **params):
        
        return super().__call__(session, **params)
        

class GetFollowersList(GetAPIBase):
    
    def __call__(self, session, **params):

        return super().__call__(session, **params)


class GetFavorites(GetAPIBase):

    def __call__(self, session, **params):

        return super().__call__(session, **params)
        
        
class GetLists(GetAPIBase):

    def __call__(self, session, **params):

        return super().__call__(session, **params)

        
class GetUserTimeline(GetAPIBase):
            
    def __call__(self, session, **params):
        
        return super().__call__(session, **params)