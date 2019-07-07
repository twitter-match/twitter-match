import os
import json
from requests_oauthlib import OAuth1Session


class Twitter():

    GET_USERS_FRIENDS_IDS_URL = 'https://api.twitter.com/1.1/friends/ids.json'
    GET_USERS_FOLLOWERS_IDS_URL = 'https://api.twitter.com/1.1/followers/ids.json'
    GET_USERS_FRIENDS_LIST_URL = 'https://api.twitter.com/1.1/friends/list.json'
    GET_USERS_FOLLOWERS_LIST_URL = 'https://api.twitter.com/1.1/followers/list.json'
    GET_USERS_FAVORITES_URL = 'https://api.twitter.com/1.1/favorites/list.json'
    GET_USERS_LISTS_URL = 'https://api.twitter.com/1.1/lists/list.json'
    GET_USERS_TWEETS_URL = 'https://api.twitter.com/1.1/statuses/user_timeline.json'

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

    def check_response(self, response):

        if response.status_code != 200:
            raise ConnectionError('Failed: {}'.format(response.status_code))

    def get_result(self, url, params):

        response = self.session.get(url, params=params)
        self.check_response(response)
        result = json.loads(response.text)

        return result

    def generate_results(self, url, params):

        cursor = -1
        while cursor != 0:
            result = self.get_result(
                url, params={**params, 'cursor': cursor})
            yield result
            cursor = result['next_cursor']

    def get_objects(self, url, params, key, max_count, **kwargs):

        objects = []
        for result in self.generate_results(url, params):
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

    def get_friends_ids(self, stringify_ids=True, max_count=None, **kwargs):

        url = self.GET_USERS_FRIENDS_IDS_URL
        params = {'user_id': self.user_id,
                  'stringify_ids': stringify_ids, **kwargs}
        self.friends_ids = self.get_objects(
            url, params, key='ids', max_count=max_count)

    def get_followers_ids(self, stringify_ids=True, max_count=None, **kwargs):

        url = self.GET_USERS_FOLLOWERS_IDS_URL
        params = {'user_id': self.user_id,
                  'stringify_ids': stringify_ids, **kwargs}
        self.followers_ids = self.get_objects(
            url, params, key='ids', max_count=max_count)

    def get_friends_list(self, max_count=None, **kwargs):

        url = self.GET_USERS_FRIENDS_LIST_URL
        params = {'user_id': self.user_id, **kwargs}
        self.friends_list = self.get_objects(
            url, params, key='users', max_count=max_count)

    def get_followers_list(self, max_count=None, **kwargs):

        url = self.GET_USERS_FOLLOWERS_LIST_URL
        params = {'user_id': self.user_id, **kwargs}
        self.followers_list = self.get_objects(
            url, params, key='users', max_count=max_count)

    def get_favorites(self, **kwargs):

        url = self.GET_USERS_FAVORITES_URL
        params = {'user_id': self.user_id, **kwargs}
        self.favorites = self.get_result(url, params)

    def get_lists(self, **kwargs):

        url = self.GET_USERS_LISTS_URL
        params = {'user_id': self.user_id, **kwargs}
        self.lists = self.get_result(url, params)

    def get_tweets(self, **kwargs):

        url = self.GET_USERS_TWEETS_URL
        params = {'user_id': self.user_id, **kwargs}
        self.tweets = self.get_result(url, params)
