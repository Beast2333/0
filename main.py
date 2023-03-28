import copy
from itertools import combinations
import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value  # 节点的值
        self.left = left  # 左子节点
        self.right = right  # 右子节点


class Tree:
    def __init__(self):
        self.root = None
        self.node_num = 0

    def remove(self, node_num):
        queue = [self.root]
        remove_list = []
        while queue:
            seed = queue.pop()
            if seed.left:
                if seed.left.value == node_num:
                    remove_list.append((seed, 'l'))
                else:
                    queue.append(seed.left)
            if seed.right:
                if seed.right.value == node_num:
                    remove_list.append((seed, 'r'))
                else:
                    queue.append(seed.right)

        for i in remove_list:
            if i[1] == 'r':
                i[0].right = None
            else:
                i[0].left = None
        return

    # def remove_unpairs(self):
    #     queue = [self.root]
    #     remove_list = []
    #     while queue:
    #         seed = queue.pop()
    #         if seed.left:
    #             if not seed.right:
    #                 remove_list.append((seed, 'l'))
    #         if seed.right:
    #             if not seed.left:
    #                 remove_list.append((seed, 'r'))
    #     for i in remove_list:
    #         if i[1] == 'r':
    #             i[0].right = None
    #         else:
    #             i[0].left = None
    #     return

    def node_number(self):
        self.node_num += 1
        return self.node_num


class Station:

    def __init__(self, seq=()):

        self.track_num = None
        self.controller = []
        self.c_list = []
        self.c = 0  # 层数
        self.l = []
        self.t_list = []

    def init_para(self):
        n = self.track_num  # 股道数
        j = 0
        while True:
            if n >= 2 ** j:
                if n <= 2 ** (j + 1):
                    c = j + 1  # 咽喉层数
                    break
            j += 1
        self.c = c
        print("咽喉层数:" + str(c))
        target_position = 2 ** c  # 股道起始点
        l = []
        for i in range(2 ** c):  # init controller
            self.controller.append(0)
            l.append(i)
        self.l = l[0: len(l) // 2]

    def insert(self, controller):  # n 为股道数
        target_position = 2 ** self.c  # 股道起始点

        t = Tree()
        if not t.root:
            t.root = Node(t.node_number())  # 1道岔定义为根节点

        c_index = 0
        for i in range(2, target_position):
            # print("第" + str(i) + "次循环")
            queue = [t.root]
            node = Node(t.node_number())
            self.generator(queue, node)

        self.t_list.append(copy.copy(t))
        for i in range(target_position):
            queue = [self.t_list[-1].root]
            if controller[c_index]:
                node = Node(self.t_list[-1].node_number())
                self.generator(queue, node)
            else:
                self.generator(queue, Node(0))
            c_index += 1
            # print("c_index:" + str(c_index))
            # self.t_list[-1].remove(0)

    def generator(self, queue, node):
        while queue:
            cur = queue.pop(0)
            if not cur.left:
                cur.left = node
                return
            elif not cur.right:
                cur.right = node
                return
            else:
                queue.append(cur.left)
                queue.append(cur.right)

    def preorder(self, seed):
        if not seed:
            return
        print(seed.value)
        self.preorder(seed.left)
        self.preorder(seed.right)

    def main(self):
        print(2 ** self.c - self.track_num, self.c, self.track_num)
        print(self.l)
        for p in combinations(self.l, self.track_num - 2 ** (self.c - 1)):  # 控制器迭代器
            controller = copy.copy(self.controller)
            # controller = [1, 1, 0, 1, 1, 0, 1, 0]
            print(p)
            for q in p:
                controller[2*q] = 1
                controller[2*q+1] = 1
            print(controller)
            if controller in self.c_list:
                continue
            self.insert(controller)
            self.c_list.append(controller)
            # s.preorder(s.root)
        print(len(self.t_list))
        print(self.c)
        # print(self.)

        j = 0
        for i in self.t_list:
            j += 1
            i.remove(0)
            # i.remove_unpairs()
            draw(i.root, j)


def create_graph(G, node, pos={}, x=0, y=0, layer=1):
    pos[node.value] = (x, y)
    if node.left:
        G.add_edge(node.value, node.left.value)
        l_x, l_y = x - 1 / 2 ** layer, y - 1
        l_layer = layer + 1
        create_graph(G, node.left, x=l_x, y=l_y, pos=pos, layer=l_layer)
    if node.right:
        G.add_edge(node.value, node.right.value)
        r_x, r_y = x + 1 / 2 ** layer, y - 1
        r_layer = layer + 1
        create_graph(G, node.right, x=r_x, y=r_y, pos=pos, layer=r_layer)
    return G, pos


def draw(node, name):  # 以某个节点为根画图
    graph = nx.DiGraph()
    graph, pos = create_graph(graph, node)
    fig, ax = plt.subplots(figsize=(8, 10))  # 比例可以根据树的深度适当调节
    nx.draw_networkx(graph, pos, ax=ax, node_size=300)

    plt.savefig('./pic/pic' + str(name) + '.jpg')
    plt.show()


if __name__ == "__main__":
    s = Station()
    s.track_num = 9
    s.init_para()
    s.main()
