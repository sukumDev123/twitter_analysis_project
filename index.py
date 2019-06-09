import numpy as np
import pandas as pd
import dill

from modules.controllers.handle_file import read_file_c, write_file_c
from modules.controllers.handle_data import handle_user_timeline_data
from modules.controllers.analysis_text import text_cut_word, find_unique_word, text_cut_hashtag
from modules.tests.unittest import UniTest
import unittest
import re
from modules.controllers.twitter_auth import auth_session
from modules.controllers.twitter_api import TwitterAPI
from multiprocessing import Process
from modules.controllers.association import apriori, generateRules
import matplotlib.pyplot as plt
from nltk import NaiveBayesClassifier as nbc
from pythainlp.tokenize import word_tokenize
import codecs
from itertools import chain
import nltk
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode


class VoteClass(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        choice_votea = votes.count(mode(votes))
        conf = choice_votea / len(votes)
        return conf


def show_all_text(name, vv, name_2, writeFile):
    name_format = './{}.json'.format(name)

    handlers = handle_user_timeline_data(read_file_c(name_format))
    siZe_d = len(handlers['text'])
    print(len(handlers['text']))
    word_not_need = ("")
    texts = [text_cut_word(text, word_not_need) for text in handlers['text']]
    texts_hh = list(filter(lambda x: len(x) > 0, texts))

    vv = vv
    L, suppData = apriori(texts_hh, minSupport=vv)
    rules = generateRules(L, suppData, minConf=vv)
    # print(rules)

    rules__ = [[
        list(f[0]),
        list(f[1]), '{:00.2f}%'.format(f[2] * 100), '{:00.2f}'.format(f[3])
    ] for f in rules]
    daa = pd.DataFrame(rules__, columns=['val1', 'val2', 'conf', 'liff'])
    aa = daa.sort_values(by="liff", ascending=False)
    if writeFile == True:
        aa.to_csv("./{}.csv".format(name_2))
    return aa


def show_all_hashtag(name, vv, name_2, writeFile):
    name_format = './{}.json'.format(name)
    # print()

    handlers = handle_user_timeline_data(read_file_c(name_format))
    siZe_d = len(handlers['text'])
    print(len(handlers['text']))
    word_not_need = ("")
    # print(handlers['text'])

    texts = [text_cut_hashtag(text) for text in handlers['text']]
    texts_hh = list(filter(lambda x: len(x) > 0, texts))
    vv = vv
    L, suppData = apriori(texts_hh, minSupport=vv)
    rules = generateRules(L, suppData, minConf=vv)
    rules__ = [[
        list(f[0]),
        list(f[1]), '{:00.2f}%'.format(f[2] * 100), '{:00.2f}'.format(f[3])
    ] for f in rules]
    daa = pd.DataFrame(rules__, columns=['val1', 'val2', 'conf', 'liff'])
    aa = daa.sort_values(by="liff", ascending=False)
    if writeFile == True:
        aa.to_csv("./{}.csv".format(name_2))
    return aa


def train_data_for_classifier():
    listpos = [txt.strip() for txt in open('./sentiment/pos.txt').readlines()]
    listneg = [txt.strip() for txt in open('./sentiment/neg.txt').readlines()]
    neutral = [
        txt.strip() for txt in open('./sentiment/neutral.txt').readlines()
    ]
    pos1 = ['pos'] * len(listpos)
    neg1 = ['neg'] * len(listneg)
    training_data = list(zip(listpos, pos1)) + list(zip(listneg, neg1))
    vocabulary = set(
        chain(*[word_tokenize(i[0].lower()) for i in training_data]))

    feature_set = [
        ({i: (i in word_tokenize(sentence.lower()))
          for i in vocabulary}, tag) for sentence, tag in training_data
    ]
    classifier = nbc.train(feature_set)
    return classifier, vocabulary


def count_pos_neg_neu(test_w_p):
    pos = [txt.strip() for txt in open('./sentiment/pos.txt').readlines()]
    neg = [txt.strip() for txt in open('./sentiment/neg.txt').readlines()]
    neutral = [
        txt.strip() for txt in open('./sentiment/neutral.txt').readlines()
    ]
    pos_freq = 0
    neg_freq = 0
    neutral_f = 0
    total_f = 0
    for txts in test_w_p:
        for txt in txts:
            total_f += 1
            if txt in pos:
                pos_freq += 1
            elif txt in neg:
                neg_freq += 1

            elif txt in neutral:
                neutral_f += 1

    return pos_freq, neg_freq, neutral_f, total_f


def writeFile_twitter_search(api, q, name_file):
    datas = api.get_search_cursor(q)
    print('size: {}'.format(len(datas)))
    name_file = name_file
    write_file_c(name_file, datas)


def json_write_csv(csv_path, json_read_data):
    datas = handle_user_timeline_data(json_read_data)
    toDF = pd.DataFrame(datas)
    # print(toDF)
    toDF.to_csv(csv_path)
    return datas


def prepro(txt, wanto):
    cut_cum = word_tokenize(txt)
    ff = list(
        filter(
            lambda x: x not in ("http", "https", ":", " ", '://', 't', '.',
                                'co', 'RT', '\n', '...'), cut_cum))
    return list(filter(lambda x: x in wanto, ff))


def naive_bayes_train(listpos, listneg):
    print(1)
    pos1 = ["pos"] * len(listpos)
    neg1 = ["neg"] * len(listneg)
    print(2)
    training_data = list(zip(listpos, pos1)) + list(zip(listneg, neg))

    # print(3)
    vocabulary = set(
        chain(*[(set(word_tokenize(i[0]))) for i in training_data]))
    feature_set = [({i: (i in word_tokenize(sentence))
                     for i in vocabulary}, tag)
                   for sentence, tag in training_data]
    classifier = nltk.NaiveBayesClassifier.train(feature_set)
    with open("./sentiment/vocabulary.data", "wb") as out_strm:
        dill.dump(vocabulary, out_strm)
    out_strm.close()
    with open("./sentiment/sentiment.data", "wb") as out_strm:
        dill.dump(classifier, out_strm)
    out_strm.close()
    print("OK")
    return classifier


def ggg_train():
    pos = [pos.strip() for pos in open("./sentiment/pos.txt").readlines()]
    neg = [neg.strip() for neg in open("./sentiment/neg.txt").readlines()]
    neutral = [
        neg.strip() for neg in open("./sentiment/neutral.txt").readlines()
    ]
    train_pos = pos
    train_neg = neg
    train_neutral = neutral

    training_data = list(zip(train_pos, ["pos"] * len(train_pos))) + list(
        zip(train_neg, ['neg'] * len(train_neg)))

    vocabulary = set(
        chain(*[(set(word_tokenize(i[0]))) for i in training_data]))
    feature_set = [({i: (i in word_tokenize(sentence))
                     for i in vocabulary}, tag)
                   for sentence, tag in training_data]

    classifier = nltk.NaiveBayesClassifier.train(feature_set)
    print("feature_set")
    with open("./sentiment/classifier.data", "wb") as out_strm:
        dill.dump(classifier, out_strm)
    out_strm.close()
    with open("./sentiment/vocabulary.data", "wb") as out_strm:
        dill.dump(vocabulary, out_strm)
    out_strm.close()

    # classifier = dill.load(open('./sentiment/sentiment.data', 'rb'))
    # print("classi")
    # print("ori acc:", nltk.classify.accuracy(classifier, feature_set_test))

    MNB_classifier = SklearnClassifier(MultinomialNB())
    MNB_classifier.train(feature_set)
    with open("./sentiment/MNB_classifier.data", "wb") as out_strm:
        dill.dump(MNB_classifier, out_strm)
    out_strm.close()
    # print("MNB acc:", nltk.classify.accuracy(MNB_classifier, feature_set_test))

    # print(classifier)
    # GaussianNB, BernoulliNB
    # GaussianNB_classifier = SklearnClassifier(GaussianNB())
    # GaussianNB_classifier.train(feature_set)
    # print("GaussianNB acc:",
    #       nltk.classify.accuracy(GaussianNB_classifier, feature_set_test))

    BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
    BernoulliNB_classifier.train(feature_set)
    with open("./sentiment/BernoulliNB_classifier.data", "wb") as out_strm:
        dill.dump(BernoulliNB_classifier, out_strm)
    out_strm.close()
    #    LogisticRegression, SGDClassifier
    # from sklearn.svm import SVC, LinearSVC, NuSVC

    LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
    LogisticRegression_classifier.train(feature_set)
    with open("./sentiment/LogisticRegression_classifier.data",
              "wb") as out_strm:
        dill.dump(LogisticRegression_classifier, out_strm)
    out_strm.close()
    # print(
    #     "LogisticRegression acc:",
    #     nltk.classify.accuracy(LogisticRegression_classifier,
    #                            feature_set_test))

    SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
    SGDClassifier_classifier.train(feature_set)
    with open("./sentiment/SGDClassifier_classifier.data", "wb") as out_strm:
        dill.dump(SGDClassifier_classifier, out_strm)
    out_strm.close()
    # print("SGDClassifier acc:",
    #       nltk.classify.accuracy(SGDClassifier_classifier, feature_set_test))
    # SVC_classifier = SklearnClassifier(SVC())
    # SVC_classifier.train(feature_set)
    # print("SVC acc:", nltk.classify.accuracy(SVC_classifier, feature_set_test))
    LinearSVC_classifier = SklearnClassifier(LinearSVC())
    LinearSVC_classifier.train(feature_set)
    with open("./sentiment/LinearSVC_classifier.data", "wb") as out_strm:
        dill.dump(LinearSVC_classifier, out_strm)
    out_strm.close()
    # print("LinearSVC acc:",
    #       nltk.classify.accuracy(LinearSVC_classifier, feature_set_test))
    NuSVC_classifier = SklearnClassifier(NuSVC())
    NuSVC_classifier.train(feature_set)
    with open("./sentiment/NuSVC_classifier.data", "wb") as out_strm:
        dill.dump(NuSVC_classifier, out_strm)
    out_strm.close()


if __name__ == "__main__":
    # pass
    # ggg_train()
    # print("NuSVC acc:",
    #   nltk.classify.accuracy(NuSVC_classifier, feature_set_test))
    classifier = dill.load(open("./sentiment/classifier.data", 'rb'))
    vocabulary = dill.load(open("./sentiment/vocabulary.data", 'rb'))
    NuSVC_classifier = dill.load(
        open("./sentiment/NuSVC_classifier.data", 'rb'))
    LinearSVC_classifier = dill.load(
        open("./sentiment/LinearSVC_classifier.data", 'rb'))
    SGDClassifier_classifier = dill.load(
        open("./sentiment/SGDClassifier_classifier.data", 'rb'))
    MNB_classifier = dill.load(open("./sentiment/MNB_classifier.data", 'rb'))
    BernoulliNB_classifier = dill.load(
        open("./sentiment/BernoulliNB_classifier.data", 'rb'))
    LogisticRegression_classifier = dill.load(
        open("./sentiment/LogisticRegression_classifier.data", 'rb'))
    vote_classify = VoteClass(classifier, NuSVC_classifier,
                              LinearSVC_classifier, SGDClassifier_classifier,
                              MNB_classifier, BernoulliNB_classifier,
                              LogisticRegression_classifier)

    # print("vote_classify acc:",
    #       nltk.classify.accuracy(vote_classify, feature_set_test))
    text_is = [
        'ผมนี้เป็นคนดีมากก', 'คุณมันคนไม่ดี', 'หนังดีนะแต่แย่เหมือนกันนะ',
        'เมื่อก่อนอะ แต่ตอนนี้คุณมันคนไม่ดีมาก', 'เมื่อก่อนอะแต่นี่เลว'
    ]
    #============
    # text_is = pd.read_csv("./files_csv/singer.csv")
    date_too = {'sentiment': [], 'texts': [], 'conf': []}
    indexx = 0
    for txt in text_is:
        asd = {i: (i in text_cut_word(txt, "")) for i in vocabulary}
        print("Classify : ", vote_classify.classify(asd), '\n', 'text: ', txt,
              "\nconf:", vote_classify.confidence(asd))
        indexx += 1

        print("index: ", indexx)
        date_too['sentiment'].append(vote_classify.classify(asd))
        date_too['texts'].append(txt)
        date_too['conf'].append(vote_classify.confidence(asd))

    # ggg = pd.DataFrame(date_too)
    # # ggg.
    # ggg.to_csv("./files_csv/wather_ss.csv")
    # print(ggg[:100])
