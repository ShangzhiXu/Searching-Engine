"""
@功能：词汇纠正模块，对输入词汇根据训练数据进行纠正
"""
import re, collections

alphabet_set = 'abcdefghijklmnopqrestuvwxyz'

def getLowerWord(text):
    """
    找到输入中的全部字母，转换为小写，搜索使用正则匹配
    用法：
    >>>>getLowerWord("text")
    :param text:
    :return:
    """
    return re.findall('[a-z]+', text.lower())


# 下面部分是网上查询得到，github开源项目 === Bayes-one
def edits1(word):
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    replaces = [a + c + b[1:] for a, b in splits for c in alphabet_set if b]
    inserts = [a + c + b for a, b in splits for c in alphabet_set]
    return set(deletes + transposes + replaces + inserts)


def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in new_words)


def known(words):
    """
    如果被查询的字符已经被查询过
    :param words:
    :return:
    """
    return set(w for w in words if w in new_words)


def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=new_words.get)


def train(new_words):
    """
    训练，输入为带训练的数据集合，根据字典进行查找，
    每发现一个单词，就加入到字典中去，
    如果字典中不存在这个单词，就新创建一个key
    如果存在这个单词，就把key的权重增加

    用法：
    >>>>new_words=train(getLowerWord(file.read()))
    :param new_words:
    :return:
    """
    model = collections.defaultdict(lambda: 1)
    for f in new_words:
        model[f] += 1
    return model

#程序运行之前提前开始训练，提高性能
#file = open("correct/wine", "r")
file = open("/Users/lxpig/PycharmProjects/chat_bot/chat_bot/src/correct/wine", "r")
new_words = train(getLowerWord(file.read()))
file.close()



