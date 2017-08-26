"""
将每行作为一个词条，分析出最关键的词
采用 tf-idf 分析出关键词
然后用 这些关键词 构建成一个高维空间
"""
import jieba
import jieba.posseg as pseg
import os
import sys
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

if __name__ == "__main__":
    with open(r"D:\desktop\newrtree\wiki.zh.text.simp", encoding='utf-8') as reader:
        file_list = []
        for line in list(reader)[:10000]:
            file_list.append(' '.join(jieba.cut(line)))

        vectorizer = CountVectorizer()
        transformer = TfidfTransformer()
        tfidf = transformer.fit_transform(vectorizer.fit_transform(file_list))
        word = vectorizer.get_feature_names()
        weight = tfidf.toarray()
        for i in range(len(weight)):
            print(u"-------这里输出第" + str(i) + u"类文本的词语tf-idf权重------")
            for j in range(len(word)):
                print(word[j], weight[i][j])



