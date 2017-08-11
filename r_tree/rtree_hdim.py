"""
原始的参考 r tree 是针对低维数据的，
现在基于这个 r tree 的结构进行高维改写
@author:alancheg
@date:2017-8-9
"""

# 在本次实验中，假设词向量是通过一定的拓展进行存储，
# 同时在本次实验中，进行处理的词向量是 32 维的(可以视情况进行调整)
WORD_VEC_LENGTH = 32
# 同时，本文对 R 数中的叶子节点也进行了定义
LEAF_NODE_MAX = 8
LEAF_NODE_MIN = 3


class RNode(object):
    """
    定义节点，从而明确 R 树的存储对象。
    在本次的实验中， level = 0 说明是叶子节点，从下往上 level 递增
    """
    def __init__(self, MBR=None, level=0, index=None, father=None):
        if MBR is None:
            # 对于一个新的节点，其 MBR 的区域是空的
            # 同时，它们的较大较小值通过列表中的序号进行一一对应
            self.MBR = {'max': [None]*WORD_VEC_LENGTH, 'min': [None]*WORD_VEC_LENGTH}
        else:
            self.MBR = MBR
        self.level = level
        self.index = index
        self.father = father


# todo:高维改写
class RTreeHdim(object):
    # 针对高维数据进行存储的 R 树
    # 在本文中，通过位置信息 MBR，level作为它的层数
    # 默认为 1 为叶子节点，m 和 M 为其子节点树的最小和最大值
    # father 作为其父节点

    def __init__(self, leaves=None, MBR=None, level=1, m=LEAF_NODE_MIN, M=LEAF_NODE_MAX, father=None):
        self.leaves = []

        if MBR is None:
            self.MBR = {'min':[None]*WORD_VEC_LENGTH, 'max': [None]*WORD_VEC_LENGTH}
        else:
            self.MBR = MBR

        self.level = level
        self.m = m
        self.M = M
        self.father = father

    def choose_leaf(self, node):
        """
        选择插入的节点
        :return:
        """
        if self.level == node.level + 1:
        # 如果当前节点的层数比要插入的节点高一层，则表明找到了合适的节点。
            return self
        else:
        # 否则对其子节点的 MBR 进行遍历，找到面积增加的最小值
            increment = [(i, space_increase(self.leaves[i].MBR, node.MBR)) for i in range(len(self.leaves))]
            res = min(increment, key=lambda x:x[i])
            return self.leaves[res[0]].chooseLeaf(node)

    def split_node(self):
        """
        节点分裂
        :return:
        """
        # todo:节点分裂
        # 如果当前节点没有父节点，则必然需要产生父节点来容纳分裂的两个节点。

        if not self.father:
            # 父节点的层级比当前节点多1。
            self.father = RTree_hdim(level=self.level + 1, m=self.m, M=self.M)
            self.father.leaves.append(self)

        # 产生新的节点，m、M和father都与当前节点相同。
        leaf1 = RTree_hdim(level=self.level, m=self.m, M=self.M, father=self.father)
        leaf2 = RTree_hdim(level=self.level, m=self.m, M=self.M, father=self.father)

        # 调用PickSeeds为leaf1和leaf2分配子节点
        self.PickSeeds(leaf1, leaf2)

        # 遍历剩余的子节点，进行插入。
        while len(self.leaves) > 0:
            # 如果剩余的子节点插入某一组才能使该组节点数大于m，则直接全部插入进去，并调整MBR。
            if len(leaf1.leaves) > len(leaf2.leaves) and len(leaf2.leaves) + len(self.leaves) == self.m:
                for leaf in self.leaves:
                    leaf2.MBR = merge(leaf2.MBR, leaf.MBR)
                    leaf2.leaves.append(leaf)
                    leaf.father = leaf2
                self.leaves = []
                break
            if len(leaf2.leaves) > len(leaf1.leaves) and len(leaf1.leaves) + len(self.leaves) == self.m:
                for leaf in self.leaves:
                    leaf1.MBR = merge(leaf1.MBR, leaf.MBR)
                    leaf1.leaves.append(leaf)
                    leaf.father = leaf1
                self.leaves = []
                break

            # 否则调用PickNext为leaf1和leaf2分配下一个节点。
            self.PickNext(leaf1, leaf2)

        # 当前节点的父节点删除掉当前节点并加入新的两个节点，完成分裂。
        self.father.leaves.remove(self)
        self.father.leaves.append(leaf1)
        self.father.leaves.append(leaf2)
        self.father.MBR = merge(self.father.MBR, leaf1.MBR)
        self.father.MBR = merge(self.father.MBR, leaf2.MBR)

    def pick_seed(self):
    # 为两组节点分配子节点
        d = 0
        t1 = 0
        t2 = 0

        # 遍历所有可能的子节点组合，寻找差值最大的项
        for i in range(len(self.leaves)):
            for j in range(i + 1, len(self.leaves)):
                MBR_new = merge(self.leaves[i].MBR, self.leaves[j].MBR)
                # todo:高维空间的覆盖空间计算
                S_new = 1.0 * (MBR_new)

    def pick_next(self):
        pass

    def adjust_tree(self):
        # 自底向上调整 R 树
        p = self
        while p is not None:
            # 如果当前节点的叶子节点数量超过 M，则分裂并且调整父节点的 MBR
            if len(p.leaves) > p.M:
                p.SplitNode()
            else:
                # 否则对父节点的 MBR 进行调整
                if p.father is not None:
                    p.father.MBR = merge(p.father.MBR, p.MBR)
            p = p.father

    def search(self, MBR):
        # 搜索给定的矩形范围
        result = []
        # 如果已经到达叶子节点，则在 result 中直接添加对象
        if self.level == 1:
            for leaf in self.leaves:
                if intersect(MBR, leaf.MBR):
                    result.append(leaf.index)
            return result
        # 否则对于目标 MBR 相交的子节点进行 search，并与 result 相加
        else:
            for leaf in self.leaves:
                if intersect(MBR, leaf.MBR):
                    result = result + leaf.Search(MBR)
            return result

    def find_leaf(self, node):
        # 查找给定的对象
        result = []
        # 如果当前的节点不是叶子节点，则递归寻找所有包含目标 MBR 的子节点
        if self.level != 1:
            for leaf in self.leaves:
                if contain(leaf.MBR, node.MBR):
                    result.append(leaf.FindLeaf(node))
            for x in result:
                if x is not None:
                    return x
        # 如果当前节点是叶子节点， 则直接遍历这些对象， 判断 index 是否相等， 并且返回
        else:
            for leaf in self.leaves:
                if leaf.index == node.index:
                    return self

    def condense_tree(self):
        # condense tree 对树进行压缩
        Q = []
        p = self
        q = self

        # todo: 进行空间压缩
        while p is not None:
            p.MBR = {}

    def condense_root(self):
        # 对树的根节点进行压缩
        p = self
        q = p

        # 如果根节点只有一个子节点，则替换子节点为根节点，直到根节点为叶子节点或者根节点有多个子节点
        while len(p.leaves) == 1 and p.father is None and p.level != 1:
            p = p.leaves[0]
            q.leaves = []
            p.father = None
            q = p
        return p


def area_calc():
    # 计算 新的面积
    pass


def insert(root, node):
    # 插入新的节点，返回更新后的根节点
    pass


def delete(root, node):
    # 删除目标对象，返回更新后的根节点
    pass


def merge(MBR1, MBR2):
    """
    合并算法 v2，原始的 R 树将
    :param MBR1:
    :param MBR2:
    :return:
    """
    if MBR1['xmin'] == None:
        return MBR2
    if MBR2['xmin'] == None:
        return MBR1

    MBR = {}
    for key in MBR1.keys():
        MBR[key] = min(MBR1[key], MBR2[key])

    return MBR


def intersect(MBR1, MBR2):
    """
    判断两个空间是否有交集，其实和三维的处理方法一样
    :param MBR1:
    :param MBR2:
    :return:
    """
    for key in MBR1.keys():
        pass


def contain(MBR1, MBR2):
    # todo：判断 MBR1 和 MBR2 是否存在交集
    pass