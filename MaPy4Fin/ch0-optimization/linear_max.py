"""
查看和修改属性

查看属性
getAttr(attrname, objs)
attrname是属性名称, objs是列表或者字典对象用来存储查询的值

setAttr(attrname, newvalue)

线性化技巧

将非线性约束转换为线性约束（广义约束）

添加广义约束的两种方法：
1. model类的方法 add_XXX
2. model.addConstr方法
"""

import gurobipy as grb

# 使用大M法线性化约束 max(x, y, 3)
def max_lin_1():
    m = grb.Model()
    x = m.addVar(name='x')
    y = m.addVar(name='y')
    z = m.addVar(name='z')
    u1 = m.addVar(vtype='B', name='u1')
    u2 = m.addVar(vtype='B', name='u2')
    u3 = m.addVar(vtype='B', name='u3')

    M = 10000 # 大M法的超参数

    # 添加约束
    m.addConstr(x <= z - M * (1-u1), name='c1')
    m.addConstr(y <= z - M * (1-u2), name='c2')
    m.addConstr(3 <= z - M * (1-u3), name='c3')
    m.addConstr(x == 4, name = 'c4')
    m.addConstr(y == 5, name='c5')
    m.addConstr(u1 + u2 + u3 >= 1, name='c6')
    m.addConstr(x <= z, name='c7')
    m.addConstr(y <= z, name='c8')
    m.addConstr(3 <= z, name='c8')

    # 定义目标函数并求解
    m.setObjective(z)
    m.optimize()
    print('z=', z.X)


# 使用gurobi内置接口的方法
def max_lin_2():
    m = grb.Model()

    x = m.addVar(name='x')
    y = m.addVar(name='y')
    z = m.addVar(name='z')

    m.addConstr(x==4, name='c4')
    m.addConstr(y==5, name='c5')
    m.addConstr(z == grb.max_(x, y, 3))
    m.setObjective(z)
    m.optimize()
    print('max value is: z=', z.X)



if __name__ == '__main__':
    max_lin_2()
    # max_lin_1()





