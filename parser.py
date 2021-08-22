import sys
from lexer import *
from astnodes import *

class Parser: 
    def __init__(self, lexer):
        self.lexer = lexer
        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()

    #Retorna true se o token **atual** casa com kind
    def checkToken(self, kind):
        return kind == self.curToken.kind

    #Retorna true se o próximo token **(peek)** casa com kind
    def checkPeek(self, kind):
        return kind == self.peekToken.kind

    def match(self, kind):
        if not self.checkToken(kind):
            self.abort("Esperava por " + kind.name + ", apareceu " + self.curToken.kind.name)
        self.nextToken()

    # Avançando com os ponteiros dos tokens (atual e peek)
    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()

    def abort(self, msg):
        sys.exit("Erro sintático: "+msg)

    #program ::== {statement}
    def program(self):
        # print("PROGRAM")
        stmts = []
        self.match(TokenType.PROGRAM)
        programName = self.curToken.text
        self.match(TokenType.IDENT)
        self.nl()
        #{statement} -- 0 ou mais statements
        while not self.checkToken(TokenType.ENDPROGRAM):
            stmts.append(self.statement())
        self.match(TokenType.ENDPROGRAM)
        self.nl()
        self.match(TokenType.EOF)
        return Program(programName, stmts)

    #statement ::== "PRINT" (expression | string) nl
    def statement(self):
        stm = None
        #"PRINT" (expression | string) nl
        if self.checkToken(TokenType.PRINT):
            # print("STM-PRINT")
            self.match(TokenType.PRINT)
            # e = None
            # if self.checkToken(TokenType.STRING_LITERAL):
            #     e = StringExpr(self.curToken.text)
            #     self.match(TokenType.STRING_LITERAL)
            # else:
            #     e = self.expression()
            e = self.expression()
            stm = PrintStm(e)
        #"IF" expression "THEN" nl {statement} "ENDIF" nl
        elif self.checkToken(TokenType.IF):
            # print("STM-IF")
            self.nextToken()
            cond = self.expression()
            self.match(TokenType.THEN)
            self.nl()
            ls = []
            while not self.checkToken(TokenType.ENDIF):
                ls.append(self.statement())
            self.match(TokenType.ENDIF)
            stm = IfStm(cond, ls)
        #"WHILE" expression "REPEAT" nl {statement} "ENDWHILE" nl
        elif self.checkToken(TokenType.WHILE):
            # print("STM-WHILE")
            self.nextToken()
            cond = self.expression()
            self.match(TokenType.REPEAT)
            self.nl()
            ls = []
            while not self.checkToken(TokenType.ENDWHILE):
                ls.append(self.statement())
            self.match(TokenType.ENDWHILE)
            stm = WhileStm(cond, ls)
        #"BEGINBLOCK" ID nl {statement} "ENDBLOCK" nl
        elif self.checkToken(TokenType.BLOCK):
            # print("STM-BLOCK")
            self.match(TokenType.BLOCK)
            blockName = self.curToken.text
            self.match(TokenType.IDENT)
            self.match(TokenType.BEGIN)
            self.nl()
            ls = []
            while not self.checkToken(TokenType.ENDBLOCK):
                ls.append(self.statement())
            self.match(TokenType.ENDBLOCK)
            stm = BlockStm(blockName,ls)
        #"PROCEDURE" ID "("{formal_parameter_list}")" "BEGIN" nl {statement} "ENDPROCEDURE" nl
        elif self.checkToken(TokenType.PROCEDURE):
            # print("STM-PROCEDURE")
            self.match(TokenType.PROCEDURE)
            procName = self.curToken.text
            self.match(TokenType.IDENT)
            self.match(TokenType.L_PAREN)
            params = self.formal_parameter_list()
            self.match(TokenType.R_PAREN)
            self.match(TokenType.BEGIN)
            self.nl()
            ls = []
            while not self.checkToken(TokenType.ENDPROCEDURE):
                ls.append(self.statement())
            self.match(TokenType.ENDPROCEDURE)
            stm = ProcedureDeclStm(procName, params, ls)
        #"CALL" ID "("{actual_parameter_list}")" nl
        elif self.checkToken(TokenType.CALL):
            # print("STM-CALL")
            self.match(TokenType.CALL)
            procName = self.curToken.text
            self.match(TokenType.IDENT)
            self.match(TokenType.L_PAREN)
            params = self.actual_parameter_list()
            self.match(TokenType.R_PAREN)
            stm = ProcedureCallStm(procName, params)
        #"DECL" ID ":" ("BOOLEAN" | "INT" | "STRING") nl 
        elif self.checkToken(TokenType.DECL):
            # print("STM-DECL")
            self.match(TokenType.DECL)
            nome = self.curToken.text
            self.match(TokenType.IDENT)
            self.match(TokenType.COLON)
            if self.checkToken(TokenType.INT) or self.checkToken(TokenType.BOOLEAN) or self.checkToken(TokenType.STRING):
                tipo = self.curToken.text
                self.nextToken()
            else:
                self.abort('Esperava um tipo válido (INT, BOOLEAN, ou STRING), recebeu ' + self.curToken.text + " ("+self.curToken.kind.name+")")
            stm = VarDeclStm(nome, tipo)
        #"LET" ID "=" expression nl 
        elif self.checkToken(TokenType.LET):
            # print("STM-LET")
            self.nextToken()
            nome = self.curToken.text
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            e = self.expression()
            stm = AssignStm(nome, e)
        #"INPUT" ID nl
        elif self.checkToken(TokenType.INPUT):
            # print("STM-INPUT")
            self.match(TokenType.INPUT)
            nome = self.curToken.text
            self.match(TokenType.IDENT)
            stm = InputStm(nome)
        else: 
            self.abort("Erro, problema com " + self.curToken.text + " ("+self.curToken.kind.name+")")
        
        self.nl()
        
        return stm

    def formal_parameter_list(self):
        """ formal_parameter_list : (formal_parameters)? (SEMICOLON formal_parameters)* """
        if not self.checkToken(TokenType.IDENT):
            return []

        params = []
        params.append(self.formal_parameters())

        while self.checkToken(TokenType.SEMICOLON):
            self.match(TokenType.SEMICOLON)
            params.append(self.formal_parameters())

        return params

    def formal_parameters(self):
        """ formal_parameters : ID COLON type_spec """
        param = []

        nome = self.curToken.text
        self.match(TokenType.IDENT)
        self.match(TokenType.COLON)
        if self.checkToken(TokenType.INT) or self.checkToken(TokenType.BOOLEAN) or self.checkToken(TokenType.STRING):
            tipo = self.curToken.text
            self.nextToken()
        else:
            self.abort('Esperava um tipo válido (INT, BOOLEAN, ou STRING), recebeu ' + self.curToken.text + " ("+self.curToken.kind.name+")")
        return Param(nome, tipo)

    def actual_parameter_list(self):
        params = []

        if self.checkToken(TokenType.R_PAREN):
            return params

        params.append(self.expression())

        while self.checkToken(TokenType.COMMA):
            self.match(TokenType.COMMA)
            params.append(self.expression())

        return params

    # expression ::== equality
    def expression(self): 
        return self.equality()
    
    # equality ::== comparison ( ("==" | "!=" ) comparison)*
    def equality(self):
        e = self.comparison()
        while self.checkToken(TokenType.NOTEQ) or self.checkToken(TokenType.EQEQ):
            if self.checkToken(TokenType.NOTEQ):
                self.match(TokenType.NOTEQ)
                t = self.comparison()
                e = NotEqualsExpr(e, t)
            elif self.checkToken(TokenType.EQEQ):
                self.match(TokenType.EQEQ)
                t = self.comparison()
                e = EqualsExpr(e, t)
        return e

    
    #comparison ::== term ( ("<" | "<=" | ">" | ">=" ) term)*
    def comparison(self): 
        # print("COMPARISON")
        e = self.term()
        while self.checkToken(TokenType.GT) or self.checkToken(TokenType.GTEQ) or self.checkToken(TokenType.LT) or self.checkToken(TokenType.LTEQ):
            if self.checkToken(TokenType.GTEQ):
                self.match(TokenType.GTEQ)
                e_r = self.term()
                e = GreaterThanEqualsExpr(e,e_r)
            elif self.checkToken(TokenType.GT):
                self.match(TokenType.GT)
                e_r = self.term()
                e = GreaterThanExpr(e,e_r)
            elif self.checkToken(TokenType.LTEQ):
                self.match(TokenType.LTEQ)
                e_r = self.term()
                e = LessThanEqualsExpr(e,e_r)
            elif self.checkToken(TokenType.LT):
                self.match(TokenType.LT)
                e_r = self.term()
                e = LessThanExpr(e,e_r)
        return e

    #term ::== factor {("-" | "+") factor}
    def term(self):
        # print("EXPRESSION")
        e = self.factor()
        while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            if self.checkToken(TokenType.PLUS):
                self.match(TokenType.PLUS)
                t = self.factor()
                e = SumExpr(e, t)
            elif self.checkToken(TokenType.MINUS):
                self.match(TokenType.MINUS)
                t = self.factor()
                e = SubExpr(e, t)
        return e

    #factor ::== unary {("*" | "/") unary}
    # 2 * 3 * 4 * 5
    def factor(self):
        e = self.unary()
        while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH):
            if self.checkToken(TokenType.ASTERISK):
                self.match(TokenType.ASTERISK)
                u = self.unary()
                e = MulExpr(e, u)
            elif self.checkToken(TokenType.SLASH):
                self.match(TokenType.SLASH)
                u = self.unary()
                e = DivExpr(e, u)
        return e 

    #unary ::== ["-" | "+" | "!"] unary | primary
    def unary(self):
        # print("UNARY")
        e = None
        if self.checkToken(TokenType.PLUS):
            self.match(TokenType.PLUS)
            e = UnaryPlusExpr(self.unary())
        elif self.checkToken(TokenType.MINUS):
            self.match(TokenType.MINUS)
            e = UnaryMinusExpr(self.unary())
        elif self.checkToken(TokenType.BANG):
            self.match(TokenType.BANG)
            e = NotExpr(self.unary())
        else:
            e = self.primary()
        return e

    #primary ::== NUM | ID | STRING | "TRUE" | "FALSE" | "(" expression ")"
    def primary(self):
        e = None
        # print("PRIMARY (" + self.curToken.text + ")")
        if self.checkToken(TokenType.NUMBER):
            e = NumExpr(int(self.curToken.text))
            self.match(TokenType.NUMBER)
        elif self.checkToken(TokenType.IDENT):
            e = IdExpr(self.curToken.text)
            self.match(TokenType.IDENT)
        elif self.checkToken(TokenType.STRING_LITERAL):
            e = StringExpr(self.curToken.text)
            self.match(TokenType.STRING_LITERAL)
        elif self.checkToken(TokenType.TRUE):
            e = TrueExpr()
            self.match(TokenType.TRUE)
        elif self.checkToken(TokenType.FALSE):
            e = FalseExpr()
            self.match(TokenType.FALSE)
        elif self.checkToken(TokenType.L_PAREN):
            self.match(TokenType.L_PAREN)
            e = self.expression()
            self.match(TokenType.R_PAREN)
        else: 
            self.abort("Token inesperado, esperava um número ou identificador, recebeu: " + self.curToken.text)
        return e

    def nl(self):
        # print("")
        self.match(TokenType.NEWLINE)
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()
