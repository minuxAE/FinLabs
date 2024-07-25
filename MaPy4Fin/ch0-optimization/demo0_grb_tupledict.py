"""
Tupledict是dict的一个子类
"""
import gurobipy as grb

def demo1():
    model = grb.Model()

    tl = [(1, 1), (1, 2), (1, 3),
          (2, 1), (2, 2), (2, 3),
          (3, 1), (3, 2), (3, 3)]
    
    vars = model.addVars(tl, name='d')

    print(sum(vars.select(1, '*')))
    print(vars.sum(1, '*'))    

"""
Gurobi变量一般是tupledict类型
"""

def demo2():
    m = grb.Model()
    x = m.addVars(3, 4, vtype=grb.GRB.BINARY, name='x')
    m.addConstrs((x.sum(i, '*') <= 1 for i in range(3)), name='con')
    m.update()
    m.write('ch0-optimization/models/tuple_vars.lp')


def demo3():
    model = grb.Model()

    c1 = [(1, 1), (1, 2), (1, 3)]
    coeff = grb.tupledict(c1)
    coeff[(1, 1)] = 1
    coeff[(1, 2)] = 0.3
    coeff[(1, 3)] = 0.4

    vars = model.addVars(c1, name='coef')

    print(vars.prod(coeff, 1, '*'))


def main():
    demo3()

if __name__ == '__main__':
    main()