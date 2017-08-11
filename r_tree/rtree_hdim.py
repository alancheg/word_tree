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
    在本次的实验中， level = 0 说明是叶子节点，从下往上 level 递增。
    """
    def __init__(self, mbr=None, level=0, index=None, father=None):
        if mbr is None:
            # 对于一个新的节点，其 mbr 的区域是空的
            # 同时，它们的较大较小值通过列表中的序号进行一一对应
            self.mbr = {'max': [None]*WORD_VEC_LENGTH, 'min': [None]*WORD_VEC_LENGTH}
        else:
            self.mbr = mbr
        self.level = level
        self.index = index
        self.father = father


class RTreeHdim(object):
    # 针对高维数据进行存储的 R 树
    # 在本文中，通过位置信息 mbr，level作为它的层数
    # 默认为 1 为叶子节点，m 和 M 为其子节点树的最小和最大值
    # father 作为其父节点

    def __init__(self, leaves=None, mbr=None, level=1, m=LEAF_NODE_MIN, M=LEAF_NODE_MAX, father=None):
        self.leaves = []

        if mbr is None:
            self.mbr = {'min': [None]*WORD_VEC_LENGTH, 'max': [None]*WORD_VEC_LENGTH}
        else:
            self.mbr = mbr

        self.level = level
        self.m = m
        self.M = M
        self.father = father

    # done
    def choose_leaf(self, node):
        """
        选择插入的节点
        :return:
        """

        if self.level == node.level + 1:
        # 如果当前节点的层数比要插入的节点高一层，则表明找到了合适的节点。
            return self
        else:
        # 否则对其子节点的 mbr 进行遍历，找到面积增加的最小值
            increment = [(i, space_increase(self.leaves[i].mbr, node.mbr)) for i in range(len(self.leaves))]
            res = min(increment, key=lambda x:x[1])
            return self.leaves[res[0]].chooseLeaf(node)

    # done
    def split_node(self):
        """
        节点分裂
        :return:
        """
        # 如果当前节点没有父节点，则必然需要产生父节点来容纳分裂的两个节点。

        if not self.father:
            # 父节点的层级比当前节点多1。
            self.father = RTreeHdim(level=self.level + 1, m=self.m, M=self.M)
            self.father.leaves.append(self)

        # 产生新的节点，m、M和father都与当前节点相同。
        leaf1 = RTreeHdim(level=self.level, m=self.m, M=self.M, father=self.father)
        leaf2 = RTreeHdim(level=self.level, m=self.m, M=self.M, father=self.father)

        # 调用PickSeeds为leaf1和leaf2分配子节点
        self.pick_seeds(leaf1, leaf2)

        # 遍历剩余的子节点，进行插入。
        while len(self.leaves) > 0:
            # 如果剩余的子节点插入某一组才能使该组节点数大于m，则直接全部插入进去，并调整mbr。
            if len(leaf1.leaves) > len(leaf2.leaves) and len(leaf2.leaves) + len(self.leaves) == self.m:
                for leaf in self.leaves:
                    leaf2.mbr = merge(leaf2.mbr, leaf.mbr)
                    leaf2.leaves.append(leaf)
                    leaf.father = leaf2
                self.leaves = []
                break
            if len(leaf2.leaves) > len(leaf1.leaves) and len(leaf1.leaves) + len(self.leaves) == self.m:
                for leaf in self.leaves:
                    leaf1.mbr = merge(leaf1.mbr, leaf.mbr)
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
        self.father.mbr = merge(self.father.mbr, leaf1.mbr)
        self.father.mbr = merge(self.father.mbr, leaf2.mbr)

    # done
    def pick_seeds(self, leaf1, leaf2):
        # pick_seeds 为两组节点分配子节点
        d = 0
        t1 = 0
        t2 = 0

        # 遍历所有可能的子节点组合，寻找差值最大的项
        for i in range(len(self.leaves)):
            for j in range(i + 1, len(self.leaves)):
                mbr_new = merge(self.leaves[i].mbr, self.leaves[j].mbr)

                s_new = area_calc(mbr_new)
                s1 = area_calc(self.leaves[i])
                s2 = area_calc(self.leaves[j])

                if s_new - s1 - s2 > d:
                    t1 = i
                    t2 = j
                    d = s_new - s1 - s2

        n2 = self.leaves.pop(t2)
        n2.father = leaf1
        leaf1.leaves.append(n2)
        leaf1.mbr = leaf1.leaves[0].mbr

        n1 = self.leaves.pop(t1)
        n1.father = leaf2
        leaf2.leaves.append(n1)
        leaf2.mbr = leaf2.leaves[0].mbr

    # done
    def pick_next(self, leaf1, leaf2):
        # 为两组节点分配一个子节点
        d = 0
        t = 0

        # 遍历子节点，找到插入两组节点之后面积增加差值最大的一项
        for i in range(len(self.leaves)):
            d1 = space_increase(merge(leaf1.mbr, self.leaves[i].mbr), leaf1.mbr)
            d2 = space_increase(merge(leaf2.mbr, self.leaves[i].mbr), leaf2.mbr)
            if abs(d1 - d2) > abs(d):
                d = d1 - d2
                t = i
        if d > 0:
            target = self.leaves.pop(t)
            leaf2.mbr = merge(leaf2.mbr, target.mbr)
            target.father = leaf2
            leaf2.leaves.append(target)
        else:
            target = self.leaves.pop(t)
            leaf1.mbr = merge(leaf1.mbr, target.mbr)
            target.father = leaf1
            leaf1.leaves.append(target)


    # done
    def adjust_tree(self):
        # 自底向上调整 R 树
        p = self
        while p is not None:
            # 如果当前节点的叶子节点数量超过 M，则分裂并且调整父节点的 mbr
            if len(p.leaves) > p.M:
                p.SplitNode()
            else:
                # 否则对父节点的 mbr 进行调整
                if p.father is not None:
                    p.father.mbr = merge(p.father.mbr, p.mbr)
            p = p.father

    # done
    def search(self, mbr):
        # 搜索给定的矩形范围
        result = []
        # 如果已经到达叶子节点，则在 result 中直接添加对象
        if self.level == 1:
            for leaf in self.leaves:
                if intersect(mbr, leaf.mbr):
                    result.append(leaf.index)
            return result
        # 否则对于目标 mbr 相交的子节点进行 search，并与 result 相加
        else:
            for leaf in self.leaves:
                if intersect(mbr, leaf.mbr):
                    result = result + leaf.Search(mbr)
            return result

    # done
    def find_leaf(self, node):
        # 查找给定的对象
        result = []
        # 如果当前的节点不是叶子节点，则递归寻找所有包含目标 mbr 的子节点
        if self.level != 1:
            for leaf in self.leaves:
                if contain(leaf.mbr, node.mbr):
                    result.append(leaf.FindLeaf(node))
            for x in result:
                if x is not None:
                    return x
        # 如果当前节点是叶子节点， 则直接遍历这些对象， 判断 index 是否相等， 并且返回
        else:
            for leaf in self.leaves:
                if leaf.index == node.index:
                    return self

    # done
    def condense_tree(self):
        # condense tree 对树进行压缩 暂时处理三维
        # 保存需要插入的节点
        Queue = []

        p = self
        q = self

        # done
        while p is not None:
            p.mbr = {'min': [None]*3, 'max': [None]*3}

            for leaf in p.leaves:
                p.mbr = merge(p.mbr, leaf.mbr)
            if len(p.leaves) < self.m and p.father is not None:
                p.father.leaves.remove(p)
                if len(p.leaves) is not 0:
                    Queue += p.leaves
            q = p
            p = p.father

        for node in Queue:
            q = insert(q, node)

    # done
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


# done
def area_calc(mbr):
    # 计算 新的面积
    vo = 1
    for i in range(mbr['min']):
        vo *= mbr['max'][i] - mbr['min'][i]
    return vo


# done
def insert(root, node):
    # 插入新的节点，返回更新后的根节点
    target = root.choose_leaf(node)
    node.father = target
    target.leaves.append(node)

    target.mbr = merge(target.mbr, node.mbr)
    target.adjust_tree()
    if root.father is not None:
        root = root.father

    return root


# done
def delete(root, node):
    # 删除目标对象，返回更新后的根节点
    target = root.find_leaf(node)
    if target is None:
        print("no result")
        return root
    target.leaves.remove(node)
    target.condense_tree()
    root = root.condense_root()
    return root


# done
def merge(mbr1, mbr2):
    """
    合并算法 v2，将两个空间进行合并
    当前所有的空间都是三维的
    :param mbr1:
    :param mbr2:
    :return:
    """

    # 如果其中有一个为空的元素，那说明这个空间是初始的，直接选择另外一个
    if mbr1['min'][0] is None:
        return mbr2
    if mbr2['min'][0] is None:
        return mbr1

    # 用 lambda 进行了改写，可能会出现问题
    return {'min': [lambda i:min(mbr1['min'][i], mbr2['min'][i]), [i for i in range(mbr1['min'])]],
            'max': [lambda i:max(mbr1['max'][i], mbr2['max'][i]), [i for i in range(mbr1['max'])]]}


# done
def intersect(mbr1, mbr2):
    """
    判断两个空间是否有交集，其实和三维的处理方法一样
    先只考虑三维空间
    :param mbr1:
    :param mbr2:
    :return:
    """
    def incl(num, alist):
        if alist[1] >= num >= alist[0]:
            return True

    for i in range(len(mbr1['min'])):
        list1 = [mbr2['min'][i], mbr2['max'][i]]
        list2 = [mbr1['min'][i], mbr1['max'][i]]
        if incl(list1[0], list2) or incl(list1[1], list2) or incl(list2[0], list1) or incl(list2[1], list1):
            return True

    return False


# done
def space_increase(mbr1, mbr2):
    """
    计算 mbr2 合并到 mbr1 之后 mbr1 的空间增加
    暂时只使用于三维空间
    :param mbr1: 空间1
    :param mbr2: 空间2
    :return:
    """
    def vulome(mbr):
        vo = 1
        for i in range(mbr['min']):
            vo = vo * (mbr['max'][i] - mbr['min'][i])
        return vo

    return 1.0 * (vulome(merge(mbr1, mbr2)) - vulome(mbr1))


# done
def contain(mbr1, mbr2):
    """
    :param mbr1: 主要
    :param mbr2: 从属
    :return: 如果 mbr1 包含了 mbr2 ,返回 True ，否则返回 False
    """
    for i in range(mbr1['min']):
        if not mbr2['min'][i] >= mbr1['min'][i] and mbr2['max'][i] <= mbr1['max'][i]:
            return False

    return True
