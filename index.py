from modules.controllers.twitter_api import TwitterAPI
from modules.controllers.twitter_auth import auth_session
from modules.controllers.analysis_hashtag import handle_hashtag_csvf_to_array, handle_hashtag_uniq_and_count, handle_hashtag_name_and_value_to_df
from pandas import read_csv
import matplotlib.pyplot as plt
import re
from modules.controllers.analysis_text import text_cut_word
import pandas as pd
from modules.controllers.handle_file import read_file_c, write_file_c
from modules.controllers.handle_data import handle_user_timeline_data
if __name__ == "__main__":

    auth = auth_session()
    api = TwitterAPI(auth)
    filename = './oat.json'
    data = read_file_c(filename)
    tempp = handle_user_timeline_data(data)
    df = pd.DataFrame(data=tempp)
    print(df)
