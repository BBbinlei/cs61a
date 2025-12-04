passphrase = 'REPLACE_THIS_WITH_PASSPHRASE'

def midsem_survey(p):
    """
    You do not need to understand this code.
    >>> midsem_survey(passphrase)
    '2bf925d47c03503d3ebe5a6fc12d479b8d12f14c0494b43deba963a0'
    """
    import hashlib
    return hashlib.sha224(p.encode('utf-8')).hexdigest()


class VendingMachine:
    """A vending machine that vends some product for some price.

    >>> v = VendingMachine('candy', 10)
    >>> v.vend()
    'Nothing left to vend. Please restock.'
    >>> v.add_funds(15)
    'Nothing left to vend. Please restock. Here is your $15.'
    >>> v.restock(2)
    'Current candy stock: 2'
    >>> v.vend()
    'Please add $10 more funds.'
    >>> v.add_funds(7)
    'Current balance: $7'
    >>> v.vend()
    'Please add $3 more funds.'
    >>> v.add_funds(5)
    'Current balance: $12'
    >>> v.vend()
    'Here is your candy and $2 change.'
    >>> v.add_funds(10)
    'Current balance: $10'
    >>> v.vend()
    'Here is your candy.'
    >>> v.add_funds(15)
    'Nothing left to vend. Please restock. Here is your $15.'

    >>> w = VendingMachine('soda', 2)
    >>> w.restock(3)
    'Current soda stock: 3'
    >>> w.restock(3)
    'Current soda stock: 6'
    >>> w.add_funds(2)
    'Current balance: $2'
    >>> w.vend()
    'Here is your soda.'
    """
    def __init__(self, product, price):
        """Set the product and its price, as well as other instance attributes."""
        "*** YOUR CODE HERE ***"
        # 商品 商品价格 商品数量 balance
        self.product = product
        self.price = price
        self.stock = 0
        self.balance = 0
        self.message = None

    def restock(self, n):
        """Add n to the stock and return a message about the updated stock level.

        E.g., Current candy stock: 3
        """
        "*** YOUR CODE HERE ***"
        # 商品数量+n， 返回current {product} stock：num
        self.stock += n
        self.message = f"Current {self.product} stock: {self.stock}"
        return self.message

    def add_funds(self, n):
        """If the machine is out of stock, return a message informing the user to restock
        (and return their n dollars).

        E.g., Nothing left to vend. Please restock. Here is your $4.
        Nothing left to vend. please restock. Here is your $n
        Otherwise, add n to the balance and return a message about the updated balance.

        E.g., Current balance: $4
        """
        "*** YOUR CODE HERE ***"
        # if num == 0 Nothing, else: Current balance: ${balance}
        if self.stock == 0:
            self.message = f"Nothing left to vend. Please restock. Here is your ${n}."
            self.balance = 0
        else:
            self.balance += n
            self.message = f"Current balance: ${self.balance}"
        return self.message
    def vend(self):
        """Dispense the product if there is sufficient stock and funds and
        return a message. Update the stock and balance accordingly.

        E.g., Here is your candy and $2 change.

        If not, return a message suggesting how to correct the problem.

        E.g., Nothing left to vend. Please restock.
              Please add $3 more funds.
        """
        "*** YOUR CODE HERE ***"
        # if suffient: Here is your candy and $balance - price change(if 0:missing)  else: if stock == 0: Nothing left to vend. Please restock
        # else Please add $price - balance
        if self.stock > 0 and self.balance >= self.price:
            if self.price == self.balance:
                self.message = f"Here is your {self.product}."
            else:
                self.message = f"Here is your {self.product} and ${self.balance - self.price} change."
            self.balance = 0
            self.stock -= 1
        else:
            if self.stock == 0:
                self.message = f"Nothing left to vend. Please restock."
            else:
                self.message = f"Please add ${self.price - self.balance} more funds."
        return self.message
    # 事前没有考虑到局部状态的变化，时候没有注意到局部状态的变化
def store_digits(n):
    """Stores the digits of a positive number n in a linked list.

    >>> s = store_digits(1)
    >>> s
    Link(1)
    >>> store_digits(2345)
    Link(2, Link(3, Link(4, Link(5))))
    >>> store_digits(876)
    Link(8, Link(7, Link(6)))
    >>> store_digits(2450)
    Link(2, Link(4, Link(5, Link(0))))
    >>> store_digits(20105)
    Link(2, Link(0, Link(1, Link(0, Link(5)))))
    >>> # a check for restricted functions
    >>> import inspect, re
    >>> cleaned = re.sub(r"#.*\\n", '', re.sub(r'"{3}[\s\S]*?"{3}', '', inspect.getsource(store_digits)))
    >>> print("Do not use str or reversed!") if any([r in cleaned for r in ["str", "reversed"]]) else None
    """
    "*** YOUR CODE HERE ***"
    # 取余迭代操作得到的位是从右到左的，而题目要求的是从左到右的，跟迭代顺序相反的操作，很自然的就想到了递归
    # 现想到两种思路，一种是迭代，从里向外构造，一种是递归，从外向里添加，还是要用到循环，两种权衡，用迭代
    "设置三个变量 digit rest_list new_list,"
    "所有位取完时循环终止，在此之前，取位，与旧链表一起构建新链表"
    rest_list = Link.empty
    while(n > 0):
        digit = n % 10
        n = n // 10
        new_list = Link(digit, rest_list)
        rest_list = new_list
    return new_list


def deep_map_mut(func, s):
    """Mutates a deep link s by replacing each item found with the
    result of calling func on the item. Does NOT create new Links (so
    no use of Link's constructor).

    Does not return the modified Link object.
"输入：函数和链表  输出：None  副作用：映射链表中的元素"
    >>> link1 = Link(3, Link(Link(4), Link(5, Link(6))))
    >>> print(link1)
    <3 <4> 5 6>
    >>> # Disallow the use of making new Links before calling deep_map_mut
    >>> Link.__init__, hold = lambda *args: print("Do not create any new Links."), Link.__init__
    >>> try:
    ...     deep_map_mut(lambda x: x * x, link1)
    ... finally:
    ...     Link.__init__ = hold
    >>> print(link1)
    <9 <16> 25 36>
    """
    "*** YOUR CODE HERE ***"
    "判断链表的first 如果不是链表则调用func修改first 如果是，则对first递归调用 deep_map_mut，随后递归调用s.rest，当first不是链表和rest为空时递归停止"
    "A =A1 + A2     f(A) = f(A1) + f(A2) + stop(f(A1), f(A2))"
    if s.rest == Link.empty and not isinstance(s.first, Link):
        s.first = func(s.first)
        return None
    if isinstance(s.first, Link):
        deep_map_mut(func, s.first)
    else:
        s.first = func(s.first)
    deep_map_mut(func, s.rest)
    # 写return 写上瘾了，在需要多部分递归的情况下，用return往往只能计算一部分递归
def two_list(vals, counts):
    """
    Returns a linked list according to the two lists that were passed in. Assume
    vals and counts are the same size. Elements in vals represent the value, and the
    corresponding element in counts represents the number of this value desired in the
    final linked list. Assume all elements in counts are greater than 0. Assume both
    lists have at least one element.
    >>> a = [1, 3]
    >>> b = [1, 1]
    >>> c = two_list(a, b)
    >>> c
    Link(1, Link(3))
    >>> a = [1, 3, 2]
    >>> b = [2, 2, 1]
    >>> c = two_list(a, b)
    >>> c
    Link(1, Link(1, Link(3, Link(3, Link(2)))))
    """
    "*** YOUR CODE HERE ***"
    # 输入：两个列表， 输出：一个链表
    "可以用迭代从里向外构造，也可以用递归从外向里构造，我想用递归，因为这样有趣一些"
    "先从列表中的第一个元素开始构造，每次递归对应次数减1，当对应次数为0时，去这个元素以后的切片，当列表为空时，返回empty"
    if vals == []:
        return Link.empty
    if counts[0] > 0:
        counts[0] -= 1
        return Link(vals[0], two_list(vals, counts))
    else:
        return two_list(vals[1:], counts[1:])


class Link:
    """A linked list.

    >>> s = Link(1)
    >>> s.first
    1
    >>> s.rest is Link.empty
    True
    >>> s = Link(2, Link(3, Link(4)))
    >>> s.first = 5
    >>> s.rest.first = 6
    >>> s.rest.rest = Link.empty
    >>> s                                    # Displays the contents of repr(s)
    Link(5, Link(6))
    >>> s.rest = Link(7, Link(Link(8, Link(9))))
    >>> s
    Link(5, Link(7, Link(Link(8, Link(9)))))
    >>> print(s)                             # Prints str(s)
    <5 7 <8 9>>
    """
    empty = ()

    def __init__(self, first, rest=empty):
        assert rest is Link.empty or isinstance(rest, Link)
        self.first = first
        self.rest = rest

    def __repr__(self):
        if self.rest is not Link.empty:
            rest_repr = ', ' + repr(self.rest)
        else:
            rest_repr = ''
        return 'Link(' + repr(self.first) + rest_repr + ')'

    def __str__(self):
        string = '<'
        while self.rest is not Link.empty:
            string += str(self.first) + ' '
            self = self.rest
        return string + str(self.first) + '>'

