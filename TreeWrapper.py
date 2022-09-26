# python 2.7.5
# wyatt wolf
# Uses modified code from https://github.com/siddhesh10/Ternary_search_tree/blob/master/ternary_search_tree.py

from TriNode import Node


class Trie:
    # a simple wrapper
    root = None

    def __init__(self, string):
        self.n = Node(string)
        self.append(string)

    def append(self, string):
        self.root = self.n.insert(self.root, string)

    def contains(self, string):
        return self.n.search(self.root, string)

    def inorder_to_file(self):
        self.root.inorder(self.root, 0)

    def postorder_to_file(self):
        self.root.postorder(self.root, 0)

    def preorder_to_file(self):
        self.root.preorder(self.root, 0)

    def traverse_to_file(self):
        self.inorder_to_file()
        self.postorder_to_file()
        self.preorder_to_file()