# python 2.7.5
# wyatt wolf
# Uses modified code from https://github.com/siddhesh10/Ternary_search_tree/blob/master/ternary_search_tree.py

class Node:
    lo = None
    hi = None
    eq = None
    endpoint = False
    val = None

    def __init__(self, char):
        self.val = char

    def insert(self, node, string):

        if node is None:
            node = Node(string)
            return node

        if string[0] == node.val[0]:
            node.eq = self.insert(node.eq, string)
        elif string < node.val:
            node.lo = self.insert(node.lo, string)
        elif string > node.val:
            node.hi = self.insert(node.hi, string)

        return node

    def search(self, node, string):
        if node is None:
            return False

        if string < node.val:
            return self.search(node.lo, string)
        elif string > node.val:
            return self.search(node.hi, string)
        else:
            # use 'and' for matches on complete words only,
            # versus 'or' for matches on string prefixes
            if string == node.val:
                return True
            return self.search(node.eq, string)

    def inorder(self, root, depth):
        if root is None or root.val is None:
            return

        print_label = (depth == 0)

        if print_label:
            out_file = open('output.inorder', 'a')
            out_file.write('Inorder Traversal\nleft (low): \n')
            out_file.close()

        self.inorder(root.lo, depth + 1)

        if print_label:
            out_file = open('output.inorder', 'a')
            out_file.write('\nRoot: \n')
            out_file.close()

        out_file = open('output.inorder', 'a')
        out_file.write(' ' * depth * 3 + root.val + '\n')
        out_file.close()

        if print_label:
            out_file = open('output.inorder', 'a')
            out_file.write('\nMiddle (equal): \n')
            out_file.close()

        self.inorder(root.eq, depth + 1)

        if print_label:
            out_file = open('output.inorder', 'a')
            out_file.write('\nRight (high): \n')
            out_file.close()

        self.inorder(root.hi, depth + 1)

    def postorder(self, root, depth):
        if root is None or root.val is None:
            return
        print_label = (depth == 0)

        if print_label:
            out_file = open('output.postorder', 'a')
            out_file.write('Postorder Traversal\nleft (low): \n')
            out_file.close()

        self.postorder(root.lo, depth + 1)

        if print_label:
            out_file = open('output.postorder', 'a')
            out_file.write('\nMiddle (equal): \n')
            out_file.close()

        self.postorder(root.eq, depth + 1)

        if print_label:
            out_file = open('output.postorder', 'a')
            out_file.write('\nRight (high): \n')
            out_file.close()

        self.postorder(root.hi, depth + 1)

        if print_label:
            out_file = open('output.postorder', 'a')
            out_file.write('\nRoot: \n')
            out_file.close()

        out_file = open('output.postorder', 'a')
        out_file.write(' ' * depth * 3 + root.val + '\n')
        out_file.close()

    def preorder(self, root, depth):
        if root is None or root.val is None:
            return

        print_label = (depth == 0)

        if print_label:
            out_file = open('output.preorder', 'a')
            out_file.write('Preorder Traversal\nRoot: \n')
            out_file.close()

        out_file = open('output.preorder', 'a')
        out_file.write(' ' * depth * 3 + root.val + '\n')
        out_file.close()

        if print_label:
            out_file = open('output.preorder', 'a')
            out_file.write('\nleft (low):\n')
            out_file.close()

        self.preorder(root.lo, depth + 1)

        if print_label:
            out_file = open('output.preorder', 'a')
            out_file.write('\nMiddle (equal):\n')
            out_file.close()

        self.preorder(root.eq, depth + 1)

        if print_label:
            out_file = open('output.preorder', 'a')
            out_file.write('\nRight (high):\n')
            out_file.close()

        self.preorder(root.hi, depth + 1)
