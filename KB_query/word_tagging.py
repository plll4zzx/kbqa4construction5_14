# encoding=utf-8

"""

@desc: 定义Word类的结构；定义Tagger类，实现自然语言转为Word对象的方法。

import jieba-fast as jieba
"""

import jieba
import jieba.posseg as pseg
import KB_query.creatDict

class Word(object):
    def __init__(self, token, pos):
        self.token = token
        self.pos = pos


class Tagger:
    def __init__(self, dict_paths):
        # TODO 加载外部词典
        for p in dict_paths:
            jieba.load_userdict(p)

    @staticmethod
    def get_word_objects(sentence):
        """
        把自然语言转为Word对象
        :param sentence:
        :return:
        """
        sentence=KB_query.creatDict.deletePunctuate(sentence)
        return [Word(word.encode('utf-8'), tag) for word, tag in pseg.cut(sentence)]

# TODO 用于测试
if __name__ == '__main__':
    tagger = Tagger(['./externalDict/Dict.txt','./externalDict/Dict1.txt'])
    #while True:
    s='一片绿园林工程有限公司有哪些项目？'
    for i in tagger.get_word_objects(s):
        print(i.token.decode('utf-8'), i.pos)
