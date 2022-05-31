from .File_manager import *
from .VSM_manager import *
from .nltk_manager import *
from .IntertedIndex import *

def init_queue(dir: object) -> object:
    VSM_base = getIndex(dir)
    files_len = VSM_base[0]
    invertedIndexTable =VSM_base[1]
    files = VSM_base[2]
    VSM_vector = getVSM(files_len, invertedIndexTable, files)
    return [VSM_vector,files_len,invertedIndexTable,files]


def start_query(setting,query_sentence,query_context):
    VSM_vector = query_context[0]
    invertedIndexTable = query_context[2]
    files = query_context[3]
    print("======================Searching Engine===========================")
    print("""
        匹配模式：
        0 默认模式，只有用户输入中包含待匹配词组，才会跳转
        1 纠错模式，修正用户输入中的错误.
        2 词干获取，用户输入可能包含不同词性，例如用户输入"playing"，
        4 去除非关键词， 去除用户输入中的例如'I'，'a'，'an'等常出现的非关键词汇.
        8 使用同义词，由于在英语中，可能用户来自不同地区，有不同习惯
        例如要同时使用：
            词干获取和去除非关键词：       输入6，也就是二者之和
            纠错模式和词干获取：          输入3，也就是二者之和""")

    print("""======================Searching Engine===========================""")
    query_set = setting
    print("=================Query mode set=================")
    query = Input_purify(query_sentence)
    set_match_setting(query_set,"default",query)

    similarity_list = {}
    for item in query.words_token:
        query_vector = getQueryVector(item,invertedIndexTable, files)
        for fileName in VSM_vector:
            similarity = cosine_similarity(query_vector,VSM_vector[fileName])
            similarity_list.setdefault(fileName,0)
            similarity_list[fileName] += similarity
            print(item)
            print(similarity_list)
        print(similarity_list)
