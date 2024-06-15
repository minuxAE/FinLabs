"""
期权三种类型

1. 实值期权：看涨期权行权价格低于相关期货合约行权时市场价格，该看涨期权具有内含价值。看跌期权行权价格高于相关期货合约时的市场价格，该看跌期权具有内涵价值
2. 虚值期权：行权价格高于当时期货市场的看涨期权或者行权价低于当时期货市场价格的看跌期权。虚值期权不具有内涵价值
3. 平值期权：平值期权的行权价格等于标的资产的市场价格。平值期权不具有内涵价值，但是具有时间价值

Markov regime-switching model: Markov转换模型, 可以在不同机制状态下描述时间序列, 对应不同的经济状态转换

Threshold Autoregressive Model. TAR 用于解释非线性时间序列最常见的自回归模型

平滑转换模型 引入平滑函数到机制急剧转换的状态中
"""
import numpy as np
"""
增量法: 求解非线性函数的简略方法
"""

def incremental_search(f, a, b, dx):
    """
    f: function to solve
    a: left boundary
    b: right boundary
    dx: incremental value
    return x-axis value of the root
    """
    fa = f(a)
    c = a+dx
    fc = f(c)
    n = 1

    while np.sign(fa) == np.sign(fc):
        if a >= b:
            return a-dx, n
        
        a = c
        fa = fc
        c = a + dx
        fc = f(c)
        n += 1

    if fa == 0:
        return a, n
    elif fc == 0:
        return c, n
    else:
        return (a + c)/2. , n
    

def inc_solver():
    y = lambda x: x**3 + 2.0*x**2 - 5.
    root, iterations = incremental_search(y, -5, 5, 0.001)
    print('root is {:.4f} and iterations are {}'.format(root, iterations))


"""
bisection method: 简单的一维求根法, 在于求出连续函数f(x)=0的x值
"""
def bisection(f, a, b, tol=0.1, maxiter=10):
    c = (a+b)*0.5
    n = 1
    while n <= maxiter:
        c = (a+b)*0.5
        if f(c) == 0 or abs(a-b)*0.5 < tol:
            return c, n
        
        n += 1
        if f(c) < 0:
            a = c
        else:
            b = c

    return c, n

def bis_solver():
    y = lambda x: x**3+2*x**2 - 5
    root, iterations = bisection(y, -5, 5, 0.001)
    print('root is {:.4f} and iterations are {}'.format(root, iterations))

"""
Newton's method: x(1) = x - f(x) / f'(x)
"""
def newton(f, df, x, tol=0.001, maxiter=100):
    n = 1
    while n <= maxiter:
        x1 = x - f(x) / df(x)
        if abs(x1 - x) < tol:
            return x1, n
        else:
            x = x1
            n += 1

    return None, x

def newton_solver():
    y = lambda x: x**3 + 2*x**2 - 5
    dy = lambda x: 3*x**2 + 4*x

    root, iterations = newton(y, dy, 5.0, 0.00001, 100)
    print('root is {:.4f} and iterations are {}'.format(root, iterations))

"""
割线法(secant method) 利用割线求根, 速度可以看作为超线性收敛, 速度快于二分法但是慢于牛顿迭代法
"""
def secant(f, a, b, tol=0.001, maxiter=100):
    n = 1
    while n <= maxiter:
        c = b - f(b)*((b-a) / (f(b)-f(a)))
        if abs(c-b) < tol:
            return c, n

        a=b
        b=c
        n+=1

    return None, n

def secant_solver():
    y = lambda x: x**3 + 2*x**2 - 5
    root, iterations = secant(y, -5.0, 5.0, 0.00001, 100)
    print('root is {:.4f} and iterations are {}'.format(root, iterations))

"""
Brent结合了二分法, 割线法和逆二次插值法(inverse quadratic interpolation), 可以调用scipy.optimize.brentq函数实现
"""
import scipy.optimize as optimize

def call_scipy_method():
    y = lambda x: x**3 + 2*x**2 - 5
    dy = lambda x: 3*x**2 + 4*x

    print('Bisection method is {:.4f}'.format(optimize.bisect(y, -5, 5, xtol=0.00001)))
    print('Newton method is {:.4f}'.format(optimize.newton(y, 5, fprime=dy)))
    print('Secant method is {:.4f}'.format(optimize.newton(y, 5)))
    print('Brent method is {:.4f}'.format(optimize.brentq(y, -5, 5)))
    
def main():
    call_scipy_method()
    # secant_solver()
    # newton_solver()
    # inc_solver()
    # bis_solver()

if __name__ == '__main__':
    main()

