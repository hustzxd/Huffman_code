import sys
import os
from util.Node import Node
import time


class Decompress:
    def __init__(self, src, dst):
        self.code = []
        self.nodes = {}
        self.src = src
        self.dst = dst
        self.output = []
        self.root = Node()
        self.sum_leafs = None
        self.cnt_leafs = 0
        self.end = False
        self.idx = 0
        # begin
        self.process()

    def process(self):
        # read code from bin file.
        self.get_code()
        print('get code done.')
        self.rebuild_tree(self.root)
        print('rebuild tree done.')
        self.decode(self.root)
        print('decode done.')
        with open(self.dst, 'w') as wf:
            wf.write(''.join(self.output))
        print('write file done.')

    def decode(self, root):
        self.idx = 0
        l = len(self.code)
        while self.idx < l:
            self.decode_one_char(root)

    def decode_one_char(self, root):
        if root.key is not None:
            self.output += root.key
            return
        if self.code[self.idx] == '0':
            self.idx += 1
            self.decode_one_char(root.left)
            return
        if self.code[self.idx] == '1':
            # self.code = self.code[1:]
            self.idx += 1
            self.decode_one_char(root.right)
            return

    def get_code(self):
        with open(self.src, 'rb') as rbf:
            bin_code = rbf.read()
        for char in bin_code:
            ASCII = bin(ord(char))[2:]
            while len(ASCII) != 8:
                ASCII = '0' + ASCII
            self.code += list(ASCII)
        redundant_cnt = int(''.join(self.code[:8]), 2)
        if redundant_cnt != 0:
            self.code = self.code[:-redundant_cnt]
        # print('redundant size:{}'.format(redundant_cnt))
        print('{}'.format(''.join(self.code[8:16])))
        self.sum_leafs = int(''.join(self.code[8:16]), 2)
        print('leafs sum:{}'.format(self.sum_leafs))
        self.code = self.code[17:]  # size of nodes(number of tree leaf) tree root 0

    def rebuild_tree(self, root):
        if root.left is None:  # root does not have left child, so to find one.
            if self.end:
                return
            if root.code is None:
                root.left = Node(code='0')
            else:
                root.left = Node(code=root.code + '0')

            if self.code[0] == '1':  # leaf
                leaf = chr(int(''.join(self.code[1:9]), 2))
                self.code = self.code[9:]
                root.left.key = leaf

                self.cnt_leafs += 1
                if self.cnt_leafs == self.sum_leafs:
                    self.end = True
                self.rebuild_tree(root)
            else:  # inner node
                self.code = self.code[1:]
                self.rebuild_tree(root.left)
        if root.right is None:
            if self.end:
                return
            if root.code is None:
                root.right = Node(code='1')
            else:
                root.right = Node(code=root.code + '1')
            if self.code[0] == '1':
                leaf = chr(int(''.join(self.code[1:9]), 2))
                self.code = self.code[9:]
                root.right.key = leaf
                self.cnt_leafs += 1
                if self.cnt_leafs == self.sum_leafs:
                    self.end = True
                return
            else:
                self.code = self.code[1:]
                self.rebuild_tree(root.right)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: python decompress.py [src_file] [dst_file]')
        exit()
    if os.path.exists(sys.argv[1]):
        start = time.time()
        Decompress(sys.argv[1], sys.argv[2])
        end = time.time()
        print('Time cost: {:.2f}s'.format(end - start))
    else:
        print('File {} does not exist!'.format(sys.argv[1]))
