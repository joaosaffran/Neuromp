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
    CALL = 6,
    TERNARY = 7
    ARRAY = 8
    IF = 9
    COMPOUND=10
    GOTO=11

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
    ">",
    "<",
    ">=",
    "<=",
]

VARS_TABLE = {}
MIN_ID_FOR_VARS = 100

class AST(object):
    def __init__(self):
        self.fors = []
        self._variables = set()
        super(AST, self).__init__()

    @property
    def variables(self):
        return sorted(list(self._variables))

    def _analyseNode(self, node):
        #print(node)
        if isinstance(node, c_ast.BinaryOp):
            return self._parseBinOP(node)

        elif isinstance(node, c_ast.ID):
            return self._parseID(node)

        elif isinstance(node, c_ast.FuncCall):
            return self._parseFuncCall(node)

        elif isinstance(node, c_ast.TernaryOp):
            return self._parseTernaryOp(node)

        elif isinstance(node, c_ast.ArrayRef):
            return self._parseArrayRef(node)

        elif isinstance(node, c_ast.Cast):
            return Node(value=['cast'],
                        token=Token.CONST,
                        lineno=node.coord.line)

        elif isinstance(node, c_ast.Decl):
            return Node(value=['decl'],
                        token=Token.CONST,
                        lineno=node.coord.line)

        elif isinstance(node, c_ast.If):
            return self._parseIf(node)

        elif isinstance(node, c_ast.Compound):
            return Node(value=[self._analyseNode(n) for n in node.block_items],
                        token=Token.COMPOUND,
                        lineno=node.coord.line)

        elif isinstance(node, c_ast.Assignment):
            return self._parseAssignment(node)

        elif isinstance(node, c_ast.UnaryOp):
            return Node(value=node.op,
                        token=Token.OP,
                        lineno=node.coord.line)

        elif isinstance(node, c_ast.Break):
            return Node(value='break',
                        token=Token.OP,
                        lineno=node.coord.line)
        elif isinstance(node, c_ast.For):
            return self._parseFor(node)

        elif isinstance(node, c_ast.Goto):
            return Node(value='GOTO',
                        token=Token.GOTO,
                        lineno=node.coord.line)
        elif isinstance(node, c_ast.Label):
            return Node(value=[self._analyseNode(node.stmt)],
                        token=Token.OP,
                        lineno=node.coord.line)
        else:
            return self._parseConst(node)

    def _getLineno(self, coord):
        return coord.line

    def _parseArrayRef(self, node):
        return Node(value=[self._analyseNode(node.subscript)],
                    token=Token.ARRAY,
                    lineno=node.coord.line)

    def _parseIf(self, node):
        aux = []
        aux.append(self._analyseNode(node.cond))

        if node.iftrue != None:
            aux.append(self._analyseNode(node.iftrue))

        if node.iffalse != None:
            aux.append(self._analyseNode(node.iffalse))

        return Node(value=aux,
                    token=Token.IF,
                    lineno=node.coord.line)

    def _parseTernaryOp(self, node):
        return Node( value=[
                        self._analyseNode(node.cond),
                        self._analyseNode(node.iftrue),
                        self._analyseNode(node.iffalse)],
                    token=Token.TERNARY,
                    lineno=node.coord.line
                )

    def _parseFuncCall(self, node):
        if node.args != None:
            return Node( value=[self._analyseNode(n) for n in node.args.exprs],
                        token=Token.CALL,
                        lineno=node.coord.line)
        else:
            return Node( value=[],
                        token=Token.CALL,
                        lineno=node.coord.line)



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


    def _parseFor(self, node):
        resp = []
        self.fors.append(node.coord.line)
        print(node.stmt.coord.line)
        for stmt in node.stmt.block_items:
            if isinstance(stmt, c_ast.Assignment):
                resp.append(self._parseAssignment(stmt))
            elif isinstance(stmt, c_ast.If):
                resp += self._parseIf(stmt)
            elif isinstance(stmt, c_ast.For):
                resp += self._parseFor(stmt)
            elif isinstance(stmt, c_ast.While):
                resp.append(self._parseBinOP(stmt.cond))
                resp.append(Node(value=[self._analyseNode(n) for n in stmt.stmt.block_items],
                        token=Token.COMPOUND,
                        lineno=node.coord.line))

        return resp

    def parse(self, f):
        statements = []
        can_parse = False
        ast = parse_file(f, use_cpp=True,
                            cpp_path='g++',
                            cpp_args=['-E', r'-I../utils/fake_libc_include'])

        for n in ast.ext:
            if isinstance(n, c_ast.FuncDef):
                for node in n.body.block_items:

                    if isinstance(node, c_ast.Pragma):
                        if node.string == "neuromp":
                            can_parse = True

                    if isinstance(node, c_ast.For) and can_parse:
                        can_parse = False
                        statements += self._parseFor(node)

                    elif isinstance(node, c_ast.While):
                        for n in node.stmt.block_items:
                            if isinstance(node, c_ast.Pragma):
                                if node.string == "pragma neuromp":
                                    can_parse = True

                            if isinstance(n, c_ast.For):
                                can_parse = False
                                statements += self._parseFor(n)
        return statements

if __name__ == "__main__":
    ast = AST()
    pp = pprint.PrettyPrinter(indent=4)
    feats = ast.parse("../data/old_pi.c")
    #feats = ast.parse("../data/CAPBenchmarks/x86/src/GF/gauss-filter.c")
    pp.pprint(feats)
    for f in feats:
        print(ast.preproStatement(f))
