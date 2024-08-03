"""
对偶问题

原问题和对偶问题可以看作一个问题的两个视角

P: 在一定资源下如何安排生产使得利润最大
Q: 如何购买这些生产资源使得花钱最少

Dual问题的几个基本性质
1. 可逆性. 对偶问题的对偶是原问题
2. 弱对偶性. 可以得到规划问题的上界或者下界
3. 无界性. 若原问题（对偶问题）的解无界, 则其对偶问题（原问题）
4. 可行解为最优解的性质. 当CX*=b^TY*时, X*和Y*是原问题和对偶问题的最优解
5. 对偶定理. 如果一个问题有最优解, 则另一个问题必有最优解, 而且它们的最优目标函数值相等（Z=D）
6. 互补松弛定理, 在互为对偶的两个问题中, 如果一个问题的某个变量取正数, 则另一个问题相应的约束必然取等式, 若一个问题的某个约束条件取不等式, 则另一个问题相应的变量为0
"""

"""
整数规划

常用方法有分支定界法和割平面法

在LP的基础上, 通过增加附加约束条件, 使得整数最优解为LP的一个极点

求解IP问题

max Z = 3x1 + 2x2

2x1 + 3x2 <= 12
4x1 + 2x2 <= 18
x1, x2 >= 0, integer
"""
import gurobipy as grb

model = grb.Model()

# 整数变量
x1 = model.addVar(vtype=grb.GRB.INTEGER, name='x1')
x2 = model.addVar(vtype=grb.GRB.INTEGER, name='x2')

# 添加约束
model.addConstr(2 * x1 + 3 * x2 <= 14)
model.addConstr(4 * x1 + 2 * x2 <= 18)
model.addConstr(x1 >= 0)
model.addConstr(x2 >= 0)

# 定义目标函数
model.setObjective(3 * x1 + 2 * x2, sense=grb.GRB.MAXIMIZE)

# 求解
model.optimize()
print('Objective function: ', model.objVal)

for v in model.getVars():
    print('Param', v.varName, '=', v.x)


"""
分支定界法就是将B的可行解空间分成子空间再求最大值的方法
逐步减少上界和下界
"""

"""
割平面法

割平面法通过增加切割超平面切割掉松弛问题的非整数解部分, 但是并没有对问题进行分支
"""


