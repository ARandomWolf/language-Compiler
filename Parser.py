# Python 2.7.5
# Wyatt Wolf


class Parser:

    def __init__(self, t_list):
        self.token_list = t_list
        self.lookahead = 0

    def print_error(self, lahead):
        print('\nError! Line: ' + str(self.token_list[lahead].line_num) + ' char: ' +
              str(self.token_list[lahead].character_num))

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
                # valid syntax
                return
            else:
                self.print_error(self.lookahead)
                print('Block statement expected to end with keyword: end')
                exit(1)
        else:
            self.print_error(self.lookahead)
            print('Block statement expected to start with keyword: begin')
            exit(1)

    # <stat> <mStat>
    def stats(self):
        self.stat()
        self.mstat()

    def stat(self):
        return

    def mstat(self):
        return

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

