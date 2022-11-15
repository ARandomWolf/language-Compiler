# python 2.7.5
# Wyatt Wolf


if __name__ == '__main__':

    from Input import get_args_input
    from Scanner import *
    from Parser import *
    from LocalScope import *

    # get input into list of lines
    input_text = get_args_input()

    # remove comments (replaces with white space to preserve file structure)
    input_text = remove_comments(input_text)

    # scan lines for tokens
    token_list = scan_for_tokens(input_text)

    # display
    # print_token_list(token_list)

    # initialize parser object
    parser = Parser(token_list)

    # parse token list into n-ary tree
    parser.parse_token_list()

    # print tree
    parser.print_preorder()

    scope_check = Local_scope(parser.parse_tree)
    scope_check.check_scope()