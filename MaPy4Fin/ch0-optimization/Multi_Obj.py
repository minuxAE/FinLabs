"""
多目标优化的方法：
1.合成型：将多个目标转化为单目标决策问题
2.分层型：在保证第一目标的情况下，尽量优化第二、三目标

在多目标规划中, Pareto是这样一个解, 对其中一个目标的优化必然会导致其他目标变差, 所有Pareto最优解组成
Pareto最优集合. 所有Pareto最优解组成的曲面称为Pareto前沿

Gurobi中, 目标规划使用分层规划的方式实现
"""

import gurobipy as grb

m = grb.Model()

# decision variables
d11 = m.addVar(lb=0, vtype=grb.GRB.CONTINUOUS, name='d11')
d12 = m.addVar(lb=0, vtype=grb.GRB.CONTINUOUS, name='d12')
d21 = m.addVar(lb=0, vtype=grb.GRB.CONTINUOUS, name='d21')
d22 = m.addVar(lb=0, vtype=grb.GRB.CONTINUOUS, name='d22')
d31 = m.addVar(lb=0, vtype=grb.GRB.CONTINUOUS, name='d31')
d32 = m.addVar(lb=0, vtype=grb.GRB.CONTINUOUS, name='d32')
x1 = m.addVar(lb=0, vtype=grb.GRB.CONTINUOUS, name='x1')
x2 = m.addVar(lb=0, vtype=grb.GRB.CONTINUOUS, name='x2')
x3 = m.addVar(lb=0, vtype=grb.GRB.CONTINUOUS, name='x3')

# constraints
m.addConstr(2 * x1 + x2 + x3 == 11)
m.addConstr(x1 - x2 + d11 - d12 == 0)
m.addConstr(x1 + 2 * x2 + d21 - d22 == 10)
m.addConstr(8 * x1 + 10 * x2 + d31 - d32 == 56)

# objectives
m.setObjectiveN(d12, index=0, priority=9, name='obj1')
m.setObjectiveN(d21 + d22, index=1, priority=6, name='obj2')
m.setObjectiveN(d31, index=2, priority=3, name='obj3')

m.optimize()

for v in m.getVars():
    print(v.varName, '=', v.x)

# 查看目标函数的值
for i in range(3):
    m.setParam(grb.GRB.Param.ObjNumber, i)
    print('Obj {} = {}'.format(i+1, m.ObjNVal))




