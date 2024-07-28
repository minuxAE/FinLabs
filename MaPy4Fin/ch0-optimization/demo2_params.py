"""
Gurobi修改参数的方法
1.setParam
2.参数字符串
3.修改类的属性
"""
import gurobipy as grb

def foo1():
    model = grb.Model()
    # 方法1
    model.setParam('TimeLimit', 600)

    # 方法2
    model.setParam(grb.GRB.param.TimeLimit, 600)

    # 方法3
    model.Params.TimeLimit = 600


def foo2():
    model_file = 'ch0-optimization/models/tuple_vars.lp'
    m = grb.read(model_file)
    
    # 参数设定, 设定优化器的求解时间为2秒
    m.Params.timeLimit = 2

    # 复制模型
    bModel = m.copy()
    bModel.optimize()

    # 修改模型参数比较不同参数下的结果
    for i in range(1, 4):
        m.reset()
        # MIP求解器在找到新的可行解与证明当前可行解是最优之间进行平衡
        # 值为1表示快速找到可行解
        # 值为2表示侧重找到最优解
        # 值为3表示专注于边界
        m.Params.MIPFocus = i 
        m.optimize()

        if bModel.MIPGap > m.MIPGap:
            bModel, m = m, bModel

    del m
    bModel.Params.timeLimit = 'default'
    bModel.optimize()

    print('Solved with MIPFocus: {}'.format(bModel.Params.MIPFocus))


def foo3():
    # 自动调优
    model_file = 'ch0-optimization/models/tuple_vars.lp'
    model = grb.read(model_file)

    # 设置最优参数组合为1
    model.Params.tuneResults = 1

    # 自动调参
    model.tune()

    if model.tuneResultCount > 0:
        # 获取最优参数组合
        model.getTuneResult(0)
        # 调参后文件保存
        model.write('ch0-optimization/models/tun.prm')
        model.optimize() # 使用获取的最优参数组合再次求解模型


if __name__ == '__main__':
    foo3()
