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

def foo5():
    model = grb.Model()
    # 求解MIP问题的过程中, 在节点添加Lazy Cut
    # 当MIP模型的完整约束集太大而无法显式表示时, 通常使用惰性约束.
    # 通过只包含在分支割平面搜索过程中不满足条件的约束, 有时也可以在只添加完整约束集的一小部分时找到最优解

    def my_callback(model, where):
        if where == grb.GRB.Callback.MIPSOL:
            sol = model.cbGetSolution([model._vars[0], model._vars[1]])
            if sol[0] + sol[1] > 1.1:
                model.cbLazy(model._vars[0] + model._vars[1] <= 1)

    model._vars = model.getVars()
    model.Params.lazyConstraints = 1
    model.optimize(my_callback)

def foo6():
    model = grb.Model()
    # 从当前节点导入解
    def my_callback(model, where, newsolution):
        if where == grb.GRB.Callback.MIPNODE: 
            model.cbSetSolution(vars, newsolution)

    model.optimize(my_callback)


import time
def foo7():
    model = grb.Model()
    # 在非分层的多目标优化问题中, 中断其优化过程
    # 会先
    def my_callback(model, where):
        if where == grb.GRB.Callback.MULTIOBJ:
            # 获取当前目标函数值
            model._objcnt = model.cbGet(grb.GRB.Callback.MULTIOBJ_OBJCNT)
            # 重置开始计时时间
            model._starttime = time.time()
        # 判断是否退出搜索
        # elif time.time() - model._starttime > BIG or solution is good_enough:
        #   model.cbStopOneMultiObj(model._objcnt)
    
    model._objcnt = 0
    model._starttime = time.time()
    model.optimize(my_callback)
    



if __name__ == '__main__':
    foo5()