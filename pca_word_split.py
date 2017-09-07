"""
1. 训练获得词向量
2. 词向量降维
3. 计算 tf-idf 或者直接通过获取关键词附近的词构建词袋进行处理
4. 进行树存储

Author:alancheg
Date:2017-9-7
"""
import sklearn.decomposition.pca as pca
from time import time
import gensim
import jieba
import pickle
import os
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from scipy import sparse


if __name__ == "__main__":

    # ==== 获取降维的词向量 ==== #
    # ---- 产生降维的权重 ---- #
    word_list = []
    word_weight = []

    if os.path.exists('word2d.list') or os.path.exists('word2d.weight'):
        # ---- 如果相关的权重已经生成完成 ---- #
        with open(r'D:\desktop\newrtree\word2d.list', 'rb') as list_file:
            word_list = list(pickle.load(list_file))
            print('word list loaded')

        with open(r'D:\desktop\newrtree\word2d.weight', 'rb') as weight_file:
            word_weight = list(pickle.load(weight_file))
            print('word weight loaded')

    else:
        # ---- 首先基于中文词库生成对应的词向量 ---- #

        # ---- 读取相关的向量模型 ---- #
        # 读取文件
        data_file = r'D:\desktop\newrtree\wiki.zh.text.simp.cut'
        model_file = r'D:\desktop\newrtree\model.old\gensim_model'

        # 加载词向量模型
        word_model = gensim.models.Word2Vec.load(model_file)

        # ---- 将相关的词词和向量的关系读取 ---- #
        # 获取了所有的词
        # todo:消除所有带字母的词
        word_list = word_model.wv.vocab
        word_list_weight = []
        for word in word_list:
            word_list_weight.append(word_model[word].tolist())

        pca_generator = pca.PCA(n_components=2)
        new_word_weight = pca_generator.fit_transform(word_list_weight)
        print(new_word_weight)

        # ---- 将词和对应的降维向量合并到词典类型中，并且进行持久化存储 ---- #
        with open('word2d.list', 'wb') as output:
            pickle.dump(word_list, output)
            print('list saved to word2d.list')

        with open('word2d.weight', 'wb') as output:
            pickle.dump(new_word_weight, output)
            print('weight saved to word2d.weight')

    # print(word_list)
    # print(word_weight)
    # for i in range(len(word_list)):
    #     print(word_list[i])
    #     print(list(word_weight)[i])

    # ==== 计算 tf-idf 值 ==== #

    # ==== 将文本的词向量转化成对应的数据结构 ==== #
    word_weight = list(word_weight)
    all_list = []
    if os.path.exists('wiki.list'):
        with open('wiki.list', 'rb') as wiki_list:
            all_list = list(pickle.load(wiki_list))
            print('wiki file loaded')
    else:
        with open(r"D:\desktop\newrtree\wiki.zh.text.simp.cut", encoding='utf-8') as reader:
            # 对于文件中的分词句子，首先转换成对应的词向量进行表示 #
            for line in list(reader)[1000]:
                line_list = []
                for word in line:
                    if word in word_list:
                        line_list.append(word_weight[word_list.index(word)])
                all_list.append(line_list)

            with open('wiki.list', 'wb') as wiki:
                pickle.dump(all_list, wiki)
                print('wiki file saved')

    # 构建一个基于 ‘土木’ ‘建筑’ 的词袋，获取相关的关键词 #


    # ==== 将文件转换为空间结构，然后进行合并存储 ==== #
