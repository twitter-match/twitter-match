import os
import json
from requests_oauthlib import OAuth1Session


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

    def get_friends_ids(self, user_id, stringify_ids=True, max_count=None, **kwargs):

        url = 'https://api.twitter.com/1.1/friends/ids.json'
        params = {'user_id': user_id, 'stringify_ids': stringify_ids, **kwargs}
        friends_ids = self.get_objects(url, params, key='ids', max_count=max_count)

        return friends_ids

    def get_followers_ids(self, user_id, stringify_ids=True, max_count=None, **kwargs):

        url = 'https://api.twitter.com/1.1/followers/ids.json'
        params = {'user_id': user_id, 'stringify_ids': stringify_ids, **kwargs}
        followers_ids = self.get_objects(url, params, key='ids', max_count=max_count)

        return followers_ids

    def get_friends_list(self, user_id, max_count=None, **kwargs):

        url = 'https://api.twitter.com/1.1/friends/list.json'
        params = {'user_id': user_id, **kwargs}
        friends_list = self.get_objects(url, params, key='users', max_count=max_count)

        return friends_list

    def get_followers_list(self, user_id, max_count=None, **kwargs):

        url = 'https://api.twitter.com/1.1/followers/list.json'
        params = {'user_id': user_id, **kwargs}
        followers_list = self.get_objects(url, params, key='users', max_count=max_count)

        return followers_list

    def get_favorites(self, user_id, **kwargs):

        url = 'https://api.twitter.com/1.1/favorites/list.json'
        params = {'user_id': user_id, **kwargs}
        favorites = self.get_result(url, params)

        return favorites

    def get_lists(self, user_id, **kwargs):

        url = 'https://api.twitter.com/1.1/lists/list.json'
        params = {'user_id': user_id, **kwargs}
        lists = self.get_result(url, params)

        return lists

    def get_tweets(self, user_id, **kwargs):

        url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        params = {'user_id': user_id, **kwargs}
        tweets = self.get_result(url, params)

        return tweets
