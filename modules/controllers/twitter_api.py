from pandas import DataFrame
import numpy as np
import modules.controllers.handle_data as hd


class TwitterAPI:
    def __init__(self, api):
        self.api = api

    def get_user_timeline(self, name_srceen):
        tweet_time_lines = self.api.user_timeline(name_srceen)
        ids_ = np.array([data.id for data in tweet_time_lines])
        texts = np.array([data.text for data in tweet_time_lines])
        created_ats = np.array([data.created_at for data in tweet_time_lines])
        sources = np.array([data.source for data in tweet_time_lines])
        datas_format = hd.handle_data_direct(ids_, created_ats, texts, sources)
        data_frame = DataFrame(data=datas_format)
        return data_frame