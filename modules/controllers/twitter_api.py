from pandas import DataFrame
import re
import modules.controllers.handle_data as hd
from tweepy import Cursor


class TwitterAPI:
    def __init__(self, api):
        self.api = api

    def get_user_timeline(self, name_srceen):
        tweet_time_lines = self.api.user_timeline(name_srceen)
        ids_ = ([data.id for data in tweet_time_lines])
        texts = ([data.text for data in tweet_time_lines])
        created_ats = ([data.created_at for data in tweet_time_lines])
        sources = ([data.source for data in tweet_time_lines])
        favorite_counts = [data.favorite_count for data in tweet_time_lines]
        langs = [data.lang for data in tweet_time_lines]
        datas_format = hd.handle_data_direct(ids_, created_ats, texts, sources,
                                             favorite_counts, langs)
        data_frame = DataFrame(data=datas_format)
        return data_frame

    def get_search_tweets(self, search):
        tweets = self.api.search(q=search)
        ids = []
        created_ats = []
        sources = []
        texts = []
        langs = []
        favorite_counts = []
        retweet_counts = []
        geos = []
        hashtag = []
        for tweet in tweets:
            ids.append(tweet.id)
            created_ats.append(tweet.created_at)
            sources.append(tweet.source)
            texts.append(tweet.text)
            langs.append(tweet.lang)
            favorite_counts.append(tweet.favorite_count)
            retweet_counts.append(tweet.retweet_count)
            geos.append(tweet.geo)
            hashtag.append(cut_hash_tag(tweet.text))
        data_f = hd.handle_tweets_data(created_ats, ids, sources, texts, langs,
                                       favorite_counts, retweet_counts, geos,
                                       hashtag)
        data_fraem = DataFrame(data=data_f)
        # data_fraem['hashtag'] = analysis_hashtag(texts)
        # print(dir(tweets[0]))
        return data_fraem

    def get_search_data_cursor(self, search):
        ids = []
        created_ats = []
        sources = []
        texts = []
        langs = []
        favorite_counts = []
        retweet_counts = []
        geos = []
        hashtag = []
        for tweet in Cursor(self.api.search, q=search).items(200):
            ids.append(tweet.id)
            created_ats.append(tweet.created_at)
            sources.append(tweet.source)
            texts.append(tweet.text)
            langs.append(tweet.lang)
            favorite_counts.append(tweet.favorite_count)
            retweet_counts.append(tweet.retweet_count)
            geos.append(tweet.geo)
            hashtag.append(cut_hash_tag(tweet.text))
        data_f = hd.handle_tweets_data(created_ats, ids, sources, texts, langs,
                                       favorite_counts, retweet_counts, geos,
                                       hashtag)
        data_fraem = DataFrame(data=data_f)
        return data_fraem


cut_hash_tag = lambda text: re.findall(r'#[A-Za-zก-๙]+', text, re.MULTILINE)
