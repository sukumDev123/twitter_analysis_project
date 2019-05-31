from modules.controllers.twitter_api import TwitterAPI
from modules.controllers.twitter_auth import auth_session
from modules.controllers.analysis import handle_hashtag_csvf_to_array, handle_hashtag_uniq_and_count, handle_hashtag_name_and_value_to_df
from pandas import read_csv
if __name__ == "__main__":

    auth = auth_session()
    read_csv = read_csv("./files_csv/bnk48.csv")

    hast_tag_uni = read_csv['hashtag']
    temp = handle_hashtag_csvf_to_array(hast_tag_uni)
    size_feq = handle_hashtag_uniq_and_count(temp)
    mm = handle_hashtag_name_and_value_to_df(size_feq)
    print(mm)
    # api = TwitterAPI(auth)
    # name = "bnk48"
    # userTimeLines = api.get_search_tweets(name)
    # userTimeLines.to_csv("./files_csv/bnk48.csv", index=True, header=True)
    # print(userTimeLines)