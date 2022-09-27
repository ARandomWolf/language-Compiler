# python 2.7.5
# Wyatt Wolf

import re
from collections import namedtuple

#                  0            1       2        3         4          5            6        7
tokenID_map = {'IDENT_tk', 'NUM_tk', 'KW_tk', 'OP_tk', 'EOF_tk', 'DELM_tk', 'EQEQ_tk', 'DTDTEQ_tk'}
token_names = {'Identifier', 'Number', 'Keyword', 'Operator', 'End of file', 'Delimiter', 'Equality Assessment', 'Coline Equal'}

Token = namedtuple('Token', ['tokenID', 'tk_string', 'line_num', 'character_num'])

char_col_map = {'digit': 0, 'letter': 1, ' ': 2, '=': 3, ':': 4}

fsa_table = [[1, 2, 0, 3],  # 0
             [1, 1001, 1001, 1001],  # 1
             [2, 2, 1000, 1000],  # 2
             [1003, 1003, 1003, 4],
             [1006, 1006, 1006, -1]
             ]


def scan_array(lines):
    new_token = ''
    current_state = 0
    token_list = []

    for ln in range(len(lines)):
        for cn in range(len(lines[ln])):
            print ('current state: ', current_state)
            current_state = get_new_state(current_state, lines[ln][cn])

            if current_state < 0:
                print('error unexpected character on line '+str(ln)+' character '+str(cn))
            elif current_state == 0:
                continue
            elif current_state > 999:
                print('final token ' + new_token + ' code ' + str(current_state))
                token_list.append(new_token)
                new_token = ''
                current_state = 0
            else:
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
