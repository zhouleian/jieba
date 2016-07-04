# coding=utf-8
import os
import jieba
import jieba.posseg as pseg
import sys
import string
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
"""计算TF_IDF"""
reload(sys)
sys.setdefaultencoding('utf8')

def getFileList():
    segPath = sys.path[0] + '/seg_result'
    fileList = os.listdir(segPath)
    return fileList
def tfidf(fileList):
    segPath = sys.path[0] + '/seg_result'
    corpus = [] #存取文档的分词结果
    for eachFile in fileList:
        fileName = segPath + '/' + eachFile
        f = open(fileName,'r+')
        content = f.read()
        corpus.append(content)
    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值,同时会使用默认的中文停用词
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    #创建tfidf文件夹,保存tf-idf的结果
    tfidfFilePath = os.getcwd() + '/tfidfFile'
    if not os.path.exists(tfidfFilePath):
        os.mkdir(tfidfFilePath)
    for i in range(len(weight)):
        print u"--------Writing all the tf-idf in the", i, u" file into ", tfidfFilePath + '/' + str(i) + '.txt', "--------"
        name = tfidfFilePath + '/' + string.zfill(i, 5) + '.txt'
        f = open(name,'w+')
        for j in range(len(word)):
            #f.write(word[j] + "    " + str(weight[i][j]) + "\n")
            #f.write(str(weight[i][j]) + "\n")
            f.write(word[j] + "\n")
        f.close()
        #print len(open(name,'rU').readlines())   #返回文件的行数


def main():
    fileList = getFileList()
    tfidf(fileList)
if __name__=='__main__':
    main()