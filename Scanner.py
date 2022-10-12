# python 2.7.5
# Wyatt Wolf

import re

# enumerated imports for readability
from Tokens import Token
from Tokens import single_char_tokens
from Tokens import keyword_names
from Tokens import error_messages
from Tokens import char_col_map
from Tokens import basic_tokenID
from Tokens import single_char_tokens_column
from Tokens import fsa_table


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


def scan_for_tokens(lines):
    new_token = ''
    current_state = 0
    token_list = []

    for ln in range(len(lines)):
        for cn in range(len(lines[ln])):
            # print ('current state: ', current_state)
            current_state = get_new_state(current_state, lines[ln][cn])

            # sometimes we pick up a leading white space, this removes it
            if new_token == ' ':
                new_token = ''

            # catch errors & print relevant error message
            if current_state < 0:

                # character not in language
                if current_state < -99:
                    print('Error! line ' + str(ln + 1) + ' character ' + str(cn))
                    print(error_messages.__getitem__(current_state) + ' ' + lines[ln][cn])

                # unrecognized sequence of characters. ex: '!=' vs '=!'
                else:
                    print('Error! line ' + str(ln + 1) + ' character ' + str(cn))
                    print('Message: ' + error_messages.__getitem__(current_state) + lines[ln][cn - 1])

                exit(1)

            # final or base token identified
            elif current_state > 999:
                #  TODO add token truple to list not just token string
                token_list.append(Token(basic_tokenID[current_state - 1000], new_token, ln + 1, cn))
                new_token = lines[ln][cn]
                current_state = 0
                current_state = get_new_state(current_state, lines[ln][cn])

            # add character to token in progress
            elif current_state != 0:
                new_token += lines[ln][cn]

    token_list.append(Token(basic_tokenID[4], 'EOF', len(lines), 1))

    return add_unique_token_ids(token_list)


def add_unique_token_ids(token_list):
    for tk_num in range(len(token_list)):

        # change from general tokenID to specific ID
        # single_char_tokens variable (map type) holds single character token to tokenID map
        if token_list[tk_num].tokenID == 'OP_tk':
            tmp = Token(single_char_tokens.get(token_list[tk_num].tk_string), token_list[tk_num].tk_string,
                        token_list[tk_num].line_num, token_list[tk_num].character_num)
            token_list[tk_num] = tmp

        # Identify keyword tokens and give them specific ID.
        # keyword_names variable (map type) takes language keyword -> tokenID.
        elif token_list[tk_num].tokenID == 'IDENT_tk' and token_list[tk_num].tk_string in keyword_names:
            tmp = Token(keyword_names.get(token_list[tk_num].tk_string), token_list[tk_num].tk_string,
                        token_list[tk_num].line_num, token_list[tk_num].character_num)
            token_list[tk_num] = tmp

    return token_list


def print_token_list(token_list):
    for tk in token_list:
        print(tk)


# driver for char_col_map
# provides FSA table column for given characters
# or passes along error ( less than 0 )
def char_to_col(character):

    if re.match("^[0-9]", character):
        return 0

    elif re.match("^[A-Za-z]", character):
        return 1

    elif character in char_col_map:
        return char_col_map.get(character)

    elif single_char_tokens_column.__contains__(character):
        # return column 8 for all single character tokens
        return 8

    # large int for capturing unrecognised character error
    else:
        return -100


# returns int value at table
# passes along unrecognised character error over 1
def get_new_state(state, character):
    col = char_to_col(character)

    if col < 0:
        return col
    else:
        new_state = fsa_table[state][col]
        return new_state
