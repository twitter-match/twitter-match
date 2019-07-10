import os
import yaml

from api import api

yaml_path = os.path.join(
    os.path.dirname(__file__), 'params.yml')
with open(yaml_path, 'r') as f:
    APIS_CONSTS = yaml.load(f, Loader=yaml.FullLoader)
        
get_friends_ids = api.GetFriendsIds(APIS_CONSTS['GET_FRIENDS_IDS'])
get_followers_ids = api.GetFollowersIds(APIS_CONSTS['GET_FOLLOWERS_IDS'])
get_friends_list = api.GetFriendsList(APIS_CONSTS['GET_FRIENDS_LIST'])
get_followers_list = api.GetFollowersList(APIS_CONSTS['GET_FOLLOWERS_LIST'])
get_favorites = api.GetFavorites(APIS_CONSTS['GET_FAVORITES'])
get_lists = api.GetLists(APIS_CONSTS['GET_LISTS'])
get_user_timeline = api.GetUserTimeline(APIS_CONSTS['GET_USER_TIMELINE'])