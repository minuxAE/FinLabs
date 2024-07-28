"""
z = min(x, y, 3)进行约束线性化
"""
import gurobipy as grb

def lin_min_1():
    m = grb.Model()
    x = m.addVar(name='x')