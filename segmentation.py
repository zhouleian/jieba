# coding=utf-8

import jieba
import jieba.analyse
import os
import sys,csv
import jieba.posseg as pseg
sys.path.append('../')
jieba.load_userdict('userdict.txt')


def readText(num):
    '''
    raw = 返回文本的原始内容
    textPath = 文本所在的路径
       '''
    textPath = os.getcwd() + '/12-2/1-200'
    os.chdir(textPath)
    textName = str(num) + '.txt'
    # print textName
    f = open(textName, 'r')
    raw = f.read()
    f.close()
    return raw


def segmentation(num, raw):
    '''
    对文本进行分词相关处理，保存到num-seg.txt中
    segList = 对文本进行分词
    words = 分词处理后的纯文本
    '''
    segList = pseg.cut(raw)
    words = []
    for w in segList:
        if w.word != '\n':  #去掉空行
            words.append(w.word)
    return words


def mdcode(str):
    '''中文乱码问题的解决'''
    for c in ('utf-8', 'gdb', 'gb2312'):
        try:
            return str.decode(c).encode('utf-8')
        except:
            pass
    return 'unknown'

def stopWordsRm(num, words):
    '''
    返回去除停用词的文本
    stopWords = 读取停用词文件，保存到列表stopWords
    '''
    #print words
    stopWordsPath = sys.path[0]
    os.chdir(stopWordsPath)
    stopWords =[line.rstrip() for line in open('stopWords.txt')]
    cleanTokens =[]
    for w in words:
        w = w.encode('utf-8')
        if w not in stopWords:
            #print type(w)
            #排除文本中的数字,字母和浮点数
            if not w.isdigit() and not w.isalnum() and ('.' not in w):
                cleanTokens.append(w)
    segPath = sys.path[0] + '/seg_result'
    os.chdir(segPath)
    f = open(str(num) + '-seg.txt', 'w+')
    for word in cleanTokens:
        f.write(word+'\n')
    f.close()
    return cleanTokens

def worker(num):
    '''
    textRaw = 文档原始的内容
    '''
    textRaw = readText(num)
    words = segmentation(num, textRaw)
    #print 'words[0] = ',words[0]
    stopWordsRm(num,words)
def main():
    num = 1
    worker(num)

if __name__=='__main__':
    main()