# python 2.7.5
# Wyatt Wolf


if __name__ == '__main__':

    from Input import SourceInput
    from Scanner import *
    from Parser import *
    from CodeTranslator import *

    # get input into list of lines

    source_input = SourceInput()

    # remove comments (replaces with white space to preserve file structure)
    input_text = remove_comments(source_input.input_as_list)

    # scan lines for tokens
    token_list = scan_for_tokens(input_text)

    # display
    # print_token_list(token_list)

    # initialize parser object
    parser = Parser(token_list)

    # parse token list into n-ary tree
    parser.parse_token_list()

    # un-comment line below to print parse tree
    # parser.print_preorder()

    # check local scope
    translator = Translator(parser.parse_tree, source_input.in_file_name)

    # Generate target language code
    translator.translate_to_asm()

