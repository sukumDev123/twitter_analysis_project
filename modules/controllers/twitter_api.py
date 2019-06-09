from pandas import DataFrame
import re
import modules.controllers.handle_data as hd
from tweepy import Cursor


class TwitterAPI:
    def __init__(self, api):
        self.api = api

    def get_user_timeline_cursor(self, name_srceen):
        temp = []
        for tweets in Cursor(self.api.user_timeline,
                             screen_name=name_srceen,
                             count=200).pages(20):
            for t in tweets:
                temp.append(t._json)
        return temp

    def get_search_cursor(self, q):
        temp = []
        for tweets in Cursor(self.api.search, q=q, count=200).pages(100):
            for gg in tweets:
                temp.append(gg._json)
        return temp
