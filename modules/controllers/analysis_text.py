from pythainlp import word_tokenize
import re
regex_text = lambda data: word_tokenize(data, engine='newmm')

filterCut = lambda x, word_not_need: re.match(r'[ก-๙]+', x
                                              ) and x not in word_not_need

#filterCut(x, word_not_need)
text_cut_word = lambda texts, word_not_need: list(
    filter(lambda x: filterCut(x, word_not_need), regex_text(texts)))

# re.findall( r'@[a-zA-Zก-๙0-9]+|#[a-zA-Zก-๙0-9]+', texts, re.MULTILINE)

#


#
#(?<=[\s>])#(\d*[A-Za-z_]+\d*)\b(?!;)
#
def find_unique_word(texts_cut, size):

    temp = []
    for text in range(size):

        for t in range(len(texts_cut[text])):
            v = texts_cut[text][t]
            ind = []
            checkIt = [vv for vv in temp if vv[0] == v]
            if (len(checkIt) == 0):
                a = 1
                ind.append(text)
                aa = [v, a, ind]
                temp.append(aa)
            else:
                for aa in temp:
                    if aa[0] == v:
                        aa[2].append(text)
                        aa[1] = len(aa[2])
    return temp
