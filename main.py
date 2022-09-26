# python 2.7.5
# Wyatt Wolf
# CS4782


if __name__ == '__main__':
    from TreeWrapper import Trie
    from inOutFunctions import *

    # get input into list of words
    input_text = get_args_input()
    print (input_text)

    # initialize tree object
    parse_tree = Trie(input_text[0])

    # add rest of input into tree
    for index in range(1, len(input_text)):
        parse_tree.append(input_text[index])

    # reset files to blank (empty)
    clear_output_files()

    # calls preorder_to_file(), postorder_to_file(), inorder_to_file()
    parse_tree.traverse_to_file()
