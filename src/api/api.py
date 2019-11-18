import json
import requests


class API:

    def __init__(self, API_CONSTS):

        self.API_CONSTS = API_CONSTS

    def check_params(self, **params):

        for param in params:
            if param not in self.API_CONSTS['PARAMETERS']:
                raise ValueError('Invalid parameter: {}'.format(param))

    def check_response(self, response):

        if response.status_code != 200:
            raise ConnectionError('Failed: {}'.format(response.status_code))


class GetAPI(API):

    def __init__(self, API_CONSTS):

        super().__init__(API_CONSTS)

    def __call__(self, session, **params):

        self.check_params(**params)
        response = session.get(self.API_CONSTS['URL'], params=dict(**params))
        self.check_response(response)
        result = json.loads(response.text)

        return result


class PostAPI(API):

    def __init__(self, API_CONSTS):

        super().__init__(API_CONSTS)

    def __call__(self, session, **params):

        self.check_params(**params)
        response = session.post(self.API_CONSTS['URL'], params=dict(**params))
        self.check_response(response)