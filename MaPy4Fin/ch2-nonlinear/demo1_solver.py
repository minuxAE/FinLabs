"""
通用非线性求解器

scipy.optimize具有多维通用求解器：
root(fun, x0, [args, method, jac, tol, ]) 找到一个向量函数的根
fsolve(func, x0, [args, fprime,...]) 找到一个函数的根
"""

import scipy.optimize as optimize

def solve_fnuc():
    y = lambda x: x**3 + 2*x**2 - 5
    dy = lambda x: 3*x**2 + 4*x
    print(optimize.fsolve(y, 5, fprime=dy))
    print(optimize.fsolve(y, -5, fprime=dy))

def main():
    solve_fnuc()

if __name__ == '__main__':
    main()