"""
列生成方法

求解限制性主问题 RMP
"""
import gurobipy as grb

def RMP1():
    model = grb.Model()

    # 定义变量
    z1 = model.addVar(vtype=grb.GRB.CONTINUOUS, name='z1')
    z2 = model.addVar(vtype=grb.GRB.CONTINUOUS, name='z2')
    z3 = model.addVar(vtype=grb.GRB.CONTINUOUS, name='z3')
    z4 = model.addVar(vtype=grb.GRB.CONTINUOUS, name='z4')

    # 添加约束
    model.addConstr(6 * z1 >= 25)
    model.addConstr(2 * z2 >= 30)
    model.addConstr(2 * z3 >= 14)
    model.addConstr(z4 >= 8)

    model.addConstr(z1 >= 0)
    model.addConstr(z2 >= 0)
    model.addConstr(z3 >= 0)
    model.addConstr(z4 >= 0)

    # 目标函数
    model.setObjective(z1 + z2 + z3 + z4, grb.GRB.MINIMIZE)
    model.optimize()

    for v in model.getVars():
        print(v.varName, '=', v.x)

    
    # 获取约束的对偶变量的值
    dual = model.getAttr(grb.GRB.Attr.Pi, model.getConstrs())

    print(dual) # [0.1667, 0.5, 0.5, 1.0]


"""
将对偶变量带入子问题
reducedcost = 1-Pi*a_n

min 1-0.1667a1 - 0.5a2 + 0.5a3 - a4
s.t. 3a1 + 7a2 + 9a3 + 16a4 <= 20
a1, a2, a3, a4 integer
"""

def SUB1():
    model = grb.Model()

    # 添加变量
    a1 = model.addVar(vtype=grb.GRB.INTEGER, name='a1')
    a2 = model.addVar(vtype=grb.GRB.INTEGER, name='a2')
    a3 = model.addVar(vtype=grb.GRB.INTEGER, name='a3')
    a4 = model.addVar(vtype=grb.GRB.INTEGER, name='a4')

    # 添加约束
    model.addConstr(3 * a1 + 7 * a2 + 9 * a3 + 16 * a4 <= 20)

    # 设定目标函数
    model.setObjective(1 - 0.166666 * a1 - 0.5 * a2 - 0.5 * a3 - a4, grb.GRB.MINIMIZE)
    model.optimize()

    print('Objective function is: {}'.format(model.objVal))

    for v in model.getVars():
        print(v.varName, '=', v.x)
    
if __name__ == '__main__':
    SUB1()
    # RMP1()