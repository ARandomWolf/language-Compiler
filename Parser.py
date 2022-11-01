
# Python 2.7.5
# Wyatt Wolf


class Parser:

    def __init__(self, t_list):
        self.token_list = t_list
        self.lookahead = 0

    def print_error(self):
        print('Error on Line: ' + str(self.token_list[self.lookahead - 0].line_num) + ' char: ' +
              str(self.token_list[self.lookahead - 0].character_num))

    def parse_token_list(self):
        self.program()

    # <vars> program <block>
    def program(self):
        # <vars>
        self.vars()

        # program
        if self.token_list[self.lookahead].tokenID == 'program_tk':
            self.lookahead += 1
            # <block>
            self.block()
            if self.token_list[self.lookahead].tokenID == 'EOF_tk':
                self.lookahead += 1
                return
            else:
                self.print_error()
                print('Token found outside main program block.')
                exit(1)
        else:
            self.print_error(self.lookahead)
            print('Invalid declaration statement or missing \'Program\' keyword after variable declaration(s)')
            exit(1)

    # begin <vars> <stats> end
    def block(self):
        # begin
        if self.token_list[self.lookahead].tokenID == 'begin_tk':
            self.lookahead += 1
            # <vars>
            self.vars()
            # <stats>
            self.stats()
            # end
            if self.token_list[self.lookahead].tokenID == 'end_tk':
                self.lookahead += 1
                return
            else:
                self.print_error()
                print('Block statement expected to end with keyword: end')
                exit(1)
        else:
            self.print_error()
            print('Block statement expected to start with keyword: begin')
            exit(1)

    # <expr> -> <N> <expr_prime>
    def expr(self):
        self.n()
        self.expr_prime()
        return

    # <expr_prime>-> -<expr> | EMPTY
    def expr_prime(self):
        if self.token_list[self.lookahead].tokenID == 'MINUS_tk':
            self.lookahead += 1
            self.expr()
            return
        else:  # EMPTY
            return

    def n(self):
        self.a()
        self.n_prime()
        return

    def n_prime(self):
        if self.token_list[self.lookahead].tokenID == 'PLUS_tk':
            self.lookahead += 1
            self.n()
            return
        elif self.token_list[self.lookahead].tokenID == 'MULT_tk':
            self.lookahead += 1
            self.n()
            return
        else:
            return

    def a(self):
        self.m()
        self.a_prime()
        return

    # <A'>-> /<A> | EMPTY
    def a_prime(self):
        if self.token_list[self.lookahead].tokenID == 'DIV_tk':
            self.lookahead += 1
            self.a()
            return
        else:  # EMPTY
            return

    def m(self):
        if self.token_list[self.lookahead].tokenID == 'COLON_tk':
            self.lookahead += 1
            self.m()
            return
        else:
            self.r()
            return

    def r(self):
        if self.token_list[self.lookahead].tokenID == 'LPREN_tk':
            self.lookahead += 1
            self.expr()
            if self.token_list[self.lookahead].tokenID == 'RPREN_tk':
                self.lookahead += 1
                return
            else:
                self.print_error()
                print('Missing closing ) in expression')
                exit(1)
        elif self.token_list[self.lookahead].tokenID == 'IDENT_tk':
            self.lookahead += 1
            return
        elif self.token_list[self.lookahead].tokenID == 'NUM_tk':
            self.lookahead += 1
            return
        else:
            self.print_error()
            print('Unexpected or missing token in expression.')
            exit(1)

    def check_semicolin(self):
        if self.token_list[self.lookahead].tokenID == 'SMICLN_tk':
            self.lookahead += 1
            return
        else:
            print('Error Semicolon expected.')
            print(self.token_list[self.lookahead])
            self.print_error()
            exit(1)

    # <stat> <mStat>
    def stats(self):
        self.stat()
        self.mstat()
        return

    def stat(self):
        ll_id = self.token_list[self.lookahead].tokenID
        if ll_id == 'input_tk':  # <in>
            self.input_tk()
            self.check_semicolin()
        elif ll_id == 'output_tk':  # <out>
            self.output_tk()
            self.check_semicolin()
        elif ll_id == 'begin_tk':  # <block>
            self.block()
        elif ll_id == 'if_tk':  # <if>
            self.if_nt()
            self.check_semicolin()
        elif ll_id == 'while_tk':  # <loop>
            self.loop_nt()
            self.check_semicolin()
        elif ll_id == 'assign_tk':  # <assign>
            self.assign_tk()
            self.check_semicolin()
        elif ll_id == 'warp_tk':  # <goto>
            self.warp_nt()
            self.check_semicolin()
        elif ll_id == 'label_tk':  # <label>
            self.label_tk()
            self.check_semicolin()
        else:
            print('Error! Statement expected.')
            print('Possibly missing \'begin\' keyword for start of statement block')
            self.print_error()
            exit(1)
        return

    def mstat(self):
        first_stat = {'input_tk', 'output_tk', 'begin_tk', 'if_tk', 'while_tk',
                      'assign_tk', 'warp_tk', 'label_tk'}
        if first_stat.__contains__(self.token_list[self.lookahead].tokenID):
            self.stat()
            self.mstat()
            return
        else:  # empty
            return

    # <label>
    def label_tk(self):
        if self.token_list[self.lookahead].tokenID == 'label_tk':
            self.lookahead += 1
            if self.token_list[self.lookahead].tokenID == 'IDENT_tk':
                self.lookahead += 1
                return
            else:
                print('Identifier expected after \'label\' token')
                self.print_error()
                exit(1)
        else:
            exit(1)

    # <goto>
    def warp_nt(self):
        if self.token_list[self.lookahead].tokenID == 'warp_tk':
            self.lookahead += 1
            if self.token_list[self.lookahead].tokenID == 'IDENT_tk':
                self.lookahead += 1
                return
            else:
                print('Error! Identifier expected')
                self.print_error()
                exit(1)
        else:
            exit(1)

    def ro(self):
        valid = {'GREAT_tk', 'LESS_tk', 'EQEQ_tk', 'NOTEQ_tk'}

        if valid.__contains__(self.token_list[self.lookahead].tokenID):
            self.lookahead += 1
            return
        elif self.token_list[self.lookahead].tokenID == 'LBRACK_tk':
            self.lookahead += 1
            if self.token_list[self.lookahead].tokenID == 'EQUAL_tk':
                self.lookahead += 1
                if self.token_list[self.lookahead].tokenID == 'RBRACK_tk':
                    self.lookahead += 1
                    return
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

    def assign_tk(self):
        if self.token_list[self.lookahead].tokenID == 'assign_tk':
            self.lookahead += 1
            if self.token_list[self.lookahead].tokenID == 'IDENT_tk':
                self.lookahead += 1
                if self.token_list[self.lookahead].tokenID == 'EQUAL_tk':
                    self.lookahead += 1
                    self.expr()
                    return
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

    def loop_nt(self): # while [<expr><RO><expr>] <stat>
        if self.token_list[self.lookahead].tokenID == 'while_tk':
            self.lookahead += 1  # while
            if self.token_list[self.lookahead].tokenID == 'LBRACK_tk':
                self.lookahead += 1  # [
                self.expr()     # <expr>
                self.ro()       # <RO>
                self.expr()     # <expr>
                if self.token_list[self.lookahead].tokenID == 'RBRACK_tk':
                    self.lookahead += 1  # ]
                    self.stat()  # <stat>
                    return
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

    # <if_nt_prime> -> pick <stat> | EMPTY
    def if_nt_prime(self):
        if self.token_list[self.lookahead].tokenID == 'pick_tk':
            self.lookahead += 1
            self.stat()
            return
        else:
            return

    # if [ <expr> <RO> <expr> ] then <stat> <if_nt_prime>
    def if_nt(self):
        if self.token_list[self.lookahead].tokenID == 'if_tk':
            self.lookahead += 1
            if self.token_list[self.lookahead].tokenID == 'LBRACK_tk':
                self.lookahead += 1
                self.expr()
                self.ro()
                self.expr()
                if self.token_list[self.lookahead].tokenID == 'RBRACK_tk':
                    self.lookahead += 1
                    if self.token_list[self.lookahead].tokenID == 'then_tk':
                        self.lookahead += 1
                        self.stat()
                        self.if_nt_prime()
                        return
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




    # <out>
    def output_tk(self):
        if self.token_list[self.lookahead].tokenID == 'output_tk':
            self.lookahead += 1
            self.expr()
            return
        else:
            exit(1)

    # <in>
    def input_tk(self):
        if self.token_list[self.lookahead].tokenID == 'input_tk':
            self.lookahead += 1
            if self.token_list[self.lookahead].tokenID == 'IDENT_tk':
                self.lookahead += 1
                return
            else:
                print('Input keyword should be followed by an identifier.')
        else:
            print('You shouldnt be here! Erron in: input_tk() ')
            exit(1)

    # whole Identifier := Integer ; <vars>
    def vars(self):
        # whole
        if self.token_list[self.lookahead].tokenID == 'whole_tk':
            self.lookahead += 1
            # Identifier
            if self.token_list[self.lookahead].tokenID == 'IDENT_tk':
                self.lookahead += 1
                # :=
                if self.token_list[self.lookahead].tokenID == 'DTDTEQ_tk':
                    self.lookahead += 1
                    # Integer
                    if self.token_list[self.lookahead].tokenID == 'NUM_tk':
                        self.lookahead += 1
                        # ;
                        if self.token_list[self.lookahead].tokenID == 'SMICLN_tk':
                            self.lookahead += 1
                            # <vars>
                            self.vars()

                        else:
                            self.print_error(self.lookahead)
                            print('Semicolon expected at end of variable declaration')
                            exit(1)

                    else:
                        self.print_error(self.lookahead)
                        print('Number expected after assignment operator in variable declaration statement')
                        exit(1)

                else:
                    self.print_error(self.lookahead)
                    print('\':=\' operator expected after variable name in declaration statement')
                    exit(1)

            else:
                self.print_error(self.lookahead)
                print('Identifier expected after whole keyword.')
                exit(1)