# Python 2.7.5
# Wyatt Wolf
# CS4280
import sys


# get command line arguments, or get input from user if no arguments are specified.
def get_args_input():
    print("cmd line args: ", sys.argv)

    # print(sys.stdin)
    lines = []

    # no arguments so user needs to enter text
    if len(sys.argv) == 1:
        print("Use CTRL-D to submit typed text.")
        for line in sys.stdin:
            tmp = line.strip()
            tmp += ' '
            lines.append(tmp)
        sys.stdin.close()

    # file or redirect
    elif len(sys.argv) == 2:
        text_file = open(sys.argv[1], "r")
        for line in text_file:
            tmp = line.strip()
            tmp += ' '
            lines.append(tmp)
        text_file.close()

    else:
        print("Error! Unexpected number of arguments provided at run-time")
        exit(1)

    lines.append(' ')
    return lines


def clear_output_files():
    f = open('output.inorder', 'w')
    f.close()
    f = open('output.postorder', 'w')
    f.close()
    f = open('output.preorder', 'w')
    f.close()
