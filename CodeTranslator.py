# Python 2.7.5
# Wyatt Wolf

from NodeClass import Node
import os


class Translator:

    def __init__(self, treeroot, filename):
        self.stack = []
        self.tree_root = treeroot
        self.var_count = 0
        self.out_file_name = filename + '.asm'
        self.file = open(self.out_file_name, 'w')
        self.asm_stack_var_index = 0
        self.temp_var_number = 0

    def get_asm_tmp(self, var_name):
        return len(self.stack) - 1 - self.stack.index(var_name)

    def translate_to_asm(self):
        self.traverse_parse_tree(self.tree_root)
        self.file.write('STOP\n')
        for i in range(self.temp_var_number):
            self.file.write('TTT' + str(i) + ' = 0\n')
        print('\nVariable declarations and scope validated!')
        self.file.close()
        return

    def traverse_parse_tree(self, root):
        count = 0
        if root is None:
            return

        # iterate through children from left to right
        for child in root.children:

            # if child is a vars node, add declared vars to stack
            if child is not None and child.name == 'vars':
                count = self.process_vars_node(child)

            else:  # non-vars nodes
                # check for variable references
                if child is not None:
                    for tk in child.data:
                        if tk.tokenID == 'IDENT_tk':
                            # print('Valid ID Token FOUND: ' + tk.tk_string)
                            # make sure variable is declared before use
                            if not self.stack.__contains__(tk.tk_string):
                                print('Error!\nVariable not declared! line ' + str(tk.line_num) +
                                      ' character ' + str(tk.character_num))
                                self.file.close()
                                os.remove(self.out_file_name)
                                exit(1)
                    # variable(s) declaration / scope-check finished

                    if child.name == 'assign_nt':
                        continue
                    elif child.name == 'in_nt':
                        tmp_var_name = self.get_tmp()
                        self.file.write('READ ' + tmp_var_name + '\n')
                        self.file.write('LOAD ' + tmp_var_name + '\n')
                        self.file.write('STACKW ' +
                                        str(self.get_asm_tmp(child.data[0].tk_string)) +
                                        '\n')
                        continue
                    elif child.name == 'r':
                        # load var or int into accumulator
                        continue
                    # TODO add code generation here

                # recursive call to get next child
                self.traverse_parse_tree(child)

        for i in range(count):
            self.stack.pop()
            self.file.write('POP\n')
            self.asm_stack_var_index -= 1

    # adds all variable names in a vars node or any of its children to stack.
    # return type  is number of variables added to stack.
    def process_vars_node(self, vars_node):
        var_count = 0
        if vars_node.name == 'vars':

            # check for re-declare on variables
            if self.stack.__contains__(vars_node.data[0].tk_string):
                print('Error!\nVariable redeclaration on line ' + str(vars_node.data[0].line_num))
                self.file.close()
                os.remove(self.out_file_name)
                exit(1)

            # add variable to internal tracking stack
            # data[0] holds variable token in vars node
            self.stack.append(vars_node.data[0].tk_string)
            # increment internal tracking counter
            var_count += 1

            # add variable to asm stack
            self.push_var(vars_node.data[1].tk_string)
            # increment ASM stack index counter
            self.asm_stack_var_index += 1

            # if vars node has children, loop and collect all variable declarations
            while len(vars_node.children) > 0:
                vars_node = vars_node.children[0]
                if vars_node is None:
                    break
                if self.stack.__contains__(vars_node.data[0].tk_string):
                    print('Error!\nVariable redeclaration on line ' + str(vars_node.data[0].line_num))
                    self.file.close()
                    os.remove(self.out_file_name)
                    exit(1)
                else:
                    # add variable to internal tracking stack
                    # data[0] holds variable token in vars node
                    self.stack.append(vars_node.data[0].tk_string)

                    # increment internal tracking counter
                    var_count += 1

                    # add variable to asm stack
                    self.push_var(vars_node.data[1].tk_string)
                    self.asm_stack_var_index += 1

        return var_count

    def get_tmp(self):
        tmp_var_name = 'TTT' + str(self.temp_var_number)
        self.temp_var_number += 1
        return tmp_var_name

    def push_var(self, int_initial_value):
        # add variable to asm stack
        # data[1] holds number token in vars node
        self.file.write('PUSH\n')
        self.file.write('LOAD ' + str(int_initial_value) + '\n')
        self.file.write('STACKW 0\n')
