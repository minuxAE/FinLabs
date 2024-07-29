"""
逻辑 or
max z = x+y
s.t.
2x+3y <= 100 或者 x + y <= 50

可以使用大M法转为线性规划

2x + 3y <= 100 + uM
x + y <= 100 + (1-u)M


指示函数 indicator

如果指标变量值为1, 则约束成立, 否则约束可以被违反

x > 0 则 y=1 可以转化为

x <= yM, yM <= M + x - B
M是一个很大的数, B是一个很小的正数
"""
import gurobipy as grb

model = grb.Model()

x = model.addVar(name = 'x')
y = model.addVar(name = 'y')
model.addConstr((y==1) >> (x >= 0), name='indicator')

model.optimize()

"""
带固定成本约束

只要订货 x>0就会有固定成本k和可变成本cx, 成本函数为:

z(x) = 0 if x = 9 
z(x) = cx + k if x > 0

使用大M法可以转为线性约束

z(x) = cx + ky
s.t
x <= yM
y = {0, 1}
"""

"""
分段线性函数

对于分段线性函数可以引入SOS2约束（a special order set constraint of Type 2）, 将其转为线性规划.

在使用Gurobi的广义线性化函数时, 不能对表达式进行线性化, 而需要将表达式赋予变量, 然后再对变量进行线性化
"""


