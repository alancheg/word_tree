#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
from random import uniform
from time import time
# from performance_test import performance_test
from r_tree import *
import gensim


with open(r'./wiki.zh.text.simp.cut', 'r', encoding='utf-8') as reader:
    pass


def r_base_test(min = 25, max = 51, length = -1):

    def data_generate(path, length):
        """
        数据的格式为： img_name,feature_name,feature_num,cor_x,cor_y

        :param path: 数据文件的路径
        :param length: 测试文件的长度，为 -1 时表示取默认的文件长度
        :return: 返回 字典格式的 data
        """

        # 生成标准的位置信息
        data = {}
        data_length = 0

        with open(path, "r") as f:
            if length == -1:
                reader = list(csv.reader(f))
            else:
                reader = list(csv.reader(f))[0: length]

            data_length = len(reader) - 1

            i = 0
            for row in reader[1:]:
                # 去掉首行的标签
                [_, _, _, x, y] = row

                x = float(x)
                y = float(y)

                data[i] = {'xmin': x, 'xmax': x + 0.01, 'ymin': y, 'ymax': y + 0.01}
                i += 1

        # data_length = length
        return data

    # 基本 r 树的测试
    csv_path = r"C:\Users\alan\Desktop\index_project\data\source.csv"
    data = data_generate(csv_path, length)
    data_length = len(data.keys())

    root = Rtree(m= min, M= max)
    n = []

    for i in range(data_length):
        n.append(node(MBR = data[i], index = i))
    t0 = time()
    print("数据加载完成，总共 " + str(data_length) + " 条数据" )

    # ------------- 插入节点 -------------------------- #
    print("开始构建索引")

    for i in range(data_length):
        root = Insert(root, n[i])

    t1 = time()
    # print ('Inserting ...')
    print ("索引构建完成，总共有 " + str(data_length) + " 条数据，耗时：")
    print (t1 - t0)

    # --------- use performance_test get the avg search time ---- #
    print("m = " + str(min) + "; M = " + str(max))
    print(" r 树中 100 条随机检索的平均用时为：")
    print(performance_test(root, [800, 800], 100))

    # -------------- 节点删除 -------------------------- #
    # for i in range(100000):
    #     root = Delete(root, n[i])
    # t3 = time()
    # print ('Deleting ...')
    # print (t3 - t2)

if __name__ == "__main__":
    r_base_test()