"""
此算法主要用于对词向量进行降维
从而保证词向量全部转换成易于处理的二维向量，在判断关系上 更加合适
同时可以增加对比实验，在二维，三维上进行对比

Author:alancheg
Date:2017-9-6
"""
import sklearn.decomposition.pca as pca
from time import time
import gensim
import jieba
import pickle
import os


if __name__ == "__main__":

    if os.path.exists('word2d.dict'):
        pass
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

        # 将词和对应的降维向量合并到词典类型中，并且进行持久化存储 ---- #
        with open('word2d.list', 'wb') as output:
            pickle.dump(word_list, output)
            print('list saved to word2d.list')

        with open('word2d.weight', 'wb') as output:
            pickle.dump(new_word_weight, output)
            print('weight saved to word2d.weight')


        # word_2d_dict = {}
        # for i in range(len(word_list)):
        #     word_2d_dict[word_list[i]] = new_word_weight[i]
        #
        # # 使用 pickle 存储数据字典 #
        # with open('word2d.dict', 'wb', encoding='utf-8') as output:
        #     pickle.dump(word_2d_dict, output)


    # ---- 对词向量进行降维处理，从而转换成二维数据 ---- #

    # ---- 将词向量结合到树中 ---- #