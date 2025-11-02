"""
1

Author: ASUS
Date: 2025/9/12
"""
def cake():
    print("beets")
    def pie():
        print("sweet")
        return 'cake'
    return pie
chocolate = cake()
print(lambda x : x)
b = higher_order_lambda = lambda f: lambda x: f(x)
g = lambda x : x * x
print(b(2)(g))