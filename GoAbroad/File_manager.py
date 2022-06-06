import json
import os
import re

projectpath = os.getcwd()

def getFileName(filename):
    end = filename.find('.')
    filename_new = filename[0:end]
    #filename_new = re.search('(.*)\.txt', filename, re.M | re.I)
    return filename_new
def ReadFromFile(filename):
    # 将数据读出
    file = open(filename,'r',encoding='ISO-8859-1')
    str = file.read()
    file.close()

def ReadLinesFromFile(filename):
    # 将数据读出
    file = open(filename,'r')
    str = ""
    try:
        str = file.readlines()
    except Exception as e:
        pass
    file.close()
    return str

def getDirFiles(path):
    #遍历目录
    files = os.listdir(path)
    for file in files:
        if file == '.DS_Store':
            files.remove(file)
    return files


def writeFile(item,filename):
    # 将数据写入到文件中
    file = open(filename,'w')
    str = json.JSONEncoder().encode(item)
    file.write(str)
    file.close()

