class SymbolTable:
    def __init__(self):
        super().__init__()

        self.globalTable = ScopedTable(None)
        self.currentScope = self.globalTable

    def put(self, name, symbol):
        pass

    def get(self, name):
        pass

    def getParentScope(self):
        pass

    def pushScope(self, name):
        pass

    def popScope(self):
        pass


class ScopedTable:
    def __init__(self, parent: ScopedTable):
        self.parent = parent
        self.tbl = {}

    def parent(self):
        return self.parent

    def lookup(self, name):
        if name in self.tbl:
            return True

        if self.parent is not None:
            return self.parent.lookup(name)
        else:
            return False

    def get(self, name):
        if name in self.tbl:
            return self.tbl[name]

        return self.parent.get(name)


class Type:
    pass
