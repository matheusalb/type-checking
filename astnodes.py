class Stmt(object):
    pass

class Expr(object):
    pass

class BooleanExpr(object):
    pass

class Program(object):
    def __init__(self, programName, ls):
        self.name = programName
        self.stmts = ls

class InputStm(Stmt):
    def __init__(self, nome):
        self.id = nome        

class PrintStm(Stmt):
    def __init__(self, e):
        self.exp = e

class VarDeclStm(Stmt):
    def __init__(self, nome, tipo):
        self.id = nome
        self.type = tipo

class Param(object):
    def __init__(self, nome, tipo):
        self.id = nome
        self.type = tipo

class ProcedureDeclStm(Stmt):
    def __init__(self, procName, params, ls):
        self.name = procName
        self.params = params
        self.stmts = ls

class ProcedureCallStm(Stmt):
    def __init__(self, procName, params):
        self.name = procName
        self.params = params

class AssignStm(Stmt):
    def __init__(self, nome, e):
        self.id = nome
        self.exp = e

class IfStm(Stmt):
    def __init__(self, c, ls):
        self.cond = c
        self.stmts = ls

class WhileStm(Stmt):
    def __init__(self, c, ls):
        self.cond = c
        self.stmts = ls

class BlockStm(Stmt):
    def __init__(self, blockName, ls):
        self.name = blockName
        self.stmts = ls

class SumExpr(Expr):
    def __init__(self, ladoEsquerdo, ladoDireito):
        self.left = ladoEsquerdo
        self.right = ladoDireito

class SubExpr(Expr):
    def __init__(self, ladoEsquerdo, ladoDireito):
        self.left = ladoEsquerdo
        self.right = ladoDireito

class MulExpr(Expr):
    def __init__(self, ladoEsquerdo, ladoDireito):
        self.left = ladoEsquerdo
        self.right = ladoDireito

class DivExpr(Expr):
    def __init__(self, ladoEsquerdo, ladoDireito):
        self.left = ladoEsquerdo
        self.right = ladoDireito

class UnaryPlusExpr(Expr):
    def __init__(self, e):
        self.exp = e

class UnaryMinusExpr(Expr):
    def __init__(self, e):
        self.exp = e

class TrueExpr(BooleanExpr):
    def __init__(self):
        self.v = True

class FalseExpr(BooleanExpr):
    def __init__(self):
        self.v = False

class NumExpr(Expr):
    def __init__(self, v):
        self.valor = v

class IdExpr(Expr):
    def __init__(self, nome):
        self.id = nome

class StringExpr(Expr):
    def __init__(self, s):
        self.str = s

class NotExpr(BooleanExpr):# !e
    def __init__(self, e):
        self.exp = e

class EqualsExpr(BooleanExpr):# left == right
    def __init__(self, ladoEsquerdo, ladoDireito):
        self.left = ladoEsquerdo
        self.right = ladoDireito

class NotEqualsExpr(BooleanExpr):# left != right
    def __init__(self, ladoEsquerdo, ladoDireito):
        self.left = ladoEsquerdo
        self.right = ladoDireito

class GreaterThanEqualsExpr(BooleanExpr):# left >= right
    def __init__(self, ladoEsquerdo, ladoDireito):
        self.left = ladoEsquerdo
        self.right = ladoDireito

class GreaterThanExpr(BooleanExpr):# left > right
    def __init__(self, ladoEsquerdo, ladoDireito):
        self.left = ladoEsquerdo
        self.right = ladoDireito

class LessThanEqualsExpr(BooleanExpr):# left <= right
    def __init__(self, ladoEsquerdo, ladoDireito):
        self.left = ladoEsquerdo
        self.right = ladoDireito

class LessThanExpr(BooleanExpr):# left < right
    def __init__(self, ladoEsquerdo, ladoDireito):
        self.left = ladoEsquerdo
        self.right = ladoDireito