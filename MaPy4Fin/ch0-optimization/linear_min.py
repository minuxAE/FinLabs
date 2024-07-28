"""
z = min(x, y, 3)进行约束线性化
"""
import gurobipy as grb

def lin_min_1():
    m = grb.Model()
    x = m.addVar(name='x')
    y = m.addVar(name='y')
    z = m.addVar(name='z')

    u1 = m.addVar(vtype='B', name='u1')
    u2 = m.addVar(vtype='B', name='u2')
    u3 = m.addVar(vtype='B', name='u3')

    M = 10000

    m.addConstr(x >= z - M * (1 - u1), name='c1')
    m.addConstr(y >= z - M * (1 - u2), name='c2')
    m.addConstr(3 >= z - M * (1 - u3), name='c3')

    m.addConstr(x == 4, name='c4')
    m.addConstr(y == 5, name='c5')
    m.addConstr(u1 + u2 + u3 >= 1, name = 'c6')
    m.addConstr(x >= z, name='c7')
    m.addConstr(y >= z, name='c8')
    m.addConstr(3 >= z, name='c9')

    m.setObjective(-z)
    m.optimize()
    print('z=', z.X)

# 使用gurobi内置接口的方法
def lin_min_2():
    m = grb.Model()
    x = m.addVar(name='x')
    y = m.addVar(name='y')
    z = m.addVar(name='z')

    m.addConstr(x==4, name='c4')
    m.addConstr(y==5, name='c5')
    m.addConstr(z==grb.min_(x, y, 3))

    m.setObjective(z)
    m.optimize()

    print('z=', z.X)

if __name__ == '__main__':
    lin_min_2()
    # lin_min_1()