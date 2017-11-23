class Node:
    def __init__(self, key=None, value=None, code=None, left=None, right=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right
        self.code = code

    def __str__(self):
        return 'key: ({}), value: ({}) code: ({}) left: ({}) right: ({})' \
            .format(self.key, self.value, self.code, self.left, self.right)

    def __contains__(self, key):
        return self.key == key

    def __add__(self, other):
        self.forward_code('0')
        other.forward_code('1')
        return Node(self.key + other.key, self.value + other.value, None, self, other)

    def is_bigger(self, other):
        if self.value > other.value or (self.value == other.value and self.key > other.key):
            return True
        return False

    def forward_code(self, prefix_code):
        if self.code is None:
            self.code = prefix_code
        else:
            self.code = prefix_code + self.code
        if self.left is not None:
            self.left.forward_code(prefix_code)
        if self.right is not None:
            self.right.forward_code(prefix_code)


# test

if __name__ == '__main__':
    n1 = Node('c', 1)
    n2 = Node('b', 3)
    print(n1 + n2)
