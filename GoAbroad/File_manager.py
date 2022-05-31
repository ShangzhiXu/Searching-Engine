import json
import os
import re
projectpath = os.getcwd()

def getFileName(filename):
    filename_new = re.search('(.*)\.', filename, re.M | re.I)
    return filename_new.group(1)
def ReadFromFile(filename):
    # 将数据读出
    file = open(filename,'r')
    str = file.read()
    file.close()

def ReadLinesFromFile(filename):
    # 将数据读出
    file = open(filename,'r')
    str = file.readlines()
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

