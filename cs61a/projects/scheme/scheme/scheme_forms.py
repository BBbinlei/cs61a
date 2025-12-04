from scheme_eval_apply import *
from scheme_utils import *
from scheme_classes import *
from scheme_builtins import *

#################
# Special Forms #
#################

# Each of the following do_xxx_form functions takes the cdr of a special form as
# its first argument---a Scheme list representing a special form without the
# initial identifying symbol (if, lambda, quote, ...). Its second argument is
# the environment in which the form is to be evaluated.

def do_define_form(expressions, env):
    """Evaluate a define form.
    >>> env = create_global_frame()
    >>> do_define_form(read_line("(x 2)"), env) # evaluating (define x 2)
    'x'
    >>> scheme_eval("x", env)
    2
    >>> do_define_form(read_line("(x (+ 2 8))"), env) # evaluating (define x (+ 2 8))
    'x'
    >>> scheme_eval("x", env)
    10
    >>> # problem 10
    >>> env = create_global_frame()
    >>> do_define_form(read_line("((f x) (+ x 2))"), env) # evaluating (define (f x) (+ x 8))
    'f'
    >>> scheme_eval(read_line("(f 3)"), env)
    5
    """
    validate_form(expressions, 2) # Checks that expressions is a list of length at least 2
    signature = expressions.first
    if scheme_symbolp(signature):
        # assigning a name to a value e.g. (define x (+ 1 2))
        validate_form(expressions, 2, 2) # Checks that expressions is a list of length exactly 2
        # BEGIN PROBLEM 4
        # 输入 pair 环境， 输出：字符， 思路：将符号和值相绑定，再返回字符,取环境中的bindings字典，以exp的第一项为key剩余项的值为值，进行绑定，返回第一项
        sigature1 = expressions.rest.first
        if scheme_symbolp(sigature1):
            env.bindings[signature] = scheme_eval(expressions.rest, env)
        env.bindings[signature] = scheme_eval(sigature1, env)
        return expressions.first
        # END PROBLEM 4
    elif isinstance(signature, Pair) and scheme_symbolp(signature.first):
        # defining a named procedure e.g. (define (f x y) (+ x y))
        # BEGIN PROBLEM 10
        # 输出：返回符号  操作：1.提取 函数名 参数表 函数体 2.创建lambdaprocedure,导入参数名，参数体 3.将函数名与lambdaprocedure绑定
        # 4.返回函数名
        # 思路：创建变量保存expressions.rest.first.first, expressions.rest.first.rest exprssions.rest.rest,
        # 创建lambdapro 导入变量， 用define绑定函数名和procedure

        function = expressions.first.first
        formals = expressions.first.rest
        body = expressions.rest
        expression = Pair(formals, body)
        procedure = do_lambda_form(expression, env)
        Frame.define(env, function, procedure)
        return function
        # END PROBLEM 10
    else:
        bad_signature = signature.first if isinstance(signature, Pair) else signature
        raise SchemeError('non-symbol: {0}'.format(bad_signature))

def do_quote_form(expressions, env):
    """Evaluate a quote form.

    >>> env = create_global_frame()
    >>> do_quote_form(read_line("((+ x 2))"), env) # evaluating (quote (+ x 2))
    Pair('+', Pair('x', Pair(2, nil)))
    """
    validate_form(expressions, 1, 1)
    # BEGIN PROBLEM 5
    # 输入：pair  env 输出：字符串 思路：分为两种情况。有嵌套表和无嵌套表，有嵌套表就打印内部，无嵌套表就直接打印本身
    return expressions.first
    # 为什么一个return 就解决了，而print却出问题啦？ 在python中打印会去除字符的引号，而返回就不会。
    # END PROBLEM 5

def do_begin_form(expressions, env):
    """Evaluate a begin form.

    >>> env = create_global_frame()
    >>> x = do_begin_form(read_line("((print 2) 3)"), env) # evaluating (begin (print 2) 3)
    2
    >>> x
    3
    """
    validate_form(expressions, 1)
    return eval_all(expressions, env)

def do_lambda_form(expressions, env):
    """Evaluate a lambda form.
    # 输入：expr  输出： lambda procedure 实例
    思路：将formals 与 body导入类创建实例并返回
    >>> env = create_global_frame()
    >>> do_lambda_form(read_line("((x) (+ x 2))"), env) # evaluating (lambda (x) (+ x 2))
    LambdaProcedure(Pair('x', nil), Pair(Pair('+', Pair('x', Pair(2, nil))), nil), <Global Frame>)
    """
    validate_form(expressions, 2)
    formals = expressions.first
    validate_formals(formals)
    # BEGIN PROBLEM 7
    body = expressions.rest
    return LambdaProcedure(formals, body, env)
    # END PROBLEM 7

def do_if_form(expressions, env):
    """Evaluate an if form.

    >>> env = create_global_frame()
    >>> do_if_form(read_line("(#t (print 2) (print 3))"), env) # evaluating (if #t (print 2) (print 3))
    2
    >>> do_if_form(read_line("(#f (print 2) (print 3))"), env) # evaluating (if #f (print 2) (print 3))
    3
    """
    validate_form(expressions, 2, 3)
    if is_scheme_true(scheme_eval(expressions.first, env)):
        return scheme_eval(expressions.rest.first, env)
    elif len(expressions) == 3:
        return scheme_eval(expressions.rest.rest.first, env)

def do_and_form(expressions, env):
    """Evaluate a (short-circuited) and form.

    >>> env = create_global_frame()
    >>> do_and_form(read_line("(#f (print 1))"), env) # evaluating (and #f (print 1))
    False
    >>> # evaluating (and (print 1) (print 2) (print 4) 3 #f)
    >>> do_and_form(read_line("((print 1) (print 2) (print 3) (print 4) 3 #f)"), env)
    1
    2
    3
    4
    False
    """
    # BEGIN PROBLEM 12
    # 输入：pair 输出：True or False 操作：返回pair中第一个为false的值，没有就返回True
    # 思路： 基线：1.nil 返回True  2.有False 就返回False  递归：看第一个元素，True 递归其余元素， False返回
    if expressions == nil:
        return True
    val = scheme_eval(expressions.first, env)
    if is_scheme_false(val):
        return val
    elif is_scheme_true(val) and expressions.rest == nil:
        return val
    else:
        return do_and_form(expressions.rest, env)
    # END PROBLEM 12

def do_or_form(expressions, env):
    """Evaluate a (short-circuited) or form.

    >>> env = create_global_frame()
    >>> do_or_form(read_line("(10 (print 1))"), env) # evaluating (or 10 (print 1))
    10
    >>> do_or_form(read_line("(#f 2 3 #t #f)"), env) # evaluating (or #f 2 3 #t #f)
    2
    >>> # evaluating (or (begin (print 1) #f) (begin (print 2) #f) 6 (begin (print 3) 7))
    >>> do_or_form(read_line("((begin (print 1) #f) (begin (print 2) #f) 6 (begin (print 3) 7))"), env)
    1
    2
    6
    """
    # BEGIN PROBLEM 12
    # 思路：基线：nil返回False 真返回当前值   递归：当前值为假，递归调用剩余元素
    if expressions == nil:
        return False
    val = scheme_eval(expressions.first, env)
    if is_scheme_true(val):
        return val
    elif expressions.rest == nil and is_scheme_true(val):
        return val
    else:
        return do_or_form(expressions.rest, env)
    # END PROBLEM 12

def do_cond_form(expressions, env):
    """Evaluate a cond form.

    >>> do_cond_form(read_line("((#f (print 2)) (#t 3))"), create_global_frame())
    3
    """
    # 输入：expressions 环境  输出：当前值， True， False  操作：计算首个表达式的值，根据true or false 运行后续的表达式，没有就返回已计算的值，直到运行else，没有else则返回none，有就返回t 或者 表达式值
    # 代码中已经实现了当first为else的情况，expressions的元素都为pair
    # 从clause（第一个条件）开始：eval 第一个值，为true则eval_all后续表达式，为nil则返回eval值，false则迭代调用rest。
    while expressions is not nil:
        clause = expressions.first
        validate_form(clause, 1)
        if clause.first == 'else':
            test = True
            if expressions.rest != nil:
                raise SchemeError('else must be last')
        else:
            test = scheme_eval(clause.first, env)
        if is_scheme_true(test):
            # BEGIN PROBLEM 13
            if clause.rest == nil:
                return test
            else:
                return eval_all(clause.rest, env)
            # END PROBLEM 13
        expressions = expressions.rest

def do_let_form(expressions, env):
    """Evaluate a let form.

    >>> env = create_global_frame()
    >>> do_let_form(read_line("(((x 2) (y 3)) (+ x y))"), env)
    5
    """
    validate_form(expressions, 2)
    let_env = make_let_frame(expressions.first, env)
    return eval_all(expressions.rest, let_env)

def make_let_frame(bindings, env):
    """Create a child frame of Frame ENV that contains the definitions given in
    BINDINGS. The Scheme list BINDINGS must have the form of a proper bindings
    list in a let expression: each item must be a list containing a symbol
    and a Scheme expression."""
    if not scheme_listp(bindings):
        raise SchemeError('bad bindings list in let form')
    names = vals = nil
    # 第二个值都是往父帧里面去计算
    #输入：blindings列表，其内部元素也是pair列表， env， 输出：子帧  操作：提取blinding符号和值构成列表导入子帧
    #思路：先提取blindings的first 对其first和rest进行长度和形式的判断，将first导入names列表，rest求值导入vals列表，最后将构建好的names和vals列表导入帧中构建子帧
    # BEGIN PROBLEM 14
    "*** YOUR CODE HERE ***"
    while bindings != nil:
        clause = bindings.first
        name = clause.first
        validate_form(clause.rest, 1, 1)
        val = scheme_eval(clause.rest.first, env)
        # 验证
        validate_form(clause,2)
        # 构建列表
        names = Pair(name, names)
        vals = Pair(val, vals)
        validate_formals(names)
        # 迭代
        bindings = bindings.rest
    # END PROBLEM 14
    # 问题：没有理解到validate_formals 与 validate_form两个函数的用法
    return env.make_child_frame(names, vals)



def do_quasiquote_form(expressions, env):
    """Evaluate a quasiquote form with parameters EXPRESSIONS in
    Frame ENV."""
    def quasiquote_item(val, env, level):
        """Evaluate Scheme expression VAL that is nested at depth LEVEL in
        a quasiquote form in Frame ENV."""
        if not scheme_pairp(val):
            return val
        if val.first == 'unquote':
            level -= 1
            if level == 0:
                expressions = val.rest
                validate_form(expressions, 1, 1)
                return scheme_eval(expressions.first, env)
        elif val.first == 'quasiquote':
            level += 1

        return val.map(lambda elem: quasiquote_item(elem, env, level))

    validate_form(expressions, 1, 1)
    return quasiquote_item(expressions.first, env, 1)

def do_unquote(expressions, env):
    raise SchemeError('unquote outside of quasiquote')


#################
# Dynamic Scope #
#################
# 创建一个不接受参数的表达式过程，表达式的参数的值，取决于父环境的绑定
def do_mu_form(expressions, env):
    """Evaluate a mu form."""
    #输入：expr env  输出：muprocedure实例  操作 导入函数体和形参 形成mu procedure
    #思路：取expressions.first, expressions.rest 分别为形参和函数体 导入构析函数创建muprocedure
    validate_form(expressions, 2)
    formals = expressions.first
    validate_formals(formals)
    # BEGIN PROBLEM 11
    "*** YOUR CODE HERE ***"
    body = expressions.rest
    return MuProcedure(formals, body)
    # END PROBLEM 11



SPECIAL_FORMS = {
    'and': do_and_form,
    'begin': do_begin_form,
    'cond': do_cond_form,
    'define': do_define_form,
    'if': do_if_form,
    'lambda': do_lambda_form,
    'let': do_let_form,
    'or': do_or_form,
    'quote': do_quote_form,
    'quasiquote': do_quasiquote_form,
    'unquote': do_unquote,
    'mu': do_mu_form,
}