# python 2.7.5
# Wyatt Wolf

import re
from collections import namedtuple

# Base token types (keywords and single operators are given unique token names after scanning)
#                  0            1       2        3         4          5            6        7           8
tokenID_map = ['IDENT_tk', 'NUM_tk', 'KW_tk', 'OP_tk', 'EOF_tk', 'DELM_tk', 'EQEQ_tk', 'DTDTEQ_tk', 'NOTEQ_tk',
               'BARBAR_tk', 'AMPAMP_tk']
#                   9           10

keyword_names = ['begin', 'end', 'do', 'while', 'whole', 'label', 'return', 'input', 'output',
                 'program', 'warp', 'if', 'then', 'pick', 'declare', 'assign', 'func']

Token = namedtuple('Token', ['tokenID', 'tk_string', 'line_num', 'character_num'])

# maps characters to their corrosponding column
char_col_map = {' ': 2, '=': 3, ':': 4, '!': 5, '|': 6, '&': 7}

# column 8 in state table contains all chars stored here
single_char_tokens_column = ['<', '>', '+', '-', '*', '/', '^', '.', '(', ')', ',', '{', '}', ';', '[', ']']

single_char_tokens = {'<': 'LESS_tk', '>': 'GREAT_tk', '+': 'PLUS_tk', '-': 'MINUS_tk',
                      '*': 'MULT_tk', '/': 'DIV_tk', '^': 'CARROT_tk', '.': 'PERIOD_tk', '(': 'LPREN_tk',
                      ')': 'RPREN_tk', ',': 'COMMA_tk', '{': 'LBRACE_tk', '}': 'RBRACE_tk', ';': 'SMICLN_tk',
                      '[': 'LBRACK_tk', ']': 'RBRACK_tk', '=': 'EQUAL_tk', ':': 'COLON_tk'}

# state table for identifying tokens
#               0    1     2     3     4     5     6      7     8
#              dig lett   ws     =     :     !     |      &   rest
fsa_table = [[1, 2, 0, 3, 5, 7, 9, 11, 13],  # 0
             [1, 1001, 1001, 1001, 1001, 1001, 1001, 1001, 1001],  # 1
             [2, 2, 1000, 1000, 1000, 1000, 1000, 1000, 1000],  # 2
             [1003, 1003, 1003, 4, 1003, 1003, 1003, 1003, 1003],  # 3
             [1006, 1006, 1006, 1006, 1006, 1006, 1006, 1006, 1006],  # 4
             [1003, 1003, 1003, 6, 1003, 1003, 1003, 1003, 1003],  # 5
             [1007, 1007, 1007, 1007, 1007, 1007, 1007, 1007, 1007],  # 6
             [-8, -8, -8, 8, -8, -8, -8, -8, -8],  # 7
             [1008, 1008, 1008, 1008, 1008, 1008, 1008, 1008, 1008],  # 8
             [-9, -9, -9, -9, -9, -9, 10, -9, -9],  # 9
             [1009, 1009, 1009, 1009, 1009, 1009, 1009, 1009, 1009],  # 10
             [-10, -10, -10, -10, -10, -10, -10, 12, -10],  # 11
             [1010, 1010, 1010, 1010, 1010, 1010, 1010, 1010, 1010],  # 12
             [1003, 1003, 1003, 1003, 1003, 1003, 1003, 1003, 1003]  # 13
             ]


def scan_for_tokens(lines):
    new_token = ''
    current_state = 0
    token_list = []

    for ln in range(len(lines)):
        for cn in range(len(lines[ln])):
            # print ('current state: ', current_state)
            current_state = get_new_state(current_state, lines[ln][cn])

            # sometimes we pick up a leading white space so this removes it
            if new_token == ' ':
                new_token = ''

            # current_state set to 5000 when char_to_col(state, char) method cannot determine col for character
            if current_state > 4000:
                print('Error! Line:'+str(ln+1) + ' Char:' + str(cn + 1) + ' Unrecognized character: ' + lines[ln][cn])
                exit(1)

            # errors specific to character sequences. ex: '!='
            if current_state < 0:
                print('Error number: ' + str(current_state))
                print('Unexpected character on line ' + str(ln + 1) + ' character ' + str(cn + 1))
                exit(1)

            # final or base token identified
            elif current_state > 999:
                print(tokenID_map[current_state - 1000] + ' ' + new_token + '    code ' + str(current_state))
                #  TODO add token truple to list not just token string
                token_list.append(new_token)
                new_token = lines[ln][cn]
                current_state = 0
                current_state = get_new_state(current_state, lines[ln][cn])

            # add character to token in progress
            elif current_state != 0:
                new_token += lines[ln][cn]


# driver for char_col_map
def char_to_col(character):
    if re.match("^[0-9]", character):
        return 0

    elif re.match("^[A-Za-z]", character):
        return 1

    elif character in char_col_map:
        return char_col_map.get(character)

    elif single_char_tokens_column.__contains__(character):
        return 8
    else:
        return 5000


# returns int value at table
def get_new_state(state, character):
    col = char_to_col(character)

    if col > 1000:
        return 5000
    else:
        new_state = fsa_table[state][col]
        return new_state
