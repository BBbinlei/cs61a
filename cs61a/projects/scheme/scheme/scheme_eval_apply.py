import sys

from pair import *
from scheme_utils import *
from ucb import main, trace

import scheme_forms

##############
# Eval/Apply #
##############

def scheme_eval(expr, env, _=None): # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in Frame ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # Evaluate atoms
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr

    # All non-atomic expressions are lists (combinations)
    if not scheme_listp(expr):
        raise SchemeError('malformed list: {0}'.format(repl_str(expr)))
    first, rest = expr.first, expr.rest
    if scheme_symbolp(first) and first in scheme_forms.SPECIAL_FORMS:
        return scheme_forms.SPECIAL_FORMS[first](rest, env)
    else:
        # BEGIN PROBLEM 3
        # 题目已经把怎么实现告诉我了，我只要照着它的思路敲就可以啦 ,将多参数函数变为单参数函数可参与闭包的方式
        "*** YOUR CODE HERE ***"
        procedure = scheme_eval(first, env)
        args = rest.map(lambda expr : scheme_eval(expr, env))
        return scheme_apply(procedure, args, env)
        # scheme_apply 不是有返回值吗？为什么还要写return?
        # END PROBLEM 3

def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment."""
    """
    自己看起来是有些迷糊的，不过在看了遍文档后，思路也渐渐清晰起来了
    思路：3步：建立参数列表，判断环境需求，返回调用函数
    第一步用循环建立参数列表，第二步procedure.need_env 判断需求  第三步，返回，将参数导入调用函数
    """
    validate_procedure(procedure)
    if not isinstance(env, Frame):
       assert False, "Not a Frame: {}".format(env)
    if isinstance(procedure, BuiltinProcedure):
        # BEGIN PROBLEM 2
        "*** YOUR CODE HERE ***"
        arg = []
        while args != nil:
            arg.append(args.first)
            args = args.rest
        if procedure.need_env:
            arg.append(env)
        # END PROBLEM 2
        try:
            # BEGIN PROBLEM 2
            "*** YOUR CODE HERE ***"
            return procedure.py_func(*arg)
            # END PROBLEM 2
        except TypeError as err:
            raise SchemeError('incorrect number of arguments: {0}'.format(procedure))
    elif isinstance(procedure, LambdaProcedure):
        # BEGIN PROBLEM 9
        # 输出：值   操作：创建子帧，将procedure的符号表和值表导入进去进行绑定，调用eval_all，计算body
        # 思路：用make_child创建子帧，将formals属性和args导入进去进行绑定，然后在调用子帧的eval_all方法作用在body上
        "*** YOUR CODE HERE ***"
        child = procedure.env.make_child_frame(procedure.formals, args)
        return eval_all(procedure.body, child)
        # 错误 ：env是函数被调用时候的帧，而非过程实例所在的帧
        # END PROBLEM 9
    elif isinstance(procedure, MuProcedure):
        # BEGIN PROBLEM 11
        "*** YOUR CODE HERE ***"
        # 操作：计算出muprocedure中参数列表的值
        #思路：先创建一个子帧，然后再计算函数体
        child = env.make_child_frame(procedure.formals, args)
        return eval_all(procedure.body, child)
        # 疑问：为什么这里是函数被调用时的帧？没有帧，就意味着在什么环境中就求什么值。
        # END PROBLEM 11
    else:
        assert False, "Unexpected procedure: {}".format(procedure)

def eval_all(expressions, env):
    # 输入 expressions   输出：最后一个expressions的值
    # 思路：用循环结构，对first调用eval函数进行求值，当rest为nil时，返回当前计算值
    """Evaluate each expression in the Scheme list EXPRESSIONS in
    Frame ENV (the current environment) and return the value of the last.
    # return是将返回值与函数名称相绑定，交互是查找函数名称所对应的值，并打印出来
    >>> eval_all(read_line("(1)"), create_global_frame())
    1
    >>> eval_all(read_line("(1 2)"), create_global_frame())
    2
    >>> x = eval_all(read_line("((print 1) 2)"), create_global_frame())
    1
    >>> x
    2
    >>> eval_all(read_line("((define x 2) x)"), create_global_frame())
    2
    """
    # BEGIN PROBLEM 6
    if expressions == nil:
        return None
    while expressions.rest != nil:
        scheme_eval(expressions.first, env)
        expressions = expressions.rest
    return scheme_eval(expressions.first, env) # replace this with lines of your own code
    # END PROBLEM 6


################################
# Extra Credit: Tail Recursion #
################################

class Unevaluated:
    """An expression and an environment in which it is to be evaluated."""

    def __init__(self, expr, env):
        """Expression EXPR to be evaluated in Frame ENV."""
        self.expr = expr
        self.env = env

def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not an Unevaluated."""
    validate_procedure(procedure)
    val = scheme_apply(procedure, args, env)
    if isinstance(val, Unevaluated):
        return scheme_eval(val.expr, val.env)
    else:
        return val

def optimize_tail_calls(unoptimized_scheme_eval):
    """Return a properly tail recursive version of an eval function."""
    def optimized_eval(expr, env, tail=False):
        """Evaluate Scheme expression EXPR in Frame ENV. If TAIL,
        return an Unevaluated containing an expression for further evaluation.
        """
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return Unevaluated(expr, env)

        result = Unevaluated(expr, env)
        # BEGIN OPTIONAL PROBLEM 1
        "*** YOUR CODE HERE ***"
        # END OPTIONAL PROBLEM 1
    return optimized_eval














################################################################
# Uncomment the following line to apply tail call optimization #
################################################################

# scheme_eval = optimize_tail_calls(scheme_eval)
