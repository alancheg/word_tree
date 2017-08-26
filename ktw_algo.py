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
from scipy import sparse


TF_IDF_VALUE = 0.04
if __name__ == "__main__":
    with open(r"D:\desktop\newrtree\wiki.zh.text.simp", encoding='utf-8') as reader:

        # ---- 分词 词袋 ------ #
        file_list = []
        for or_line in list(reader)[:1000]:
            # file_list.append(' '.join(jieba.cut(line)))

            # todo:首先将词向量按照词袋模型进行处理，减少后面的计算量
            # todo:词袋算法还能够再优化一下
            line = ' '.join(jieba.cut(or_line))
            new_line = []
            for item in line.split(' '):
                if item not in new_line:
                    new_line.append(item)

            min_line = ''
            for item in new_line:
                min_line += str(item)
                min_line += ' '

            print(min_line)
            file_list.append(min_line)

        # ---- tf-idf 计算 ---- #
        vectorizer = CountVectorizer()
        transformer = TfidfTransformer()
        tfidf = transformer.fit_transform(vectorizer.fit_transform(file_list))
        word = vectorizer.get_feature_names()
        weight = tfidf.toarray()

        # ---- 筛选出大于阈值的词 ---- #
        imp_words = {}
        print(len(weight))
        for i in range(len(weight)):
            print(u"-------这里输出第" + str(i) + u"类文本的词语tf-idf权重------")
            for j in range(len(word)):
                if weight[i][j] > TF_IDF_VALUE:
                    imp_words[word[j]] = weight[i][j]
                    print(word[j], weight[i][j])

        #todo: 基于这个矩阵进行计算（如何让它能够并行）
        # 将上文的矩阵转化为一个稀疏矩阵，
        # 在构建时，选择存在于矩阵中的元素作为主要的构建元素
        # 如果不存在，只能通过划分选择其他的节点进行分裂

        print('end')
