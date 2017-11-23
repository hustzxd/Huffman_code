import sys
import os
from util.Node import Node
from util.BinaryHeap import BinaryHeap


class Decompress:
    def __init__(self, src, dst):
        self.code = ''
        self.nodes = {}
        self.src = src
        self.dst = dst
        self.output = ''
        self.root = Node()
        self.sum_leafs = None
        self.cnt_leafs = 0
        self.end = False
        # begin
        self.process()

    def process(self):
        # read code from bin file.
        self.get_code()
        self.rebuild_tree(self.root)
        self.decode(self.root)
        with open(self.dst, 'w') as wf:
            wf.write(self.output)

    def decode(self, root):
        while len(self.code) != 0:
            self.decode_one_char(root)

    def decode_one_char(self, root):
        if root.key is not None:
            self.output += root.key
            return
        if self.code[0] == '0':
            self.code = self.code[1:]
            self.decode_one_char(root.left)
            return
        if self.code[0] == '1':
            self.code = self.code[1:]
            self.decode_one_char(root.right)
            return

    def get_code(self):
        with open(self.src, 'rb') as rbf:
            bin_code = rbf.read()
        for char in bin_code:
            ASCII = bin(ord(char))[2:]
            while len(ASCII) != 8:
                ASCII = '0' + ASCII
            self.code += ASCII
        redundant_cnt = int(self.code[:8], 2)
        self.code = self.code[:-redundant_cnt]
        print('redundant size:{}'.format(redundant_cnt))
        self.sum_leafs = int(self.code[8:16], 2)
        print('leafs sum:{}'.format(self.sum_leafs))
        self.code = self.code[17:]  # size of nodes(number of tree leaf) tree root 0

    def rebuild_tree(self, root):
        if self.end:
            return
        if self.code[0] == '0':  # inner node
            if root.left is None:  # root does not have left child, so to find one.
                if root.code is None:
                    # if root.code is None, so root is an tree root node.
                    root.left = Node(code='0')
                else:  # else, it's a normal inner node, so generate the code.
                    root.left = Node(code=root.code + '0')
                self.code = self.code[1:]
                self.rebuild_tree(root.left)
            elif root.right is None:
                if root.code is None:
                    root.right = Node(code='1')
                else:
                    root.right = Node(code=root.code + '1')
                self.code = self.code[1:]
                self.rebuild_tree(root.right)
            else:
                return
        else:  # self.code[0] == '1' known as a leaf node.
            if root.left is None:
                leaf = chr(int(self.code[1:9], 2))  # '0b1100001' => 'a'
                if root.code is None:
                    root.left = Node(key=leaf, code='0')
                else:
                    root.left = Node(key=leaf, code=root.code + '0')
                self.nodes[root.left.code] = leaf  # '0' => 'a' huffman code :)
                self.code = self.code[9:]
                self.cnt_leafs += 1
                if self.cnt_leafs == self.sum_leafs:  # we have found all lead nodes, so it comes to the end.
                    self.end = True
            elif root.right is None:
                leaf = chr(int(self.code[1:9], 2))
                if root.code is None:
                    root.right = Node(key=leaf, code='1')
                else:
                    root.right = Node(key=leaf, code=root.code + '1')
                self.nodes[root.right.code] = leaf
                self.code = self.code[9:]
                self.cnt_leafs += 1
                if self.cnt_leafs == self.sum_leafs:  # we have found all lead nodes, so it comes to the end.
                    self.end = True
            else:
                return
            self.rebuild_tree(root)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: python decompress.py [src_file] [dst_file]')
        exit()
    if os.path.exists(sys.argv[1]):
        Decompress(sys.argv[1], sys.argv[2])
    else:
        print('File {} does not exist!'.format(sys.argv[1]))
