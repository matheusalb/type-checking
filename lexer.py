import enum
import sys

class Lexer:
    def __init__(self, input):
        self.source = input + '\n' #código-fonte (entrada)
        self.curChar = '' #caractere atual dentro do código-fonte
        self.curPos = -1
        self.nextChar()
        pass

    # Processa o proximo caractere
    def nextChar(self):
        self.curPos = self.curPos + 1
        if self.curPos >= len(self.source):
            self.curChar = '\0' #EOF
        else:
            self.curChar = self.source[self.curPos]

    # Retorna o caractere seguinte (ainda não lido).
    def peek(self):
        if self.curPos+1 >= len(self.source):
            return '\0'
        else: 
            return self.source[self.curPos+1]

    # Token inválido encontrado, método usado para imprimir mensagem de erro e encerrar.
    def abort(self, message):
        sys.exit("Erro léxico! " + message)
		
    # Pular espaço em branco, exceto novas linhas, que são usadas como separadores.
    def skipWhitespace(self):
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            self.nextChar()
		
    # Pular comentários.
    def skipComment(self):
        if self.curChar=='#':
            while self.curChar != '\n':
                self.nextChar()

    # Return o próximo token.
    def getToken(self):
        self.skipWhitespace()
        self.skipComment()
        token = None
        if self.curChar == '+':
            token = Token(self.curChar, TokenType.PLUS)
        elif self.curChar == '-':
            token = Token(self.curChar, TokenType.MINUS)
        elif self.curChar == '*':
            token = Token(self.curChar, TokenType.ASTERISK)
        elif self.curChar == '/':
            token = Token(self.curChar, TokenType.SLASH)
        elif self.curChar == ':':
            token = Token(self.curChar, TokenType.COLON)
        elif self.curChar == ';':
            token = Token(self.curChar, TokenType.SEMICOLON)
        elif self.curChar == '(':
            token = Token(self.curChar, TokenType.L_PAREN)
        elif self.curChar == ')':
            token = Token(self.curChar, TokenType.R_PAREN)
        elif self.curChar == ',':
            token = Token(self.curChar, TokenType.COMMA)
        elif self.curChar == '\n':
            token = Token(self.curChar, TokenType.NEWLINE)
        elif self.curChar == '\0':
            token = Token(self.curChar, TokenType.EOF)
        #se for = EQ, se for == EQEQ
        elif self.curChar == '=':
            if self.peek() == '=':
                c = self.curChar
                self.nextChar()
                token = Token(c + self.curChar, TokenType.EQEQ)
            else: 
                token = Token(self.curChar, TokenType.EQ)
        elif self.curChar == '!':
            if self.peek() == '=':
                c = self.curChar
                self.nextChar()
                token = Token(c + self.curChar, TokenType.NOTEQ)
            else: 
                token = Token(self.curChar, TokenType.BANG)
        elif self.curChar == '>':
            if self.peek() == '=':
                c = self.curChar
                self.nextChar()
                token = Token(c + self.curChar, TokenType.GTEQ)
            else: 
                token = Token(self.curChar, TokenType.GT)
        elif self.curChar == '<':
            if self.peek() == '=':
                c = self.curChar
                self.nextChar()
                token = Token(c + self.curChar, TokenType.LTEQ)
            else: 
                token = Token(self.curChar, TokenType.LT)
        elif self.curChar == '\"':
            self.nextChar()
            startPos = self.curPos
            while self.curChar != '\"':
                if self.curChar == '\\' or self.curChar == '\t' or self.curChar == '\r'  or self.curChar == '%':
                    self.abort("Caractere ilegal dentro de uma string")
                self.nextChar()
            stringText = self.source[startPos : self.curPos]
            token = Token(stringText, TokenType.STRING_LITERAL)
        elif self.curChar.isdigit():
            startPos = self.curPos
            while self.peek().isdigit():
                self.nextChar()
            if self.peek() == '.': #decimais
                self.nextChar()
                if not self.peek().isdigit():
                    self.abort("Caractere ilegal dentro de um número: "+ self.peek())
                while self.peek().isdigit():
                    self.nextChar()
            number = self.source[startPos : self.curPos + 1]
            token = Token(number, TokenType.NUMBER)
        elif self.curChar.isalpha():
            startPos = self.curPos
            while self.peek().isalnum():
                self.nextChar()
            word = self.source[startPos : self.curPos + 1]
            keyword = Token.checkIfKeyword(word)
            if keyword == None:
                token = Token(word, TokenType.IDENT)
            else: 
                token = Token(word, keyword)
        else: 
            #Token desconhecido
            self.abort("Token desconhecido: "+self.curChar)
        
        self.nextChar()
        return token

class Token:
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText #lexema, a instância específica encontrada
        self.kind = tokenKind # o tipo de token (TokenType) classificado
    
    @staticmethod
    def checkIfKeyword(word):
        for kind in TokenType:
            if kind.name == word.upper() and kind.value > 100 and kind.value < 200:
                return kind
        return None

class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING_LITERAL = 3
    COLON = 4
    L_PAREN = 5
    R_PAREN = 6
    SEMICOLON = 7
    COMMA = 8
    #PALAVRAS RESERVADAS
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
    DECL = 112
    INT = 113
    BOOLEAN = 114
    TRUE = 115
    FALSE = 116
    STRING = 117
    PROGRAM = 118
    ENDPROGRAM = 119
    BLOCK = 120
    BEGIN = 121
    ENDBLOCK = 122
    PROCEDURE = 123
    ENDPROCEDURE = 124
    CALL = 125
    #OPERADORES
    EQ = 201  
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211
    BANG = 212