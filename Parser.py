# Python 2.7.5
# Wyatt Wolf


from NodeClass import Node


class Parser:

    def __init__(self, t_list):
        self.token_list = t_list
        self.lookahead = 0
        self.parse_tree = None

    # prints info on token that caused error
    # (actually just token at current look-a-head)
    def print_error(self):
        print('Error on Line: ' + str(self.token_list[self.lookahead - 0].line_num) + ' char: ' +
              str(self.token_list[self.lookahead - 0].character_num))

    # call to parse stored token list
    def parse_token_list(self):
        self.lookahead = 0
        self.parse_tree = None
        self.parse_tree = self.program()

    # wrapper for preorder traversal defined in NodeClass.py
    def print_preorder(self):
        self.parse_tree.preorder(self.parse_tree, 0)

    # wrapper for stack print defined in NodeClass.py
    def printstack(self):
        self.parse_tree.print_stack()

    # standalone semicolon check
    def check_semicolon(self):
        if self.token_list[self.lookahead].tokenID == 'SMICLN_tk':
            self.lookahead += 1
            return
        else:
            print('Error Semicolon expected.')
            print(self.token_list[self.lookahead])
            self.print_error()
            exit(1)

    # *******************************************************************************************
    # Below BNF of language is implemented, where each non-terminal has its own function.
    # Comment before each method specifies the production rule it checks
    # *******************************************************************************************

    # <program> -> <vars> program <block>
    def program(self):
        temp = Node('program')
        # <vars>
        temp.add_child(self.vars())

        # program
        if self.token_list[self.lookahead].tokenID == 'program_tk':
            self.lookahead += 1
            # <block>
            temp.add_child(self.block())
            if self.token_list[self.lookahead].tokenID == 'EOF_tk':
                self.lookahead += 1
                return temp
            else:
                self.print_error()
                print('Token found outside main program block.')
                exit(1)
        else:
            self.print_error()
            print('Invalid declaration statement or missing \'Program\' keyword after variable declaration(s)')
            exit(1)

    # <block> -> begin <vars> <stats> end
    def block(self):
        temp = Node('block')
        if self.token_list[self.lookahead].tokenID == 'begin_tk':  # begin
            self.lookahead += 1
            # <vars>
            temp.add_child(self.vars())
            # <stats>
            temp.add_child(self.stats())
            # end
            if self.token_list[self.lookahead].tokenID == 'end_tk':
                self.lookahead += 1
                return temp
            else:
                self.print_error()
                print('Block statement expected to end with keyword: end')
                exit(1)
        else:
            self.print_error()
            print('Block statement expected to start with keyword: begin')
            exit(1)

    # <vars> -> whole Identifier := Integer ; <vars>
    def vars(self):
        temp = Node('vars')

        # whole
        if self.token_list[self.lookahead].tokenID == 'whole_tk':
            self.lookahead += 1
            # Identifier
            if self.token_list[self.lookahead].tokenID == 'IDENT_tk':
                temp.data.append(self.token_list[self.lookahead])
                self.lookahead += 1
                # :=
                if self.token_list[self.lookahead].tokenID == 'DTDTEQ_tk':
                    self.lookahead += 1
                    # Integer
                    if self.token_list[self.lookahead].tokenID == 'NUM_tk':
                        temp.data.append(self.token_list[self.lookahead])
                        self.lookahead += 1
                        # ;
                        if self.token_list[self.lookahead].tokenID == 'SMICLN_tk':
                            self.lookahead += 1
                            # <vars>
                            temp.add_child(self.vars())
                            return temp
                        else:
                            self.print_error()
                            print('Semicolon expected at end of variable declaration')
                            exit(1)

                    else:
                        self.print_error()
                        print('Number expected after assignment operator in variable declaration statement')
                        exit(1)

                else:
                    self.print_error()
                    print('\':=\' operator expected after variable name in declaration statement')
                    exit(1)

            else:
                self.print_error()
                print('Identifier expected after whole keyword.')
                exit(1)
        else:
            return

    # <expr> -> <N> <expr_prime>
    def expr(self):
        temp = Node('expr')
        temp.add_child(self.n())
        temp.add_child(self.expr_prime())
        return temp

    # <expr_prime>-> -<expr> | EMPTY
    def expr_prime(self):
        temp = Node('expr_prime')
        if self.token_list[self.lookahead].tokenID == 'MINUS_tk':
            temp.data.append(self.token_list[self.lookahead])
            self.lookahead += 1
            temp.add_child(self.expr())
            return temp
        else:  # EMPTY
            return

    #  <n> -> <a><n_prime>
    def n(self):
        temp = Node('n')
        temp.add_child(self.a())
        temp.add_child(self.n_prime())
        return temp

    # <n_prime> -> +<n> | *<n> | EMPTY
    def n_prime(self):
        temp = Node('n_prime')
        if self.token_list[self.lookahead].tokenID == 'PLUS_tk':
            temp.data.append(self.token_list[self.lookahead])

        elif self.token_list[self.lookahead].tokenID == 'MULT_tk':
            temp.data.append(self.token_list[self.lookahead])

        else:
            return

        self.lookahead += 1
        temp.add_child(self.n())
        return temp

    # <a> -> <m><a_prime>
    def a(self):
        temp = Node('a')
        temp.add_child(self.m())
        temp.add_child(self.a_prime())
        return temp

    # <a_prime> -> /<a> | EMPTY
    def a_prime(self):
        temp = Node('a_prime')
        if self.token_list[self.lookahead].tokenID == 'DIV_tk':
            temp.data.append(self.token_list[self.lookahead])
            self.lookahead += 1
            temp.add_child(self.a())
            return temp
        else:  # EMPTY
            return

    # <m> -> :<m> | <r>
    def m(self):
        temp = Node('m')
        if self.token_list[self.lookahead].tokenID == 'COLON_tk':
            temp.data.append(self.token_list[self.lookahead])
            self.lookahead += 1
            temp.add_child(self.m())
            return temp
        else:
            temp.add_child(self.r())
            return temp

    # <r> ->  (<expr>) | IDENT_tk | NUM_tk
    def r(self):
        temp = Node('r_node')
        if self.token_list[self.lookahead].tokenID == 'LPREN_tk':
            self.lookahead += 1
            temp.add_child(self.expr())

            if self.token_list[self.lookahead].tokenID == 'RPREN_tk':
                self.lookahead += 1
                return temp
            else:
                self.print_error()
                print('Missing closing ) in expression')
                exit(1)
        elif self.token_list[self.lookahead].tokenID == 'IDENT_tk':
            temp.data.append(self.token_list[self.lookahead])
            self.lookahead += 1
            return temp
        elif self.token_list[self.lookahead].tokenID == 'NUM_tk':
            temp.data.append(self.token_list[self.lookahead])
            self.lookahead += 1
            return temp
        else:
            self.print_error()
            print('Unexpected or missing token in expression.')
            exit(1)

    # <stats> -> <stat> <mStat>
    def stats(self):
        temp = Node('stats')
        temp.add_child(self.stat())
        temp.add_child(self.mstat())
        return temp

    # <mstat> -> <stat><mstat> | EMPTY
    def mstat(self):
        temp = Node('mstat')
        first_stat = {'input_tk', 'output_tk', 'begin_tk', 'if_tk', 'while_tk',
                      'assign_tk', 'warp_tk', 'label_tk'}
        if first_stat.__contains__(self.token_list[self.lookahead].tokenID):
            temp.add_child(self.stat())
            temp.add_child(self.mstat())
            return temp
        else:  # empty
            return

    # <stat> -> <in_nt>; | <out_nt>; | <block> | <if_nt>; | <warp_nt>; | <assign_nt>; | <loop_nt>; | <label_nt>;
    def stat(self):
        temp = Node('stat')

        ll_id = self.token_list[self.lookahead].tokenID
        if ll_id == 'input_tk':  # <in>
            temp.add_child(self.in_nt())
            self.check_semicolon()
        elif ll_id == 'output_tk':  # <out>
            temp.add_child(self.out_nt())
            self.check_semicolon()
        elif ll_id == 'begin_tk':  # <block>
            temp.add_child(self.block())
        elif ll_id == 'if_tk':  # <if>
            temp.add_child(self.if_nt())
            self.check_semicolon()
        elif ll_id == 'while_tk':  # <loop>
            temp.add_child(self.loop_nt())
            self.check_semicolon()
        elif ll_id == 'assign_tk':  # <assign>
            temp.add_child(self.assign_nt())
            self.check_semicolon()
        elif ll_id == 'warp_tk':  # <goto>
            temp.add_child(self.warp_nt())
            self.check_semicolon()
        elif ll_id == 'label_tk':  # <label>
            temp.add_child(self.label_nt())
            self.check_semicolon()
        else:
            print('Error! Statement expected.')
            print('Possibly missing \'begin\' keyword for start of statement block')
            self.print_error()
            exit(1)

        return temp

    # <in_nt> -> input IDENT_tk
    def in_nt(self):
        temp = Node('in_nt')

        if self.token_list[self.lookahead].tokenID == 'input_tk':
            self.lookahead += 1

            if self.token_list[self.lookahead].tokenID == 'IDENT_tk':
                temp.data.append(self.token_list[self.lookahead])
                self.lookahead += 1
                return temp
            else:
                self.print_error()
                print('Input keyword should be followed by an identifier.')
                exit(1)
        else:
            print('You shouldnt be here! Erron in: input_tk() ')
            exit(1)

    # <out_nt> -> output <expr>
    def out_nt(self):
        temp = Node('out_nt')

        if self.token_list[self.lookahead].tokenID == 'output_tk':
            self.lookahead += 1
            temp.add_child(self.expr())
            return temp
        else:
            self.print_error()
            exit(1)

    # <if_nt> -> if [ <expr> <RO> <expr> ] then <stat> <if_nt_prime>
    def if_nt(self):
        temp = Node('if_nt')

        if self.token_list[self.lookahead].tokenID == 'if_tk':
            self.lookahead += 1
            if self.token_list[self.lookahead].tokenID == 'LBRACK_tk':
                self.lookahead += 1
                temp.add_child(self.expr())
                temp.add_child(self.ro())
                temp.add_child(self.expr())

                if self.token_list[self.lookahead].tokenID == 'RBRACK_tk':
                    self.lookahead += 1
                    if self.token_list[self.lookahead].tokenID == 'then_tk':
                        self.lookahead += 1
                        temp.add_child(self.stat())
                        temp.add_child(self.if_nt_prime())
                        return temp
                    else:
                        self.print_error()
                        print(' Missing \'then\' keyword in \'if\' statement')
                        exit(1)
                else:
                    self.print_error()
                    print('Missing ] in \'if\' statement')
                    exit(1)
            else:
                self.print_error()
                print('Missing [ in \'if\' statement')
                exit(1)
        else:
            exit(1)

    # <if_nt_prime> -> pick <stat> | EMPTY
    def if_nt_prime(self):
        if self.token_list[self.lookahead].tokenID == 'pick_tk':
            temp = Node('if_nt_prime')
            self.lookahead += 1
            temp.add_child(self.stat())
            return temp
        else:
            return

    # <loop_nt> -> while [<expr><RO><expr>] <stat>
    def loop_nt(self):
        temp = Node('loop_nt')

        if self.token_list[self.lookahead].tokenID == 'while_tk':
            self.lookahead += 1  # while
            if self.token_list[self.lookahead].tokenID == 'LBRACK_tk':
                self.lookahead += 1  # [
                temp.add_child(self.expr())  # <expr>
                temp.add_child(self.ro())  # <RO>
                temp.add_child(self.expr())  # <expr>

                if self.token_list[self.lookahead].tokenID == 'RBRACK_tk':
                    self.lookahead += 1  # ]
                    temp.add_child(self.stat())  # <stat>
                    return temp

                else:
                    self.print_error()
                    print('Missing ] in \'while\' statement.')
                    exit(1)
            else:
                self.print_error()
                print('Missing [ in \'while\' statement.')
                exit(1)
        else:
            exit(1)

    # <assign_nt> -> assign IDENT_tk EQUAL_tk <expr>
    def assign_nt(self):
        temp = Node('assign_nt')
        if self.token_list[self.lookahead].tokenID == 'assign_tk':
            self.lookahead += 1
            if self.token_list[self.lookahead].tokenID == 'IDENT_tk':
                temp.data.append(self.token_list[self.lookahead])
                self.lookahead += 1
                if self.token_list[self.lookahead].tokenID == 'EQUAL_tk':
                    self.lookahead += 1
                    temp.add_child(self.expr())
                    return temp

                else:
                    print('Error! \'=\' token expected after identifier in statement starting with \'assign\' keyword.')
                    self.print_error()
                    exit(1)
            else:
                print('Error! Identifier expected.')
                self.print_error()
                exit(1)
        else:
            exit(1)

    # <ro> -> > | < | == | [=] | !=
    def ro(self):
        temp = Node('ro')
        valid = {'GREAT_tk', 'LESS_tk', 'EQEQ_tk', 'NOTEQ_tk'}

        if valid.__contains__(self.token_list[self.lookahead].tokenID):
            temp.data.append(self.token_list[self.lookahead])
            self.lookahead += 1
            return temp

        elif self.token_list[self.lookahead].tokenID == 'LBRACK_tk':
            temp.data.append(self.token_list[self.lookahead])
            self.lookahead += 1

            if self.token_list[self.lookahead].tokenID == 'EQUAL_tk':
                temp.data.append(self.token_list[self.lookahead])
                self.lookahead += 1

                if self.token_list[self.lookahead].tokenID == 'RBRACK_tk':
                    temp.data.append(self.token_list[self.lookahead])
                    self.lookahead += 1
                    return temp
                else:
                    self.print_error()
                    print('Did you mean \'[=]\' ? ')
                    exit(1)
            else:
                self.print_error()
                print('Did you mean \'[=]\' ? ')
                exit(1)
        else:
            self.print_error()
            print('Equality operator expected.')
            exit(1)

    # <label_nt> -> label IDENT_tk
    def label_nt(self):
        temp = Node('label_nt')
        if self.token_list[self.lookahead].tokenID == 'label_tk':
            self.lookahead += 1

            if self.token_list[self.lookahead].tokenID == 'IDENT_tk':
                temp.data.append(self.token_list[self.lookahead])
                self.lookahead += 1
                return temp

            else:
                print('Identifier expected after \'label\' token')
                self.print_error()
                exit(1)
        else:
            exit(1)

    # <warp_nt> -> warp IDENT_tk
    def warp_nt(self):
        temp = Node('warp_nt')

        if self.token_list[self.lookahead].tokenID == 'warp_tk':
            self.lookahead += 1
            if self.token_list[self.lookahead].tokenID == 'IDENT_tk':
                temp.data.append(self.token_list[self.lookahead])
                self.lookahead += 1
                return temp
            else:
                print('Error! Identifier expected')
                self.print_error()
                exit(1)
        else:
            exit(1)
