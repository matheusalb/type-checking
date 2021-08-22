class Symbol(object):
    def __init__(self, n, t=None):
        self.name = n
        self.type = t

class BuiltinTypeSymbol(Symbol):
    def __init__(self, n):
        super().__init__(n)
    
    def __str__(self):
        return "<{class_name}(name='{n}')>".format(class_name=self.__class__.__name__, n=self.name)    
    
    __repr__ = __str__

class VarSymbol(Symbol): 
    def __init__(self, n, t, v=None):
        super().__init__(n, t)
        self.value = v
    
    def __str__(self):
        return "<{class_name}(name='{n}', type='{t}', value='{v}')>".format(
            class_name=self.__class__.__name__,
            n=self.name,
            t=self.type,
            v=self.value
        )
    
    __repr__ = __str__

class ProcedureSymbol(Symbol): 
    def __init__(self, n, params=None):
        super().__init__(n)
        self.params = params if params is not None else []
    
    def __str__(self):
        return '<{class_name}(name={n}, parameters={ps})>'.format(class_name=self.__class__.__name__, n=self.name, ps=self.params)
    
    __repr__ = __str__

class SymbolTable(object):
    def __init__(self):
        self.symbols = {}
        for primitive in ['INT', 'BOOLEAN', 'STRING']:
            self.insert(primitive, BuiltinTypeSymbol(primitive))
    
    def update(self, name, data):
        if self.lookup(name) is None:
            raise Exception("Símbolo inexistente: '%s'" % name)
        else:
            self.symbols[name] = data    
    
    def insert(self, name, data):
        self.symbols[name] = data
    
    def lookup(self, name):
        return self.symbols.get(name)#retorna um objeto Symbol ou None
    
    def __str__(self):
        symtab_header = '      Symbol Table      '
        lines = ['\n', symtab_header, '_' * len(symtab_header)]
        lines.extend(
            ('%2s: %r' % (key, value))
            for key, value in self.symbols.items()
        )
        lines.append('\n')
        s = '\n'.join(lines)
        return s
    
    __repr__ = __str__

class ScopedSymbolTable(object):
    def __init__(self, scope_name, scope_level, enclosing_scope=None):
        self.symbols = {}
        self.scope_name = scope_name
        self.scope_level = scope_level
        self.enclosing_scope = enclosing_scope
        self._init_builtins()
    
    def _init_builtins(self):
        for primitive in ['INT', 'BOOLEAN', 'STRING']:
            self.insert(primitive, BuiltinTypeSymbol(primitive))
    
    def update(self, name, data):
        if self.lookup(name) is None:
            raise Exception("Símbolo inexistente: '%s'" % name)
        else:
            self.symbols[name] = data    
    
    def insert(self, name, data):
        self.symbols[name] = data
    
    def lookup(self, name, deepSearch = True):
        if (deepSearch):
            if self.enclosing_scope is None:
                return self.symbols.get(name)#retorna um objeto Symbol ou None
            else:
                res = self.symbols.get(name)
                if res is None:
                    return self.enclosing_scope.lookup(name)
                
                return res
        else:
            return self.symbols.get(name)
    
    def __str__(self):
        h1 = 'SCOPE (SCOPED SYMBOL TABLE)'
        lines = ['\n', h1, '=' * len(h1)]
        for header_name, header_value in (
            ('Scope name', self.scope_name),
            ('Scope level', self.scope_level),
            ('Enclosing scope',
             self.enclosing_scope.scope_name if self.enclosing_scope else None
            )
        ):
            lines.append('%-15s: %s' % (header_name, header_value))
        h2 = 'Scope (Scoped symbol table) contents'
        lines.extend([h2, '-' * len(h2)])
        lines.extend(
            ('%7s: %r' % (key, value))
            for key, value in self.symbols.items()
        )
        lines.append('\n')
        s = '\n'.join(lines)
        return s
    
    __repr__ = __str__