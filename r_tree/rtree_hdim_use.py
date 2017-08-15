"""
本文主要是针对高维的词向量数据进行转换
现在的方案是将高维词向量转换成二维向量，从而能够进行空间的判定，进而使用 r 树

现在的版本是将词向量转化成三维空间进行检索
@author:alancheg
@date:2017-8-10
"""
import jieba
import gensim
from time import time
from r_tree.rtree_hdim import *


# def vec2area(word_vec1):
#     # 通过为向量增加一定的长度，从而将向量转换成一个区域
#     return [word_vec1, word_vec1 + 0.1]


def merge_area(area_list):
    """
    对于一个给定的空间列表，返回一个能够覆盖它们所有空间的集合
    :param area_list:一组空间列表
    :return:最后返回一个覆盖了它们的空间
    """

    # 判断空间的维度，初始化新的空间
    dim = len(area_list[0]['min'])
    area = {'min': [None]*dim, 'max': [None]*dim}

    # for item in area_list:
    #     for key in item.keys():
    #         if area[key] is None:
    #             area[key] = item[key]
    #         else:
    #             if area[key] < item[key]:
    #                 area[key] = item[key]

    for item in area_list:
        for i in range(len(item['min'])):
            if area['min'][i] is None:
                area['min'][i] = item['min'][i]
            elif area['min'][i] > item['min'][i]:
                area['min'][i] = item['min'][i]

            if area['max'][i] is None:
                area['max'][i] = item['max'][i]
            elif area['max'][i] < item['max'][i]:
                area['max'][i] = item['max'][i]

    return area


def vec2cube(word_vec):
    """
    直接将词向量取值进行转换，从而得出一个立方体
    :param word_vec: 需要转换的词向量
    :return: 一个以词向量进行排列的立方体
    """
    # return {'xmin': min(word_vec[0:len(word_vec) / 3]), 'xmax': max(word_vec[0:len(word_vec) / 3]),
    #         'ymin': min(word_vec[len(word_vec) / 3:(2 * len(word_vec)) / 3]),
    #         'ymax': max(word_vec[len(word_vec) / 3:(2 * len(word_vec)) / 3]),
    #         'zmin': min(word_vec[(2 * len(word_vec)) / 3:len(word_vec)]),
    #         'zmax': max(word_vec[(2 * len(word_vec)) / 3:len(word_vec)])}

    return {'min': [min(word_vec[0:int(len(word_vec) / 3)]),
                    min(word_vec[int(len(word_vec) / 3):int((2 * len(word_vec)) / 3)]),
                    min(word_vec[int((2 * len(word_vec)) / 3): len(word_vec)])],
            'max': [max(word_vec[0:int(len(word_vec) / 3)]),
                    max(word_vec[int(len(word_vec) / 3):int((2 * len(word_vec)) / 3)]),
                    max(word_vec[int((2 * len(word_vec)) / 3):len(word_vec)])]}


if __name__ == "__main__":
    # 读取文件
    data_file = r'D:\desktop\newrtree\wiki.zh.text.simp.cut'
    model_file = r'D:\desktop\newrtree\gensim_model'

    # 加载词向量模型
    word_model = gensim.models.Word2Vec.load(model_file)

    # 通过将原始的数据文件按照行进行转化，然后以行为单元进行划分，
    # 从而将词向量模型以空间结构进行存储
    with open(data_file, 'r', encoding='utf-8') as reader:
        # count = 0
        area_list = []
        for line in list(reader)[0:100]:
            words = jieba.cut(line)

            # 现在的模拟实验就是将数据进行按行存储
            # 将每行转化成一个高维空间，从而进行覆盖查询
            w_vec = []
            for w in words:
                # print(w)

                # 如果当前的词不在词向量模型中，直接抛弃
                try:
                    w = word_model[w].tolist()
                    # print('w_list')
                    # print(w)

                    w_vec.append(vec2cube(w))
                except:
                    pass


            # 将每一行合并成一个区域
            line_area = merge_area(w_vec)

            area_list.append(line_area)

    # 树的初始化及数据预处理
    root = RTreeHdim()
    n = []
    for i in range(len(area_list)):
        n.append(RNode(mbr=area_list[i], index=i))
    print("数据加载完成，总共有 " + str(len(area_list)) + " 条数据")

    t0 = time()
    for i in range(len(area_list)):
        root = insert(root, n[i])
    t1 = time()
    print("索引构建耗时: " + (t1 - t0))

    # 查询，通过用户输入的语句进行查询
    user_query = input("请输入您的查询语句：")

    # todo:将查询语句合并成一个区域，然后在 R 树中进行查询
