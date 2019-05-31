from tweepy import OAuthHandler, API
# import sys
# sys.path.insert(0, "/Users/sukumnilphet/python/twitter_presenter/private")
from private.twitter_token import twitter_token
twitter_token_v = twitter_token()
consumer_key = twitter_token_v['consumer_key']
consumer_secret = twitter_token_v['consumer_secret']
access_token = twitter_token_v['access_token']
access_token_secret = twitter_token_v['access_token_secret']


def auth_session():
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return API(auth)
