import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

"""
绘制动态图, 用于模拟系统仿真
"""

class Car():
    def __init__(self, marker):
        self.x = 1
        self.y = 1
        self.marker = marker

    def move(self):
        # 随机选择方向, 移动后并更新目标
        self.x = self.x + np.random.randint(low=-1, high=2, size=1)[0]
        self.y = self.y + np.random.randint(low=-1, high=2, size=1)[0]

        # boundary check
        self.x = self.x if self.x > 0 else 0
        self.x = self.x if self.x < 10 else 10
        self.y = self.y if self.y > 0 else 0
        self.y = self.y if self.y < 10 else 10

cars = [Car(marker='o'), Car(marker='^'), Car(marker='*')]

fig = plt.figure()

i = list(range(1, 1000)) # 模拟1000个时间节点

def update(i):
    plt.clf() # 清空图层

    for c in cars:
        c.move()
        x = c.x
        y = c.y
        marker = c.marker
        plt.xlim(0, 10)
        plt.ylim(0, 10)
        plt.scatter(x, y, marker=marker)
    return

ani = animation.FuncAnimation(fig, update)
plt.show()



