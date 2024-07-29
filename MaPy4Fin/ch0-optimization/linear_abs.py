import gurobipy as grb

"""
将绝对值约束转为
min cy
s.t
y >= -x
y <= x
"""

m = grb.Model()
x = m.addVar(lb=-10, name='x')
y = m.addVar(name = 'y')

m.addConstr(y == grb.abs_(x), name='C_abs')
m.addConstr(x >= -5, name='C_2')
m.addConstr(x <= 3, name='C_3')
c = 2

m.setObjective(c * y)
m.optimize()

print('y=', y.X)
print('x=', x.X)


