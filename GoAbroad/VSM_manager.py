import cmath

from .File_manager import *
from .VSM_manager import *
from .nltk_manager import *
from .IntertedIndex import *

"""
tf-idf
https://blog.csdn.net/weixin_43216017/article/details/86755145
"""


def getVSM(files_len, invertedIndexTable, files):
    words_all = invertedIndexTable.keys()
    VSMTable = {}
    for file in files:
        # 遍历每一个file
        fileName = getFileName(file)
        tf_idf_list = []
        for word in words_all:
            # +1的目的是防止这个词语在语料中没有出现导致分母为0的问题
            tf = 0
            if invertedIndexTable[word].get(str(fileName)) != None:
                tf = len(invertedIndexTable[word][str(fileName)]) / (files_len[str(fileName)] + 1)
            idf = cmath.log10((len(files) / len(invertedIndexTable[word])) + 1).real
            weight = 0
            if tf != 0 and idf != 0:
                weight = "%.3f" % float(tf * idf)
            tf_idf_list.append(weight)
        VSMTable[fileName] = tf_idf_list
    return VSMTable


def getQueryVector(query, invertedIndexTable, files):
    words_all = invertedIndexTable.keys()
    query_words = Input_purify(query)
    tf_idf_Vector = []

    for word in words_all:
        # +1的目的是防止这个词语在语料中没有出现导致分母为0的问题
        tf = 0
        tf = (query_words.words_token.count(word)) / (len(query_words.words_token) + 1)
        idf = cmath.log10((len(files) + 1 / len(invertedIndexTable[word])) + 1).real
        weight = 0
        if tf != 0 and idf != 0:
            weight = "%.3f" % float(tf * idf)
        tf_idf_Vector.append(weight)

    return tf_idf_Vector


""" 
 计算两个向量x和y的余弦相似度
 假定A和B是两个n维向量，A是 [A1, A2, ..., An] ，B是 [B1, B2, ..., Bn] 
 余弦值越接近1，就表明夹角越接近0度，两个向量越相似
 值越趋近于1，代表两个向量的方向越接近；越趋近于-1，他们的方向越相反；接近于0，表示两个向量近乎于正交
 """


def cosine_similarity(vector1, vector2):
    sum = 0.0
    A = 0.0
    B = 0.0
    for a, b in zip(vector1, vector2):
        A += float(a) ** 2
        B += float(b) ** 2
        sum += float(a) * float(b)
    if A == 0.0 or B == 0.0:
        return 0
    else:
        return sum / ((A ** 0.5) * (B ** 0.5))