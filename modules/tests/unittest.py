import unittest
from modules.controllers.analysis_text import text_cut_word, find_unique_word


class UniTest(unittest.TestCase):
    def test_cut_word_array2D(self):
        sent = "สวัสดีครับ"
        cutword = text_cut_word(sent)
        self.assertEqual(cutword, ['สวัสดี', 'ครับ'])

    def test_find_uni_word(self):
        datas = ['สวยน่ารัก', 'สวย', 'น่ารักมากเลยครับ']
        textscuts = [text_cut_word(word) for word in datas]
        texts_and_value = find_unique_word(textscuts, len(textscuts))
        # print()
        self.assertEqual(texts_and_value,
                         [['สวย', 2, [0, 1]], ['น่ารัก', 2, [0, 2]],
                          ['มาก', 1, [2]], ['เลย', 1, [2]], ['ครับ', 1, [2]]])
        # vv = find_unique_word(datas, 10)
