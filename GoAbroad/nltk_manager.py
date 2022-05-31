"""
自然语言处理模块

@ 功能：词干提取，句子分词，同义词提取，词汇匹配，短语匹配, 拼写纠错
@ 工具：nltk === Copyright (C) 2001-2021 NLTK Project
     github开源项目 === Bayes-one
"""
# -*- coding: utf-8 -*-
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.util import ngrams

from .correct import correct
from .correct import correct_food
from .correct import correct_wine


deleteSignal = [',','.',';','&',':','>',"'",'`','(',')','+','!','*','"','?','\'s']
deleteSignalForInput = [',','.',';','&',':','>',"'",'`','+','!','*','"','?',' ','``','\'','\'\'','``']
deleteWords = ['the','an','and','a','be']
class Input_purify:
    """
    此类主要用于净化用户输入，可以对用户输入：词干提取，句子分词，同义词提取，拼写纠错
    用法：
    >>> words = Input_purify("Check My acount")   #对输入字符串进行处理
    >>> words.word_correction()                   #对用户输入进行错误修正
    >>> words.delete_stopwords()                  #设置跳过停止字符
    >>> words.get_stem()                          #设置获取词干
    >>> words.use_synonym()                       #设置获取同义词

    上述函数的具体含义见函数体注释
    """
    words = ""                                  #用户输入的句子
    words_token = ""                            #将用户输入的句子拆分成单词
    words_tag = ""                              #保存用户的输入单词的词性
    words_lemma = []                            #保存用户的输入单词的同义词

    def __init__(self,input):
        """
        此函数主要用于初始化类
        :param input:
        用法：
        >>> words = Input_purify("Check My acount")
        """
        self.words = input.lower()
        self.words_token = nltk.word_tokenize(self.words)
        self.words_tag = nltk.pos_tag(self.words_token)

    def get_stem(self):
        """
        此函数主要用于获取词干
        用法：
        >>> words.get_stem()
        用户输入可能包含不同词性，例如用户输入"playing"，调用此函数之后，
        会将该单词转化为"play"并保存，默认保存为动词格式，如"I"保存为"be"

        :return:
        """
        wordnet_lemmatizer = WordNetLemmatizer()
        s = []
        for i in range(0, len(self.words_token)):
            s.append(wordnet_lemmatizer.lemmatize(self.words_token[i], pos='v'))
        self.words_token = s


    def delete_stopwords(self):
        """
        此函数主要用于清除用户输入中的stop words
        :return:;
        用法：
        >>> words.delete_stopwords()
        去除用户输入中的例如'I'，'a'，'an'等常出现的非关键词汇，依托nltk的停止词汇表得出
        删除的词汇，该表由11种语言的2400个停止字组成，见http://nltk.org/book/ch02.html
        """
        words_token = []
        for item in self.words_token:
            words_token.append(item)
        for token in words_token:
            if token in stopwords.words('english'):
                self.words_token.remove(token)
            elif token in deleteWords:
                self.words_token.remove(token)
            if token in deleteSignal or token in deleteSignalForInput:
                self.words_token.remove(token)
            if len(token) == 0:
                self.words_token.remove(token)
        self.words_tag = nltk.pos_tag(self.words_token)

    def use_synonym(self):
        """
        此函数主要用于获取用户输入的同义词
        用法：
        >>> words.use_synonym()
        由于在英语中，可能用户来自不同地区，有不同习惯，依托ntlk的wordnet实现同义词获取
        例如用户输入"check"，调用本函数后将会保存下如"cheque""tick""stop"等穷举出来的
        同义词，脚本用户在编写时可以不需要穷举各种情况

        *** 注意：只适用于处理单个词汇，如"play"，短语如："how much"暂时不支持
        :return:
        """
        synonyms = []
        for i in range(0, len(self.words_token)):
            for syn in wordnet.synsets(self.words_token[i]):
                for lemma in syn.lemmas():
                    synonyms.append(lemma.name())
        self.words_token = synonyms;
        self.words_tag = nltk.pos_tag(self.words_token)

    def word_correction(self,field):
        """
        此函数主要用于修正用户输入中的错误
        用法：
        >>> words.word_correction(field)
        例如用户输入：cheeck，将会修改为check，用户输入：wrod修改为word
        但是对于少写一些字母，例如chck，将无法修改，因为可能的情况太多了
        机器学习依托txt文件进行训练。
        :return:
        """
        s = []
        for i in self.words_token:
            #print("input: "+i)
            if field == 'food':
                corrected = correct_food.correct(i)
            elif field == 'wine':
                corrected = correct_wine.correct(i)
            else:
                corrected = correct.correct(i)
           # print("After correction: "+corrected )
            s.append(corrected)
        self.words_token = s

class Words_Match:
    """
    类主要用于匹配用户输入中的内容
    用法：
        >>> b = ('check','account')
        >>> words_match.match(b,1)

    """
    match_size = 1               #匹配词组长度，默认为1
    words_token = ""             #将输入的句子拆分成单词
    ngram = ""                   #将用户输入穷举出所有的（match_size元组），如三元组、二元组
    ngram_list  = []             #ngram的list保存格式
    def __init__(self,input_words,match_size):
        """
        用户输入应当是Input_purify类中的words_token

        ***注意：调用本类，如果要匹配多元词组
                words_token不能是获取同义词之后的，也就是不能调用use_synonym
                否则将无法匹配

        :param input_words 用户输入
        :param match_size 穷举为n元组
        用法：
        >>> words_match = Words_Match(words.words_token,1)
        """
        self.words_token = input_words.words_token
        self.match_size = match_size

    def match(self,match_word):
        """
        用户输入要匹配的单词或短语以及单词或短语的长度（包含几个单词）
        随后本函数将穷举出words_token中所有的n元组并进行匹配
        例如：['check', 'my', 'account']穷举二元组为
        ['check', 'my']['my', 'account']两个

        :param: match_word
        :return:
        """
        self.ngram = ngrams(self.words_token,self.match_size)#穷举
        s = []
        for i in self.ngram:
            s.append(i)
        self.ngram_list = s
        for i in self.ngram_list:
            match_tuple = tuple(match_word.split(" "))
            if  match_tuple == i :
                return 1




def set_match_setting(match_setting,field,Input_purify):
        """

        :param match_setting: 匹配设置

        *********************************
        匹配模式：
        0 默认模式，只有用户输入中包含待匹配词组，才会跳转
        1 纠错模式，修正用户输入中的错误，
                例如用户输入：cheeck，将会修改为check
                用户输入：wrod修改为word
                但是对于少写一些字母，例如chck，将无法修改
        2 词干获取，用户输入可能包含不同词性，例如用户输入"playing"，
                会将该单词转化为"play"并保存，默认保存为动词格式，如"I"保存为"be"
        4 去除非关键词， 去除用户输入中的例如'I'，'a'，'an'等常出现的非关键词汇，
                依托nltk的停止词汇表得出删除的词汇，
                该表由11种语言的2400个停止字组成，
                见http://nltk.org/book/ch02.html
        8 使用同义词，由于在英语中，可能用户来自不同地区，有不同习惯，
                依托ntlk的wordnet实现同义词获取
                例如用户输入"check"，
                将会保存下如"cheque""tick""stop"等穷举出来的同义词，
                脚本用户在编写时可以不需要穷举各种情况
                注意：只适用于处理单个词汇，如"play"，短语如："how much"暂时不支持

        这里采用二进制的表示方式，windows部分API中也使用了类似方式
        例如要同时使用：
            词干获取和去除非关键词，就输入6，也就是二者之和
            纠错模式和词干获取，就输入3，也就是二者之和

        *********************************
        :param Input_purify 用户输入
        :return:
        用法：
        >>> set_match_setting(match_setting,field,purified_user_input)
        """
        bin_setting = int(bin(int(match_setting)),2)
        if bin_setting == 0b0:
            pass;
        if (bin_setting & 0b0001) != 0:
            f = field
            Input_purify.word_correction(field)
        if (bin_setting & 0b0010) != 0:
            Input_purify.get_stem()
        if (bin_setting & 0b0100) != 0:
            Input_purify.delete_stopwords()
        if (bin_setting & 0b1000) != 0:
            Input_purify.use_synonym()




