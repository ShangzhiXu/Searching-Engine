
# main函数

# Press the green button in the gutter to run the script.

from .Query_manager import *
import nltk
def initNLTK():
    nltk.download("wordnet")
    nltk.download("averaged_perceptron_tagger")
    nltk.download("punkt")
    nltk.download("maxnet_treebank_pos_tagger")
    nltk.download('stopwords')
    nltk.download('omw-1.4')
def main():
    #initNLTK()
    return init_queue("/Users/lxpig/PycharmProjects/SearchEngine/SearchEngine/GoAbroad/News")


