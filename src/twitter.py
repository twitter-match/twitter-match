import os
import json
from requests_oauthlib import OAuth1Session

import api

class Twitter():

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

    def create_user(self, user_id):

        return User(self.session, user_id)

    def generate_results(self, api_func, **params):

        cursor = -1
        while cursor != 0:
            result = api_func(
                self.session, **{**params, **{'cursor':cursor}})
            yield result
            cursor = result['next_cursor']

    def get_objects(self, api_func, key, max_count, **params):

        objects = []
        for result in self.generate_results(api_func, **params):
            objects += result[key]
            if max_count is not None:
                if len(objects) > max_count:
                    objects = objects[:max_count]
                    break

        return objects


class User(Twitter):

    def __init__(self, session, user_id):

        if not isinstance(user_id, str):
            raise ValueError('User id must be a string.')
            
        self.session = session
        self.user_id = user_id

    def get_friends_ids(self, max_count=None, **params):
        
        self.friends_ids = self.get_objects(
            api.get_friends_ids, key='ids', max_count=max_count, 
            user_id=self.user_id, **params)

    def get_followers_ids(self, max_count=None, **params):

        self.followers_ids = self.get_objects(
            api.get_followers_ids, key='ids', max_count=max_count,
            user_id=self.user_id, **params)

    def get_friends_list(self, max_count=None, **params):
        
        self.friends_list = self.get_objects(
            api.get_friends_list, key='users', max_count=max_count,
            user_id=self.user_id, **params)

    def get_followers_list(self, max_count=None, **params):
        
        self.followers_list = self.get_objects(
            api.get_followers_list, key='users', max_count=max_count,
            user_id=self.user_id, **params)

    def get_favorites(self, **params):

        self.favorites = api.get_favorites(
            self.session, user_id=self.user_id, **params)

    def get_lists(self, **params):

        self.lists = api.get_lists(
            self.session, user_id=self.user_id, **params)

    def get_user_timeline(self, **params):

        self.timeline = api.get_user_timeline(
            self.session, user_id=self.user_id, **params)
