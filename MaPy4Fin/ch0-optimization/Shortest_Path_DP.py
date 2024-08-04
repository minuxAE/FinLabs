"""
使用动态规划方法求解最短路径问题
"""
import pandas as pd
import numpy as np

# 存储节点距离
# A->B 的距离
df1 = pd.DataFrame(np.array([[10, 20]]), index=["A"], columns=['B1', 'B2'])
# B->C 的距离
df2 = pd.DataFrame(np.array([[30, 10], [5, 20]]), index=['B1', 'B2'], columns=['C1', 'C2'])
# C->D 的距离
df3 = pd.DataFrame(np.array([[20], [10]]), index=['C1', 'C2'], columns=['D'])


def dp(df_from, df_to):
    from_node = df_to.index
    f = pd.Series()
    g = []

    for j in from_node:
        m1 = df_to.loc[j]
        m2 = m1 + df_from
        m3 = m2.sort_values()
        f[j] = m3[0]
        g.append(m3.index[0])

    dc = pd.DataFrame()
    dc['v'] = f.values
    dc['n'] = g
    dc.index = f.index
    cv.append(dc)

    if len(start) > 0:
        df = start.pop()
        t = dp(dc['v'], df)
    else:
        return dc


# 主函数
start = [df1] # 初始状态
cv = [] # 存储路径
t1 = df3['D'] # 初始状态
h1 = dp(df3['D'], df2)

# 输出路径
for m in range(len(cv)):
    xc = cv.pop()
    x1 = xc.sort_values(by='v')
    print(x1['n'].values[0], end='->')
