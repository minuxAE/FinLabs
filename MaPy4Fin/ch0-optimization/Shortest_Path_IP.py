import gurobipy as grb

# 定义边
edge = {
    ('V1', 'A'): 0,
    ('A', 'B1'): 10,
    ('A', 'B2'): 20,
    ('B1', 'C1'): 30,
    ('B1', 'C2'): 10,
    ('B2', 'C1'): 5,
    ('B2', 'C2'): 20,
    ('C1', 'D'): 20,
    ('C2', 'D'): 10,
    ('D', 'V2'): 0
}

# 创建边和边长度的常量
links, length = grb.multidict(edge)

# 创建模型
m = grb.Model()
x = m.addVars(links, obj=length, name='flow')

# 添加约束
for i in ['A', 'B1', 'B2', 'C1', 'C2', 'D']:
    if i=='A':
        delta = 1
    elif i=='D':
        delta = -1
    else:
        delta = 0
    name = 'C_{}'.format(i)

    m.addConstr(x.sum(i, '*') - x.sum('*', i) == delta, name=name)

m.optimize()

for i, j in links:
    if x[i, j].x > 0:
        print('{} -> {} : {}'.format(i, j, edge[i, j]))