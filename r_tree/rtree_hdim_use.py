"""
本文主要是针对高维的词向量数据进行转换
现在的方案是将高维词向量转换成二维向量，从而能够进行空间的判定，进而使用 r 树
@author:alancheg
@date:2017-8-10
"""
import jieba
import gensim


def vec2area(word_vec1):
    # 通过为向量增加一定的长度，从而将向量转换成一个区域
    return [word_vec1, word_vec1 + 0.1]


def merge_area(area_list):
    # todo:将一组矩阵合并成一个包含所有的矩阵
    area = []

    return area

if __name__ == "__main__":
    # 读取文件
    data_file = ""
    model_file = ''

    word_model = gensim.models.Word2Vec.load(model_file)
    with open(data_file, 'r', encoding='utf-8') as reader:
        for line in reader:
            words = jieba.cut(line)

            # 现在的模拟实验就是将数据进行按行存储
            # 将每行转化成一个高维空间，从而进行覆盖查询
            w_vec = []
            for w in words:
                w_vec.append(vec2area(w_vec))

            # 将每一行合并成一个区域
            line_area = merge_area(w_vec)

            # todo:将这个区域插入 R 树中
            pass

    # 查询，通过用户输入的语句进行查询
    user_query = input("请输入您的查询语句：")

    # todo:将查询语句合并成一个区域，然后在 R 树中进行查询
