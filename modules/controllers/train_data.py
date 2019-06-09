import codecs
import nltk


def train_data_():
    listpos = [
        e.strip() for e in codecs.open("pos.txt", "r", "utf-8").readlines()
    ]
    listneg = [
        e.strip() for e in codecs.open("neg.txt", "r", "utf-8").readlines()
    ]
    print(1)
    pos1 = ["pos"] * len(listpos)
    neg1 = ["neg"] * len(listneg)
    print(2)
    training_data = list(zip(listpos, pos1)) + list(zip(listneg, neg1))
    print(3)
    # vocabulary = set(chain(*[(set(word_tokenize(i[0]))) for i in training_data]))
    # vocabulary = set(chain(*[x for x in a if x not in [list(set(word_tokenize(i[0]))) for i in training_data]]))
    # # print(3.1)
    # # feature_set = [
    # #     ({i: (i in word_tokenize(sentence)) for i in vocabulary}, tag)
    # #     for sentence, tag in training_data
    # # ]
    # print(4)
    # classifier = nltk.NaiveBayesClassifier.train(feature_set)
    # # print(classifier)
    # print(5)
    # with open("vocabulary.data", "wb") as out_strm:
    #     dill.dump(vocabulary, out_strm)
    # out_strm.close()
    # with open("sentiment.data", "wb") as out_strm:
    #     dill.dump(classifier, out_strm)
    # out_strm.close()
    # print("OK")
