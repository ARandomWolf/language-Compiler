# Python 2.7.5
# Wyatt Wolf
# CS4280
import sys
import re


# get command line arguments, or get input from user if no arguments are specified.
def get_args_input():
    print("cmd line args: ", sys.argv)

    # print(sys.stdin)
    lines = []

    if len(sys.argv) == 1:
        print("Use CTRL-D to submit typed text.")
        for line in sys.stdin:
            tmp = line.strip()
            tmp += ' '
            lines.append(tmp)

        sys.stdin.close()

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

    return lines


# removes comments from a list of strings
# comments are started and ended with '#' characters.
# in the space where a comment was, space is added back to retain line and character information.
def remove_comments(lines):
    is_comment = False

    # iterate over list of strings that represent each line of input
    for line_number in range(len(lines)):
        new_string = ''

        # iterate over each character in the line and remove comments
        for char_number in range(len(lines[line_number])):

            # start of comment in program
            if lines[line_number][char_number] == '#' and is_comment is False:
                is_comment = True
                new_string += ' '

            # end of comment in program
            elif lines[line_number][char_number] == '#' and is_comment:
                is_comment = False
                new_string += ' '

            elif is_comment:
                new_string += ' '

            else:
                new_string += lines[line_number][char_number]

        # replace the existing string with the new one (strings are unmutable in python)
        lines[line_number] = new_string

    return lines


def comment_free_input():
    return remove_comments(get_args_input())


def clear_output_files():
    f = open('output.inorder', 'w')
    f.close()
    f = open('output.postorder', 'w')
    f.close()
    f = open('output.preorder', 'w')
    f.close()
