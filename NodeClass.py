# Python 2.7.5
# Wyatt Wolf

class Node(object):
    def __init__(self, name):
        self.name = name
        self.data = []  # tokens go here
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

    def preorder(self, root, depth):
        if root is None :
            return

        print_label = (depth == 0)

        if print_label:
            print('\nPreorder Traversal\n')

        print(' ' * depth * 3 + root.name + '()  Tokens: ' + str(root.data) + '\n')

        for child in root.children:
            self.preorder(child, depth + 1)

