import operator
from typing import Dict

from pyparsing import Literal, Word, ZeroOrMore, Forward, alphas, Regex, Suppress, oneOf, Optional

__all__ = 'berekenen'

# Based on https://github.com/pyparsing/pyparsing/blob/master/examples/fourFn.py
# Stripped down to a minimum
# Implementation can be considered quick and dirty

point = Literal(".")
fnumber = Regex(r"[+-]?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?")
ident = Word(alphas + "_")

plus = Literal("+")
minus = Literal("-")
mult = Literal("*")
div = Literal("/")

lpar, rpar = map(Suppress, "()")
addop  = plus | minus
multop = mult | div

unary_op = {
    'ABS': abs,
}


def veilig_delen(x, y):
    if abs(float(y)) < 1e-6:
        raise RekenFout(f"Kan {x} niet delen door te kleine waarde {y}")

    return float(x) / float(y)

binary_op = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': veilig_delen,
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le,
    '=': operator.eq,
}


class RekenFout(Exception):
    def __init__(self, melding):
        self.melding = melding
        super(RekenFout, self).__init__(melding)


class Rekenmachine(object):
    def __init__(self, omgeving):
        self._stack = []
        self._bnf = self._make_bnf()
        self._omgeving = omgeving

    def _make_bnf(self):
        expr = Forward()
        atom = (fnumber | (ident + lpar + expr + rpar) | ident | (lpar + expr + rpar)).setParseAction(self._push_stack)
        term = atom + ZeroOrMore((multop + atom).setParseAction(self._push_stack))
        expr << term + ZeroOrMore((addop + term).setParseAction(self._push_stack))
        comp = Literal('>') | Literal('<') | Literal('=') | Literal('>=') | Literal('<=')
        comp_expr = expr + Optional((comp + expr).setParseAction(self._push_stack))
        return comp_expr

    def _push_stack(self, _1, _2, toks):
        """Zet een operator of waarde op de stack."""
        self._stack.append(toks[0])

    def _reduce_stack(self):
        """Reduceer de stack tot een enkele waarde.

        Bijvoorbeeld:
            stack [4, 5, + 3, -]
        wordt gereduceerd tot 6

        Eigenlijk is dit RPN-notatie:
        http://concatenative.org/wiki/view/Factor/Examples
        """
        
        op = self._stack.pop()
        if op in unary_op:
            return unary_op[op](self._reduce_stack())
        elif op in binary_op:
            rechter_operand = self._reduce_stack()
            linker_operand = self._reduce_stack()
            return binary_op[op](linker_operand, rechter_operand)
        elif op in self._omgeving:
            return self._omgeving[op]
        elif op[0].isdigit():
            return float(op)
        else:
            raise RekenFout(f"Rekenmachine kan niet omgaan met {op}")

    def bereken(self, expressie):
        self._bnf.parseString(expressie, parseAll=True)
        return self._reduce_stack()


def bereken(formule: str, omgeving: Dict[str, float]):
    """
    Voer de formule uit.

    :param formule: string met uit te voeren formule
    :param omgeving: dict met te gebruiken parameters
    """

    rekenmachine = Rekenmachine(omgeving)
    return rekenmachine.bereken(formule)
