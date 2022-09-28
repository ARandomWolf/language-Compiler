# python 2.7.5
# Wyatt Wolf

import re
from collections import namedtuple

#                  0            1       2        3         4          5            6        7           8
tokenID_map = {'IDENT_tk', 'NUM_tk', 'KW_tk', 'OP_tk', 'EOF_tk', 'DELM_tk', 'EQEQ_tk', 'DTDTEQ_tk', 'NOTEQ_tk' ,
               'BARBAR_tk', 'AMPAMP_tk'}
#                   9           10

token_names = {'Identifier', 'Number', 'Keyword', 'Operator', 'End of file', 'Delimiter',
               'Equality Assessment', 'Coline Equal', 'Not Equal', 'or operator'}

Token = namedtuple('Token', ['tokenID', 'tk_string', 'line_num', 'character_num'])

char_col_map = {'digit': 0, 'letter': 1, ' ': 2, '=': 3, ':': 4, '!': 5, '|': 6, '&': 7}

fsa_table = [[1   ,    2,    0,    3,    5,    7,    9,   11],    # 0
             [1   , 1001, 1001, 1001, 1001, 1001, 1001, 1001],    # 1
             [2   ,    2, 1000, 1000, 1000, 1000, 1000, 1000],    # 2
             [1003, 1003, 1003, 4   , 1003, 1003, 1003, 1003],    # 3
             [1006, 1006, 1006, 1006, 1006, 1006, 1006, 1006],    # 4
             [1003, 1003, 1003,    6, 1003, 1003, 1003, 1003],    # 5
             [1007, 1007, 1007, 1007, 1007, 1007, 1007, 1007],    # 6
             [  -8,   -8,   -8,    8,   -8,   -8,   -8,   -8],    # 7
             [1008, 1008, 1008, 1008, 1008, 1008, 1008, 1008],    # 8
             [  -9,   -9,   -9,   -9,   -9,   -9,   10,   -9],    # 9
             [1009, 1009, 1009, 1009, 1009, 1009, 1009, 1009],    # 10
             [ -10,  -10,  -10,  -10,  -10,  -10,  -10,   12],    # 11
             [1010, 1010, 1010, 1010, 1010, 1010, 1010, 1010]     # 12
             ]


def scan_for_tokens(lines):
    new_token = ''
    current_state = 0
    token_list = []

    for ln in range(len(lines)):
        for cn in range(len(lines[ln])):
            print ('current state: ', current_state)
            current_state = get_new_state(current_state, lines[ln][cn])

            if current_state < 0:
                print('Error number: ' +str(current_state))
                print('Unexpected character on line '+str(ln)+' character '+str(cn))
                exit(1)

            elif current_state > 999:
                print('final_token: ' + new_token + '    code ' + str(current_state))
                token_list.append(new_token)
                new_token = lines[ln][cn]
                current_state = 0
                current_state = get_new_state(current_state, lines[ln][cn])
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

    return 5000


# returns int value at table
def get_new_state(state, character):
    col = char_to_col(character)
    new_state = fsa_table[state][col]
    return new_state

