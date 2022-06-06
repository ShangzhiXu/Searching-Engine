from .File_manager import *
from .VSM_manager import *
from .nltk_manager import *
from .IntertedIndex import *

def getIndex(dirName):
    files = getDirFiles(dirName)
    files_len = {}
    invertedIndexTable = {} #
    for file in files:
        fileName = getFileName(file)
        filePath = dirName+'/'+file
        file_word_num = 0
        content = ReadLinesFromFile(filePath)
        for sentence in content:
            words = Input_purify(sentence)
            words.get_stem()
            words.delete_stopwords()
            for word in words.words_token:
                if word not in invertedIndexTable:
                    pos = {}
                    pos[fileName] = [file_word_num]
                    invertedIndexTable[word] = pos
                else:
                    if fileName not in invertedIndexTable[word]:
                        invertedIndexTable[word][fileName] = [file_word_num]
                    else:
                        invertedIndexTable[word][fileName].append(file_word_num)
                file_word_num += 1
        files_len.setdefault(fileName,0)
        files_len[fileName] = file_word_num
    writeFile(invertedIndexTable,projectpath+'/invertIndex.json')
    return [files_len,invertedIndexTable,files]