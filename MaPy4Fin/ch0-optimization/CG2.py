"""
列生成方法

求解限制性主问题 RMP
"""
import gurobipy as grb

def RMP2():
    model = grb.Model()

    # 定义变量
    z1 = model.addVar(vtype=grb.GRB.CONTINUOUS, name='z1')
    z2 = model.addVar(vtype=grb.GRB.CONTINUOUS, name='z2')
    z3 = model.addVar(vtype=grb.GRB.CONTINUOUS, name='z3')
    z4 = model.addVar(vtype=grb.GRB.CONTINUOUS, name='z4')
    z5 = model.addVar(vtype=grb.GRB.CONTINUOUS, name='z5')

    # 添加约束
    model.addConstr(6 * z1 + 2 * z5 >= 25)
    model.addConstr(2 * z2 + 2 * z5 >= 30)
    model.addConstr(2 * z3 >= 14)
    model.addConstr(z4 >= 8)

    model.addConstr(z1 >= 0)
    model.addConstr(z2 >= 0)
    model.addConstr(z3 >= 0)
    model.addConstr(z4 >= 0)
    model.addConstr(z5 >= 0)

    # 目标函数
    model.setObjective(z1 + z2 + z3 + z4 + z5, grb.GRB.MINIMIZE)
    model.optimize()

    for v in model.getVars():
        print(v.varName, '=', v.x)

    
    # 获取约束的对偶变量的值
    dual = model.getAttr(grb.GRB.Attr.Pi, model.getConstrs())

    print(dual) # [0, 0.5, 0.5, 1]


def SUB2():
    model = grb.Model()

    # 添加变量
    a1 = model.addVar(vtype=grb.GRB.INTEGER, name='a1')
    a2 = model.addVar(vtype=grb.GRB.INTEGER, name='a2')
    a3 = model.addVar(vtype=grb.GRB.INTEGER, name='a3')
    a4 = model.addVar(vtype=grb.GRB.INTEGER, name='a4')

    # 添加约束
    model.addConstr(3 * a1 + 7 * a2 + 9 * a3 + 16 * a4 <= 20)

    # 设定目标函数
    model.setObjective(1 - 0 * a1 - 0.5 * a2 - 0.5 * a3 - a4, grb.GRB.MINIMIZE)
    model.optimize()

    print('Objective function is: {}'.format(model.objVal))

    for v in model.getVars():
        print(v.varName, '=', v.x)

    # reduced cost = 0

if __name__ == '__main__':
    SUB2()
    # RMP2()