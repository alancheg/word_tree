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
        word_2d_dict = {}
        for i in range(len(word_list)):
            word_2d_dict[word_list[i]] = new_word_weight[i]

        pickle._dump(word_2d_dict, open('word2d.dict', 'rw', encoding='utf-8'))



    # # 通过将原始的数据文件按照行进行转化，然后以行为单元进行划分
    # # 从而将词向量模型以空间结构进行存储
    # word_data = []
    # with open(data_file, 'r', encoding='utf-8') as reader:
    #     word_data = list(reader)[0:10000]
    #
    # area_list = []
    #
    # for line in word_data:
    #     words = jieba.cut(line)
    #
    #     # 现在的模拟实验就是将数据进行按行存储
    #     # 将每行转化成一个高维空间，从而进行覆盖查询
    #     w_vec = []
    #     for w in words:
    #         # print(w)
    #
    #         # 如果当前的词不在词向量模型中，直接抛弃
    #         try:
    #             # 只采用前 6 维数据
    #             w = word_model[w].tolist()[0:6]
    #             w_vec.append(vec2cube(w))
    #         except:
    #             pass
    #
    #     # 将每一行合并成一个区域
    #     line_area = merge_area(w_vec)
    #     area_list.append(line_area)
    #
    # # 树的初始化及数据预处理
    # root = RTreeHdim()
    # node_queue = []
    # for i in range(len(area_list)):
    #     node_queue.append(RNode(mbr=area_list[i], index=i))
    # print("数据加载完成，总共有 " + str(len(area_list)) + " 条数据")
    #
    # t0 = time()
    # for i in range(len(node_queue)):
    #     root = insert(root, node_queue[i])
    # t1 = time()
    # print("索引构建耗时: " + str(t1 - t0))
    #
    # # 查询，通过用户输入的语句进行查询
    # user_query = input("请输入您的查询语句：")
    #
    # # 对于用户的输入语句，分词然后进行空间化
    # words = jieba.cut(user_query)
    # word_vec = []
    # for wd in words:
    #     # 如果当前的词不在词向量模型中，直接抛弃
    #     try:
    #         wd = word_model[wd].tolist()[0:6]
    #         word_vec.append(vec2cube(w))
    #     except:
    #         pass
    #
    # query_area = merge_area(w_vec)
    #
    # # ---------- 获取查询结果，并且计算查询时间 ------------ #
    # query_st = time()
    # query_result = root.search(query_area)
    # query_ed = time()
    # print('query time :' + str(query_ed - query_st))
    # # ------------------------------------------------- #
    #
    # for item in query_result[0:10]:
    #     print(item)
    #     print(word_data[item])
    #
    # print(len(query_result))


    # ---- 对词向量进行降维处理，从而转换成二维数据 ---- #

    # ---- 将词向量结合到树中 ---- #