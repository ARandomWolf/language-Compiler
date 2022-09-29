# python 2.7.5
# Wyatt Wolf
# CS4280

from collections import namedtuple
Token = namedtuple('Token', ['tokenID', 'tk_string', 'line_num', 'character_num'])

# Base token types (keywords and single operators are given unique token names after scanning)
#                  0            1       2        3         4          5            6        7           8
tokenID_map = ['IDENT_tk', 'NUM_tk', 'KW_tk', 'OP_tk', 'EOF_tk', 'DELM_tk', 'EQEQ_tk', 'DTDTEQ_tk', 'NOTEQ_tk',
               'BARBAR_tk', 'AMPAMP_tk']
#                   9           10

keyword_names = {'begin': 'begin_tk', 'end': 'end_tk', 'do': 'do_tk', 'while': 'while_tk', 'whole': 'whole_tk',
                 'label': 'label_tk', 'return': 'return_tk', 'input': 'input_tk', 'output': 'output_tk',
                 'program': 'program_tk', 'warp': 'warp_tk', 'if': 'if_tk', 'then': 'then_tk', 'pick': 'pick_tk',
                 'declare': 'declare_tk', 'assign': 'assign_tk', 'func': 'func_tk'}

# maps characters to their corresponding column
char_col_map = {' ': 2, '=': 3, ':': 4, '!': 5, '|': 6, '&': 7}

# column 8 in state table contains all chars stored here
single_char_tokens_column = ['<', '>', '+', '-', '*', '/', '^', '.', '(', ')', ',', '{', '}', ';', '[', ']']

# all single character reserved tokens
single_char_tokens = {'<': 'LESS_tk', '>': 'GREAT_tk', '+': 'PLUS_tk', '-': 'MINUS_tk',
                      '*': 'MULT_tk', '/': 'DIV_tk', '^': 'CARROT_tk', '.': 'PERIOD_tk', '(': 'LPREN_tk',
                      ')': 'RPREN_tk', ',': 'COMMA_tk', '{': 'LBRACE_tk', '}': 'RBRACE_tk', ';': 'SMICLN_tk',
                      '[': 'LBRACK_tk', ']': 'RBRACK_tk', '=': 'EQUAL_tk', ':': 'COLON_tk'}

# more helpful error messages
error_messages = {-8: '\'=\' expected after ', -9: '\'|\' expected after ',
                  -10: '\'&\' expected after ', -100: 'Unexpected Character: '}

# state table for identifying tokens
#               0    1     2     3     4     5     6      7     8
#              dig lett   ws     =     :     !     |      &   rest
fsa_table = [[   1,    2,    0,    3,    5,    7,    9,   11,   13],  # 0
             [   1, 1001, 1001, 1001, 1001, 1001, 1001, 1001, 1001],  # 1
             [   2,    2, 1000, 1000, 1000, 1000, 1000, 1000, 1000],  # 2
             [1003, 1003, 1003,    4, 1003, 1003, 1003, 1003, 1003],  # 3
             [1006, 1006, 1006, 1006, 1006, 1006, 1006, 1006, 1006],  # 4
             [1003, 1003, 1003,    6, 1003, 1003, 1003, 1003, 1003],  # 5
             [1007, 1007, 1007, 1007, 1007, 1007, 1007, 1007, 1007],  # 6
             [  -8,   -8,   -8,    8,   -8,   -8,   -8,   -8,   -8],  # 7
             [1008, 1008, 1008, 1008, 1008, 1008, 1008, 1008, 1008],  # 8
             [  -9,   -9,   -9,   -9,   -9,   -9,   10,   -9,   -9],  # 9
             [1009, 1009, 1009, 1009, 1009, 1009, 1009, 1009, 1009],  # 10
             [ -10,  -10,  -10,  -10,  -10,  -10,  -10,   12,  -10],  # 11
             [1010, 1010, 1010, 1010, 1010, 1010, 1010, 1010, 1010],  # 12
             [1003, 1003, 1003, 1003, 1003, 1003, 1003, 1003, 1003]   # 13
             ]

