from pythainlp import word_tokenize
regex_text = lambda data: word_tokenize(data, engine='newmm')

filterCut = lambda x: x not in (":", " ", "RT", "@", "https", "://", "/", "\n")


def text_cut_word(texts):
    cut = []
    size_for = 5  # range(len(texts))
    for index in range(size_for):
        name_cut_s = list(filter(filterCut, regex_text(texts[index])))
        temp_value = 0
        for i in range(len(name_cut_s)):
            if name_cut_s[i] in ("สวย", "ดี", "น่ารัก", "ดีกว่า", "ค่ะ"):
                temp_value = temp_value + 1
            if name_cut_s[i] in ("ไม่ดี", "น่าเกียจ"):
                temp_value = temp_value - 1
        format_ = {"word": list(name_cut_s), "value": temp_value}

        cut.append(format_)
    return cut