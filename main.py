# python 2.7.5
# Wyatt Wolf
# CS4280


if __name__ == '__main__':

    from Input import *
    from Tokens import *
    # get input into list of lines
    lines = comment_free_input()

    # scan lines for tokens
    scan_for_tokens(lines)



