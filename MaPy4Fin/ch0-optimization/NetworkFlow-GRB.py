import gurobipy as grb

# 定义网络
flow = {(0, 1): 99999, (1, 2): 70, (1, 3): 100, (1, 4): 90, (2, 6): 80,
        (3, 4): 40, (3, 5): 70, (4, 5): 40, (4, 6): 100, (5, 6): 90, (6, 7): 99999}

arch, maxflow = grb.multidict(flow)
m = grb.Model('maxflow')
X = m.addVars(arch, name='X')

# 添加约束
for i, j in arch:
    # 流量约束
    m.addConstr(X[i, j] <= maxflow[i, j])
    if i == 0 or j == 7:
        continue
    else:
        m.addConstr(X.sum(i, '*') == X.sum('*', i))

# 添加目标函数
m.setObjective(X.sum(1, '*'), sense=grb.GRB.MAXIMIZE)
m.optimize()

print('Objective Value: ', m.objVal)

for i, j in arch:
    print('{} -> {}: {}'.format(i, j, X[i, j].x))