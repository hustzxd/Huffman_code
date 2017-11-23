# complete binary tree stored in an array


class BinaryHeap:
    def __init__(self):
        self.nodes = []
        pass

    def insert(self, node):
        self.nodes.append(node)
        self.bubble_up()

        return True

    def delete(self):
        if len(self.nodes) == 0:
            return None
        ret = self.nodes[0]
        self.nodes[0] = self.nodes[-1]
        self.nodes.pop()
        self.bubble_down(0, self.get_lchild_idx(0), self.get_rchild_idx(0))
        return ret

    # 1.Replace the root of the heap with the last element on the last level.
    # 2.Compare the new root with its children; if they are in the correct order, stop.
    # 3.If not, swap the element with one of its children and return to the previous step.
    # (Swap with its smaller child in a min-heap and its larger child in a max-heap.)
    def bubble_down(self, parent_idx, l_child_idx, r_child_idx):
        if self.is_valid_idx(l_child_idx) and self.is_valid_idx(r_child_idx):
            if self.is_bigger(l_child_idx, r_child_idx):
                if self.is_bigger(parent_idx, r_child_idx):
                    self.swap(parent_idx, r_child_idx)
                    parent_idx = r_child_idx
                else:
                    return
            elif self.is_bigger(parent_idx, l_child_idx):
                self.swap(parent_idx, l_child_idx)
                parent_idx = l_child_idx
            else:
                return
        elif self.is_valid_idx(l_child_idx):
            if self.is_bigger(parent_idx, l_child_idx):
                self.swap(parent_idx, l_child_idx)
                parent_idx = l_child_idx
            else:
                return
        elif self.is_valid_idx(r_child_idx):
            if self.is_bigger(parent_idx, r_child_idx):
                self.swap(parent_idx, r_child_idx)
                parent_idx = r_child_idx
            else:
                return
        else:
            return
        self.bubble_down(parent_idx, self.get_lchild_idx(parent_idx), self.get_rchild_idx(parent_idx))

    def is_bigger(self, idx, idx2):
        return self.nodes[idx].is_bigger(self.nodes[idx2])

    # 1.Add the element to the bottom level of the heap.
    # 2.Compare the added element with its parent; if they are in the correct order, stop.
    # 3.If not, swap the element with its parent and return to the previous step.
    def bubble_up(self):
        child_idx = len(self.nodes) - 1
        parent_idx = self.get_parent_index(child_idx)
        while self.is_valid_idx(parent_idx) and self.is_bigger(parent_idx, child_idx):
            self.swap(parent_idx, child_idx)
            child_idx = parent_idx
            parent_idx = self.get_parent_index(child_idx)

    def swap(self, idx, idx2):
        temp = self.nodes[idx]
        self.nodes[idx] = self.nodes[idx2]
        self.nodes[idx2] = temp

    def get_parent(self, child_index):
        if child_index > 0:
            return self.nodes[self.get_parent_index(child_index)]
        else:
            return None

    def is_valid_idx(self, idx):
        if idx >= len(self.nodes) or idx < 0:
            return False
        return True

    def get_lchild_idx(self, parent_idx):
        return 2 * parent_idx + 1

    def get_rchild_idx(self, parent_idx):
        return 2 * parent_idx + 2

    def get_parent_index(self, child_index):
        return int((child_index - 1) / 2)
