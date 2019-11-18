from types import MethodType

from api import consts
from session import Session


class Crawler(Session):
    
    def __init__(self):
        
        super().__init__()
    
    def generate_results(self, method, **params):

        cursor = -1
        while cursor != 0:
            result = method(**{**params, **{'cursor': cursor}})
            yield result
            cursor = result['next_cursor']

    def get_objects(self, method, key, max_count, **params):

        objects = []
        for result in self.generate_results(method, **params):
            objects += result[key]
            if max_count is not None:
                if len(objects) > max_count:
                    objects = objects[:max_count]
                    break
        return objects