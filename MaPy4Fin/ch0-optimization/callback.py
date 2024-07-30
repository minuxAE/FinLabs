"""
callback函数主要作用是为了获取程序运行过程中的一些中间信息, 或者在程序运行过程中
动态修改程序的运行状态

如用户可以在求解过程中加入终止优化、添加约束条件、嵌入算法等

def function_name(model, where):
    print('...')

model: gurobi.Model类
where: 回调函数的出发点

if where==grb.GRB.Callback.MULTIOBJ: # where
    print(model.cbGet(grb.GRB.Callback.MULTIOBJ_OBJCNT)) # what

where和what一般配合使用, 如果where=MIP, what只能获取MIP相关信息
"""

import gurobipy as grb

def foo1():
    model = grb.Model()
    # 查询求解过程中的信息
    def my_callback(model, where):
        if where == grb.GRB.Callback.SIMPLEX:
            print(model.cbGet(grb.GRB.Callback.SPX_OBJVAL))

    model.optimize()

def foo2():
    model = grb.Model()
    # 查询变量在当前节点的松弛解
    def my_callback(model, where):
        if where == grb.GRB.Callback.MIPNODE and model.cbGet(grb.GRB.Callback.MIPNODE_STATUS) == grb.GRB.OPTIMAL:
            print(model.cbGetNodeRel(model._vars))

    model._vars = model.getVars()
    model.optimize(my_callback)

def foo3():
    model = grb.Model()
    # 在MIP问题中查询变量在新可行解中的值
    def my_callback(model, where):
        if where == grb.GRB.Callback.MIPSOL:
            print(model.cbGetSolution(model._vars))

    model._vars = model.getVars()
    model.optimize(my_callback)


def foo4():
    model = grb.Model()
    # 在求解MIP问题再节点处添加割平面
    def my_callback(model, where):
        if where == grb.GRB.Callback.MIPNODE:
            status = model.cbGet(grb.GRB.Callback.MIPNODE_STATUS)
            if status == grb.GRB.OPTIMAL:
                rel = model.cbGetNodeRel([model._vars[0], model._vars[1]])
                if rel[0] + rel[1] > 1.1:
                    model.cbCut(model._vars[0] + model._vars[1] <= 1)

    model._vars = model.getVars()
    model.Params.PreCrush = 1
    model.optimize(my_callback)
            


if __name__ == '__main__':
    foo4()