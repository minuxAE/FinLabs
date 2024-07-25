import gurobipy as grb

# 设定两种商品
commdities = ['Pencils', 'Pens']
nodes = ['Detroit', 'Denver', 'Boston', 'New York', 'Seattle']

# 网络中每条弧的容量
arcs, capacity = grb.multidict({
    ('Detroit', 'Boston'): 100,
    ('Detroit', 'New York'): 80,
    ('Detroit', 'Seattle'): 120,
    ('Denver', 'Boston'): 120,
    ('Denver', 'New York'): 120,
    ('Denver', 'Seattle'): 120
})

# 商品在不同弧上的运输成本
cost = {
    ('Pencils', 'Detroit', 'Boston'): 10,
    ('Pencils', 'Detroit', 'New York'): 20,
    ('Pencils', 'Detroit', 'Seattle'): 60,
    ('Pencils', 'Denver', 'Boston'): 40,
    ('Pencils', 'Denver', 'New York'): 40,
    ('Pencils', 'Denver', 'Seattle'): 30,
    ('Pens', 'Detroit', 'Boston'): 20,
    ('Pens', 'Detroit', 'New York'): 20,
    ('Pens', 'Detroit', 'Seattle'): 80,
    ('Pens', 'Denver', 'Boston'): 60,
    ('Pens', 'Denver', 'New York'): 70,
    ('Pens', 'Denver', 'Seattle'): 30,
}

# 商品在不同节点的需求量
inflow = {
    ('Pencils', 'Detroit'): 50,
    ('Pencils', 'Denver'): 60,
    ('Pencils', 'Boston'): -50,
    ('Pencils', 'New York'): -50,
    ('Pencils', 'Seattle'): -10,
    ('Pens', 'Detroit'): 60,
    ('Pens', 'Denver'): 40,
    ('Pens', 'Boston'): -40,
    ('Pens', 'New York'): -30,
    ('Pens', 'Seattle'): -30
}

m = grb.Model('netflow')
flow = m.addVars(commdities, arcs, obj=cost, name='flow')

# 添加容量约束
m.addConstrs((flow.sum('*', i, j) <= capacity[i, j] for i, j in arcs), 'caps')

# 流平衡约束
m.addConstrs((flow.sum(h, '*', j) + inflow[h, j] == flow.sum(h, j, '*') for h in commdities for j in nodes), 'node')

m.optimize()

if m.status == grb.GRB.Status.OPTIMAL:
    solution = m.getAttr('x', flow)
    for h in commdities:
        print('Optimal flows for :', h)
        for i, j in arcs:
            if solution[h, i, j] > 0:
                print('{} -> {}: {}'.format(i, j, solution[h, i, j]))
