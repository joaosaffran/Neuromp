from pycparser import parse_file, c_ast
from collections import namedtuple
from enum import Enum
import pprint

class Token(Enum):
    CONST = 1
    ID = 2
    OP = 3
    BINOP = 4
    ASSIGN = 5

Node = namedtuple("Node", ["value",
                           "token",
                           "lineno"])

OP_LIST = [
    "=",
    "+",
    "-",
    "*",
    "/",
    "+=",
    "-=",
    "*=",
    "/="
]

VARS_TABLE = {}
MIN_ID_FOR_VARS = 16

class AST(object):
    def __init__(self):
        self.fors = []
        self._variables = set()
        super(AST, self).__init__()

    @property
    def variables(self):
        return sorted(list(self._variables))

    def _analyseNode(self, node):
        if isinstance(node, c_ast.BinaryOp):
            return self._parseBinOP(node)

        elif isinstance(node, c_ast.ID):
            return self._parseID(node)

        else:
            return self._parseConst(node)

    def _getLineno(self, coord):
        return coord.line

    def _parseConst(self, node):
        return Node(value=[node.value],
                    token=Token.CONST,
                    lineno=node.coord.line)

    def _parseID(self, node):
        n = Node(value=[node.name],
                 token=Token.ID,
                 lineno=node.coord.line)

        self._variables.add(n.value[0])
        return n

    def _parseBinOP(self, node):
        op = node.op
        left = self._analyseNode(node.left)
        right = self._analyseNode(node.right)

        return Node(value=[left,
                           Node(value=[op],
                                token=Token.OP,
                                lineno=node.coord.line),
                                right],
                           token=Token.BINOP,
                           lineno=node.coord.line)

    def _parseAssignment(self, node):
        op = node.op
        left = self._analyseNode(node.lvalue)
        right = self._analyseNode(node.rvalue)

        return Node(value=[left,
                           Node(value=[op], token=Token.OP, lineno=node.coord.line),
                           right],
                           token=Token.ASSIGN,
                           lineno=node.coord.line)


    def printNode(self, node):
        for n in node.value:
            if len(n.value) > 1:
                print("(", end='')
                self.printNode(n)
                print(")", end='')
            else:
                print(n.value[0], end='')

    def preproStatement(self, stmt):
        global MIN_ID_FOR_VARS
        resp = []
        if isinstance(stmt.value[0], Node):
            for x in stmt.value:
                resp += self.preproStatement(x)
        else:
            if stmt.token == Token.OP:
                resp.append(4 + OP_LIST.index(stmt.value[0]))
            elif stmt.token == Token.ID:
                value = stmt.value[0]
                if value in VARS_TABLE:
                    resp.append(VARS_TABLE[value])
                else:
                    VARS_TABLE[value] = MIN_ID_FOR_VARS
                    resp.append(MIN_ID_FOR_VARS)
                    MIN_ID_FOR_VARS += 1
            else:
                resp.append(stmt.token.value)
        return resp


    def parse(self, f):
        statements = []
        ast = parse_file(f, use_cpp=True,
                            cpp_path='clang',
                            cpp_args=['-E', r'-I../../utils/fake_libc_include'])

        for n in ast.ext:
            if isinstance(n, c_ast.FuncDef):
                for node in n.body.block_items:
                    if isinstance(node, c_ast.For):
                        self.fors.append(node.coord.line)
                        for stmt in node.stmt.block_items:
                            if isinstance(stmt, c_ast.Assignment):
                                statements.append(self._parseAssignment(stmt))
        return statements

if __name__ == "__main__":
    ast = AST()
    pp = pprint.PrettyPrinter(indent=4)
    feats = ast.parse("../data/pi.c")
    for f in feats:
        print(ast.preproStatement(f))
