import builtins

from pair import *

class SchemeError(Exception):
    """Exception indicating an error in a Scheme program."""

################
# Environments #
################

class Frame:
    """An environment frame binds Scheme symbols to Scheme values."""

    def __init__(self, parent):
        """An empty frame with parent frame PARENT (which may be None)."""
        self.bindings = {}
        self.parent = parent

    def __repr__(self):
        if self.parent is None:
            return '<Global Frame>'
        s = sorted(['{0}: {1}'.format(k, v) for k, v in self.bindings.items()])
        return '<{{{0}}} -> {1}>'.format(', '.join(s), repr(self.parent))
#  """
    # 输入：符号 值
    # 输出：无
    # 操作：将符号于值相绑定
    # 思路：用字典将符号与值相绑定
    # """
    def define(self, symbol, value):
        """Define Scheme SYMBOL to have VALUE."""
        # BEGIN PROBLEM 1
        "*** YOUR CODE HERE ***"
        self.bindings[symbol] = value
        # END PROBLEM 1
# 输入：symbol  输出：值     操作：在当前帧或父帧找到符号所对应的值
# 思路：有递归和迭代用法，我觉得迭代用法相对来说高效一些，不过不符合工业标准，可能会使程序崩溃，简单来说就是在当前帧的字典中搜索，
 #   没找到，如果还有父帧再到父帧中去搜索，如此反复循环
# 范的错误：将实例名写错了，习惯性写self，忘记这里是循环，需要不断转换变量所指的对象
    def lookup(self, symbol):
        """Return the value bound to SYMBOL. Errors if SYMBOL is not found."""
        # BEGIN PROBLEM 1
        "*** YOUR CODE HERE ***"
        frame = self
        while frame is not None:
            if symbol in frame.bindings:
                return frame.bindings[symbol]
            frame = frame.parent
        # END PROBLEM 1
        raise SchemeError('unknown identifier: {0}'.format(symbol))


    def make_child_frame(self, formals, vals):
        """Return a new local frame whose parent is SELF, in which the symbols
        in a Scheme list of formal parameters FORMALS are bound to the Scheme
        values in the Scheme list VALS. Both FORMALS and VALS are represented
        as Pairs. Raise an error if too many or too few vals are given.



        >>> env = create_global_frame()
        >>> formals, expressions = read_line('(a b c)'), read_line('(1 2 3)')
        >>> env.make_child_frame(formals, expressions)
        <{a: 1, b: 2, c: 3} -> <Global Frame>>
        """
        # 输入：formals列表  vals列表   输出：frame实例   操作：列表个数不一致抛出SchemeError， self作为父帧，formals与vals的对应元素绑定

        # 思路：1.创建一个帧，其parent 设置为self。2.绑定：运用循环结构，反复调用帧的define行为实现符号和值的绑定

        if len(formals) != len(vals):
            raise SchemeError('Incorrect number of arguments to function call')
        # BEGIN PROBLEM 8
        "*** YOUR CODE HERE ***"
        frame = Frame(self)
        while formals != nil:
            frame.define(formals.first, vals.first)
            formals, vals = formals.rest, vals.rest
        return frame
        # END PROBLEM 8

##############
# Procedures #
##############

class Procedure:
    """The the base class for all Procedure classes."""

class BuiltinProcedure(Procedure):
    """A Scheme procedure defined as a Python function."""

    def __init__(self, py_func, need_env=False, name='builtin'):
        self.name = name
        self.py_func = py_func
        self.need_env = need_env

    def __str__(self):
        return '#[{0}]'.format(self.name)

class LambdaProcedure(Procedure):
    """A procedure defined by a lambda expression or a define form."""

    def __init__(self, formals, body, env):
        """A procedure with formal parameter list FORMALS (a Scheme list),
        whose body is the Scheme list BODY, and whose parent environment
        starts with Frame ENV."""
        assert isinstance(env, Frame), "env must be of type Frame"

        from scheme_utils import validate_type, scheme_listp
        validate_type(formals, scheme_listp, 0, 'LambdaProcedure')
        validate_type(body, scheme_listp, 1, 'LambdaProcedure')
        self.formals = formals
        self.body = body
        self.env = env

    def __str__(self):
        return str(Pair('lambda', Pair(self.formals, self.body)))

    def __repr__(self):
        return 'LambdaProcedure({0}, {1}, {2})'.format(
            repr(self.formals), repr(self.body), repr(self.env))

class MuProcedure(Procedure):
    """A procedure defined by a mu expression, which has dynamic scope.
     _________________
    < Scheme is cool! >
     -----------------
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||
    """

    def __init__(self, formals, body):
        """A procedure with formal parameter list FORMALS (a Scheme list) and
        Scheme list BODY as its definition."""
        self.formals = formals
        self.body = body

    def __str__(self):
        return str(Pair('mu', Pair(self.formals, self.body)))

    def __repr__(self):
        return 'MuProcedure({0}, {1})'.format(
            repr(self.formals), repr(self.body))
