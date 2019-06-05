import numpy as np
import pandas as pd
from modules.controllers.handle_file import read_file_c, write_file_c
from modules.controllers.handle_data import handle_user_timeline_data
from modules.controllers.analysis_text import text_cut_word, find_unique_word
from modules.tests.unittest import UniTest
import unittest
import re
from modules.controllers.twitter_auth import auth_session
from modules.controllers.twitter_api import TwitterAPI
from multiprocessing import Process
from modules.controllers.association import apriori, generateRules


def show_all(name, vv, name_2):
    # pp = lambda pa, num: (num - (num * pa / 100)) / num
    name_format = './{}.json'.format(name)
    handlers = handle_user_timeline_data(read_file_c(name_format))
    # handlers = [["c", 'b', 'v'], ['b', 'b', 'c'], ['c', 'v'], ['a', 'b']]
    siZe_d = len(handlers['text'])
    print(len(handlers['text']))
    word_not_need = ("")
    texts = [text_cut_word(text, word_not_need) for text in handlers['text']]
    texts_hh = list(filter(lambda x: len(x) > 0, texts))
    # print(texts_hh)
    vv = vv
    L, suppData = apriori(texts_hh, minSupport=vv)
    rules = generateRules(L, suppData, minConf=vv)
    # print(rules)

    rules__ = [[list(f[0]),
                list(f[1]), '{:06.2f}%'.format(f[2] * 100)] for f in rules]
    daa = pd.DataFrame(rules__, columns=['val1', 'val2', 'conf'])
    aa = daa.sort_values(by="conf", ascending=False)
    aa.to_csv("./{}.csv".format(name_2))
    return aa


if __name__ == "__main__":
   
    file_s = input("file : ")
    inputt = float(input("value : "))
    shh = Process(target=show_all, args=(file_s, inputt, file_s + "_file"))
    shh.start()

