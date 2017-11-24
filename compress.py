import sys
import os
from util.BinaryHeap import BinaryHeap
from util.Node import Node
import time


def compress(src, dst):
    nodes = {}
    with open(src, 'r') as fr:
        text = fr.read()
        for c in text:
            if c in nodes:
                nodes[c].value += 1
            else:
                nodes[c] = Node(c, 1)
    print('nodes complete')
    # Add in psuedo-EOF marker symbol
    # EOF = chr(255) + chr(255)
    # nodes[EOF] = Node(EOF, 1)
    num = len(nodes)  # maximum is 255, so 8 bits is enough.
    print('num: {}'.format(num))
    num_code = bin(num)[2:]
    while len(num_code) != 8:
        num_code = '0' + num_code
    q = BinaryHeap()
    for node in nodes.values():
        q.insert(node)
    min1 = q.delete()
    min2 = q.delete()
    while min2:
        q.insert(min1 + min2)
        min1 = q.delete()
        min2 = q.delete()
    root = min1
    # print(root)
    result = ''
    for char in text:
        if char in nodes:
            result += nodes[char].code
        else:
            print('Char {} not found'.format(char))

            # result += node
    header = tree_serialization(root)
    result = num_code + header + result
    cnt = 0
    while len(result) % 8 != 0:
        cnt += 1
        result += '0'
    print('cnt: {}'.format(cnt))
    cnt_code = bin(cnt)[2:]
    while len(cnt_code) != 8:
        cnt_code = '0' + cnt_code
    result = cnt_code + result

    # with open('debug.txt', 'w') as f:
    #    f.write(result)
    hexGrp = []
    # while result:
    #     hexGrp.append(result[:8])
    #     result = result[8:]
    # Cost too much time.
    i = 0
    while i < len(result):
        hexGrp.append(result[i:i + 8])
        i += 8
    print('Generate hex_group done.')
    # print(hexGrp)
    output = bytearray([int(group, 2) for group in hexGrp])
    with open(dst, 'wb') as wbf:
        wbf.write(output)


def tree_serialization(root):
    code = ''
    if root is None:
        return code
    # leaf
    if root.left is None and root.right is None:
        code += '1'
        # if len(root.key) == 2:
        #     code += '1' * 16
        # else:
        ASCII = bin(ord(root.key))[2:]  # '0b1100001'
        while len(ASCII) != 8:
            ASCII = '0' + ASCII
        code += ASCII
    # inner node
    else:
        code += '0'
    return code + tree_serialization(root.left) + tree_serialization(root.right)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python compress.py src_file dst_file')
        exit()
    if os.path.exists(sys.argv[1]):
        src_size = os.stat(sys.argv[1]).st_size
        start = time.time()
        compress(sys.argv[1], sys.argv[2])
        end = time.time()
        print('time cost:{}s'.format(end - start))
        dst_size = os.stat(sys.argv[2]).st_size
        print('Src file size: {}\nDst file size: {}\nPercent Space saved:{:.2f}% '
              .format(src_size, dst_size, (1.0 - float(dst_size) / src_size) * 100))
    else:
        print('File {} does not exist!'.format(sys.argv[1]))
