class SymbolTable:
    def __init__(self):
        super().__init__()

        self.globalTable = ScopedTable(None)
        self.currentScope = self.globalTable

    def put(self, name, symbol):
        self.currentScope.put(name, symbol)

    def get(self, name):
        return self.currentScope.get(name)

    def pushScope(self):
        self.currentScope = ScopedTable(self.currentScope)

    def popScope(self):
        self.currentScope = self.currentScope.parentTable()


class ScopedTable:
    def __init__(self, parent: 'ScopedTable'):
        self.parent = parent
        self.tbl = {}

    def parentTable(self):
        return self.parent

    def lookup(self, name):
        if name in self.tbl:
            return True

        if self.parent() is not None:
            return self.parent.lookup(name)
        else:
            return False

    def put(self, name, symbol):
        self.tbl[name] = symbol

    def get(self, name):
        if name in self.tbl:
            return self.tbl[name]

        return self.parent().get(name)


class Type:
    pass
