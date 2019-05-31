import re
import pandas as pd


# each of hashtag from string to array
def handle_hashtag_csvf_to_array(hast_tag_uni):
    temp = []
    for hash in hast_tag_uni:
        ff = re.findall(r'#[A-Za-z]+', hash, re.MULTILINE)
        for j in ff:
            temp.append(j)
    return temp


# each of hashtag are array to unique hashtag with set and name == hashtag , value == freq of hashtag
def handle_hashtag_uniq_and_count(hashtag_is_arrays):
    temp_uni = list(set(hashtag_is_arrays))
    handle = lambda data, temp: {
        'value': len(list(filter(lambda s: s == data, temp))),
        'name': data
    }
    size_feq = [handle(data, hashtag_is_arrays) for data in temp_uni]
    return size_feq


# when i get many hashtag, have i want to change from json to data fraem.
# I create 2 variable for keep name and value are array, i set each column of fields for data frame.
# data is returned type are dataframe with pandas datafraem.
def handle_hashtag_name_and_value_to_df(size_feq):
    gg = []
    hh = []
    for ss in size_feq:
        gg.append(ss['name'])
        hh.append(ss['value'])
    mm = {"name": gg, "value": hh}
    return pd.DataFrame(data=mm)
