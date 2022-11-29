# Python 2.7.5
# Wyatt Wolf

import sys


# get command line arguments, or input from user if no arguments are specified.
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


class SourceInput:

    def __init__(self):
        self.input_as_list = get_args_input()

        self.in_file_name = 'kb'
        if len(sys.argv) == 2:
            self.in_file_name = sys.argv[1]



