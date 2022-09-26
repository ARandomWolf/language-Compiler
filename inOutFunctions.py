# Python 2.7.5
# Wyatt Wolf
# CS4782
import sys
import re


# get comandline arguments, or get input from user if no arguments are specified.
def get_args_input():
    print("cmd line args: ", sys.argv)

    # print(sys.stdin)
    lines = []
    if len(sys.argv) == 1:
        print("Use CTRL-D to submit typed text.")
        for line in sys.stdin:
            splitline = line.strip().split(' ')
            lines.extend(splitline)

    elif len(sys.argv) == 2:
        text_file = open(sys.argv[1], "r")
        for line in text_file:
            splitline = line.strip().split(' ')
            lines.extend(splitline)

    lines = filter(None, lines)
    for word in lines:
        if not re.match("^[A-Za-z0-9_-]*$", word):
            print('Error! Invalid character(s) entered: ' + word)
            exit(1)

    return lines


def clear_output_files():
    f = open('output.inorder', 'w')
    f.close()
    f = open('output.postorder', 'w')
    f.close()
    f = open('output.preorder', 'w')
    f.close()

