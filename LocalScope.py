# Python 2.7.5
# Wyatt Wolf

from NodeClass import Node


class Local_scope:

    def __init__(self,treeroot):
        self.stack = []
        self.tree_root = treeroot
        self.varCount = 0

    def check_scope(self):
        self.get_global_vars()
        self.preorder(self.tree_root.children[1])
        return

    def preorder(self, root):
        count = 0
        if root is None:
            return

        # iterate through children from left to right
        for child in root.children:

            # if child is a vars node, add declared vars to stack
            if child is not None and child.name == 'vars':
                count = self.get_vars(child)
                print(str(count))
            else:
                if child is not None:
                    for tk in child.data:
                        if tk.tokenID == 'IDENT_tk':
                            print('Valid ID Token FOUND: ' + tk.tk_string)
                            # make sure variable is declared before use
                            if not self.stack.__contains__(tk.tk_string):
                                print ('Error!\nVariable not declared! line ' + str(tk.line_num) +' character ' + str(tk.character_num))
                                exit(1)
                self.preorder(child)

        i = 0
        for i in range(count):
            self.stack.pop()

    def get_vars(self,vars_node):
        var_count =0
        if vars_node.name == 'vars':
            if self.stack.__contains__(vars_node.data[0].tk_string):
                print ('Error!\nVariable redeclaration on line ' + str(vars_node.data[0].line_num))
                exit(1)

            self.stack.append(vars_node.data[0].tk_string)
            var_count += 1
            while len(vars_node.children) > 0:
                vars_node = vars_node.children[0]
                if vars_node is None:
                    break
                if self.stack.__contains__(vars_node.data[0].tk_string):
                    print ('Error!\nVariable redeclaration on line ' + str(vars_node.data[0].line_num))
                    exit(1)
                else:
                    self.stack.append(vars_node.data[0].tk_string)
                    var_count += 1

        return var_count

    def get_global_vars(self):

        for child in self.tree_root.children:
            if child is not None and child.name == 'vars':
                self.stack.append(child.data[0].tk_string)

                while len(child.children) > 0:
                    child = child.children[0]
                    if child is None:
                        break
                    if self.stack.__contains__(child.data[0].tk_string):
                        print ('Error!\nVariable redeclaration on line ' + str(child.data[0].line_num))
                        exit(1)
                    else:
                        self.varCount+=1
                        self.stack.append(child.data[0].tk_string)

        print ('global vars:' + str(self.stack))

        return

