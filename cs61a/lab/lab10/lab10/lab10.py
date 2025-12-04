############## You do not need to understand any of this code!
import base64
ob = "CmRlZiBhZGRpdGlvbihleHByKToKICAgIGRpdmlkZW5kID0gZXhwci5maXJzdAogICAgZXhwciA9IGV4cHIucmVzdAogICAgd2hpbGUgZXhwciAhPSBuaWw6CiAgICAgICAgZGl2aXNvciA9IGV4cHIuZmlyc3QKICAgICAgICBkaXZpZGVuZCArPSBkaXZpc29yCiAgICAgICAgZXhwciA9IGV4cHIucmVzdAogICAgcmV0dXJuIGRpdmlkZW5kCgpkZWYgc3VidHJhY3Rpb24oZXhwcik6CiAgICBkaXZpZGVuZCA9IGV4cHIuZmlyc3QKICAgIGV4cHIgPSBleHByLnJlc3QKICAgIHdoaWxlIGV4cHIgIT0gbmlsOgogICAgICAgIGRpdmlzb3IgPSBleHByLmZpcnN0CiAgICAgICAgZGl2aWRlbmQgLT0gZGl2aXNvcgogICAgICAgIGV4cHIgPSBleHByLnJlc3QKICAgIHJldHVybiBkaXZpZGVuZAoKZGVmIG11bHRpcGxpY2F0aW9uKGV4cHIpOgogICAgZGl2aWRlbmQgPSBleHByLmZpcnN0CiAgICBleHByID0gZXhwci5yZXN0CiAgICB3aGlsZSBleHByICE9IG5pbDoKICAgICAgICBkaXZpc29yID0gZXhwci5maXJzdAogICAgICAgIGRpdmlkZW5kICo9IGRpdmlzb3IKICAgICAgICBleHByID0gZXhwci5yZXN0CiAgICByZXR1cm4gZGl2aWRlbmQKCmRlZiBkaXZpc2lvbihleHByKToKICAgIGRpdmlkZW5kID0gZXhwci5maXJzdAogICAgZXhwciA9IGV4cHIucmVzdAogICAgd2hpbGUgZXhwciAhPSBuaWw6CiAgICAgICAgZGl2aXNvciA9IGV4cHIuZmlyc3QKICAgICAgICBkaXZpZGVuZCAvPSBkaXZpc29yCiAgICAgICAgZXhwciA9IGV4cHIucmVzdAogICAgcmV0dXJuIGRpdmlkZW5kCg=="
exec(base64.b64decode(ob.encode("ascii")).decode("ascii"))
##############
# 输入：pair 列表  输出：各种值  操作：赋值 计算 查找
def calc_eval(exp):
    """
    >>> calc_eval(Pair("define", Pair("a", Pair(1, nil))))
    'a'
    >>> calc_eval("a")
    1
    >>> calc_eval(Pair("+", Pair(1, Pair(2, nil))))
    3
    """
    if isinstance(exp, Pair):
        operator = exp.first # UPDATE THIS FOR Q2, e.g (+ 1 2), + is the operator
        operands = exp.rest # UPDATE THIS FOR Q2, e.g (+ 1 2), 1 and 2 are operands
        if operator == 'and': # and expressions
            return eval_and(operands)
        elif operator == 'define': # define expressions
            return eval_define(operands)
        else: # Call expressions
            return calc_apply(calc_eval(operator), operands) # UPDATE THIS FOR Q2, what is type(operator)?
    elif exp in OPERATORS:   # Looking up procedures
        return OPERATORS[exp]
    elif isinstance(exp, int) or isinstance(exp, bool):   # Numbers and booleans
        return exp
    elif exp in bindings : # CHANGE THIS CONDITION FOR Q4 where are variables stored?
        return bindings[exp] # UPDATE THIS FOR Q4, how do you access a variable?

def calc_apply(op, args):
    return op(args)

"""
输入 pair 输出 num
思路：运用calc_eval，将第一个数设为被除数，其他的设为除数，反复取被除数作除法
"""
def floor_div(args):
    """
    >>> floor_div(Pair(100, Pair(10, nil)))
    10
    >>> floor_div(Pair(5, Pair(3, nil)))
    1
    >>> floor_div(Pair(1, Pair(1, nil)))
    1
    >>> floor_div(Pair(5, Pair(2, nil)))
    2
    >>> floor_div(Pair(23, Pair(2, Pair(5, nil))))
    2
    >>> calc_eval(Pair("//", Pair(4, Pair(2, nil))))
    2
    >>> calc_eval(Pair("//", Pair(100, Pair(2, Pair(2, Pair(2, Pair(2, Pair(2, nil))))))))
    3
    >>> calc_eval(Pair("//", Pair(100, Pair(Pair("+", Pair(2, Pair(3, nil))), nil))))
    20
    """
    "*** YOUR CODE HERE ***"
    divisor = args.first
    while args.rest != nil:
        args = args.rest
        divided = calc_eval(args.first)
        divisor //= divided
    return divisor
scheme_t = True   # Scheme's #t
scheme_f = False  # Scheme's #f
'''
输入 ： pair  输出： True 或 False
思路：递归：合并第n个与剩余n-1个的正确性，如果为false则返回当前值，如果不是则递归调用n-1，直到nil，返回True
基线条件：False或为nil    


'''
def eval_and(expressions):
    """
    >>> calc_eval(Pair("and", Pair(1, nil)))
    1
    >>> calc_eval(Pair("and", Pair(False, Pair("1", nil))))
    False
    >>> calc_eval(Pair("and", Pair(1, Pair(Pair("//", Pair(5, Pair(2, nil))), nil))))
    2
    >>> calc_eval(Pair("and", Pair(Pair('+', Pair(1, Pair(1, nil))), Pair(3, nil))))
    3
    >>> calc_eval(Pair("and", Pair(Pair('-', Pair(1, Pair(0, nil))), Pair(Pair('/', Pair(5, Pair(2, nil))), nil))))
    2.5
    >>> calc_eval(Pair("and", Pair(0, Pair(1, nil))))
    1
    >>> calc_eval(Pair("and", nil))
    True
    """
    "*** YOUR CODE HERE ***"

    if expressions == nil:
        return scheme_t
    val = calc_eval(expressions.first)
    if val is scheme_f:
        return val
    if expressions.rest == nil:
        return val

    return eval_and(expressions.rest)

bindings = {}
"""
输入：pair 输出：字符
思路：保存一个字面量，计算剩余字面量的值，用字典将第一个字面量与剩余值相绑定


"""
def eval_define(expressions):
    """
    >>> eval_define(Pair("a", Pair(1, nil)))
    'a'
    >>> eval_define(Pair("b", Pair(3, nil)))
    'b'
    >>> eval_define(Pair("c", Pair("a", nil)))
    'c'
    >>> calc_eval("c")
    1
    >>> calc_eval(Pair("define", Pair("d", Pair("//", nil))))
    'd'
    >>> calc_eval(Pair("d", Pair(4, Pair(2, nil))))
    2
    """
    "*** YOUR CODE HERE ***"
    ob = expressions.first
    val = calc_eval(expressions.rest.first)
    bindings[ob] = val
    return ob

OPERATORS = { "//": floor_div, "+": addition, "-": subtraction, "*": multiplication, "/": division }

class Pair:
    """A pair has two instance attributes: first and rest. rest must be a Pair or nil

    >>> s = Pair(1, Pair(2, nil))
    >>> s
    Pair(1, Pair(2, nil))
    >>> print(s)
    (1 2)
    >>> print(s.map(lambda x: x+4))
    (5 6)
    """
    def __init__(self, first, rest):
        self.first = first
        self.rest = rest

    def __repr__(self):
        return 'Pair({0}, {1})'.format(repr(self.first), repr(self.rest))

    def __str__(self):
        s = '(' + str(self.first)
        rest = self.rest
        while isinstance(rest, Pair):
            s += ' ' + str(rest.first)
            rest = rest.rest
        if rest is not nil:
            s += ' . ' + str(rest)
        return s + ')'

    def __len__(self):
        n, rest = 1, self.rest
        while isinstance(rest, Pair):
            n += 1
            rest = rest.rest
        if rest is not nil:
            raise TypeError('length attempted on improper list')
        return n

    def __eq__(self, p):
        if not isinstance(p, Pair):
            return False
        return self.first == p.first and self.rest == p.rest

    def map(self, fn):
        """Return a Scheme list after mapping Python function FN to SELF."""
        mapped = fn(self.first)
        if self.rest is nil or isinstance(self.rest, Pair):
            return Pair(mapped, self.rest.map(fn))
        else:
            raise TypeError('ill-formed list')

class nil:
    """The empty list"""

    def __repr__(self):
        return 'nil'

    def __str__(self):
        return '()'

    def __len__(self):
        return 0

    def map(self, fn):
        return self

nil = nil() # Assignment hides the nil class; there is only one instance

