from Ast import Ast
from treelib import Node, Tree


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


class TreePrinter:
    separator = ' | '

    @addToClass()
    def printTree(self, indent):
        """
            Basic text tree representation.
        """
        print(TreePrinter.separator * indent + str(self))
        for child in self.children:
            child.printTree(indent + 1)

    @addToClass(Ast)
    def printFancyTree(self):
        """
            This one produces more friendly output.
        """
        tree = Tree()
        tree.create_node(tag=str(self), identifier=1)
        parents = [(1, self.children)]
        nextParents = []

        for i in range(2):
            for (id, children) in parents:
                for child in children:
                    node = tree.create_node(tag=str(child), parent=id)
                    if len(child.children) > 0:
                        nextParents.append((node.identifier, child.children))

            parents = nextParents

        tree.show(line_type="ascii-ex", reverse=False)
