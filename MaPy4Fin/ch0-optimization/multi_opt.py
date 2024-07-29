"""
Gurobi多目标优化

Model.setObjectiveN(expr, index, priority, weight, abstol, reltol, name)

expr: 目标函数的表达式 x + 2y + 3z
index: 目标函数对应的序号
priority: 优先级, 整数, 数值越大表示目标优先级越高
weight: 权重, 在合成多目标解法中使用该参数
abstol: 允许的目标函数值最大的降低量, 即当前迭代的值相比最优值的可接受劣化程度
reltol: abstol的百分数表示, 如reltol=1%表示可以接受的劣化程度为1%
name: 目标函数名称
"""

"""
例如, 需要优化如下两个目标:
obj1 = x + 2y, weight = 3
obj2 = x - 3y, weight = 0.5

可以使用加权合成方法进行处理
"""


import gurobipy as grb

# 合成方法处理多目标问题
def foo1():
    model = grb.Model()

    x = model.addVar(name = 'x')
    y = model.addVar(name = 'y')

    model.setObjectiveN(x + 2 * y, index=0, weight=3, name='obj1')
    model.setObjectiveN(x - 3 * y, index=1, weight=0.5, name='obj2')
    model.optimize()

# 层次优化, 设定优先级
def foo2():
    model = grb.Model()

    x = model.addVar(name = 'x')
    y = model.addVar(name = 'y')

    # 第一个目标
    model.setObjectiveN(x + 2 * y, index=0, priority=20, name='obj1')
    # 第二个目标
    model.setObjectiveN(x - 3 * y, index=1, priority=1, name='obj2')

    model.optimize()

# 合并+层次的混合方式
def foo3():
    model = grb.Model()

    x = model.addVar(name = 'x')
    y = model.addVar(name = 'y')

    # 第一个目标
    model.setObjectiveN(x + 2 * y, index=0, weight=3, priority=20, name='obj1')
    # 第二个目标
    model.setObjectiveN(x - 3 * y, index=1, weight=0.5, priority=1, name='obj2')

    model.optimize()

    for i in range(model.NumObj):
        model.setParam(grb.GRB.Param.ObjNumber, i)

        print('The {}th objective is {}'.format(i+1, model.ObjNVal))


if __name__ == '__main__':
    foo3()

