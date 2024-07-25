from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm # 颜色配置
import numpy as np

# 生成画布
fig = plt.figure()
ax = fig.add_subplot(projection='3d') # 设定为3d

# 生成数据
x = np.arange(-5, 5, 0.25)
y = np.arange(-5, 5, 0.25)
x, y = np.meshgrid(x, y)

z = np.sin(np.sqrt(x ** 2 + y ** 2))

# plot_surface
surf = ax.plot_surface(x, y, z, cmap = cm.coolwarm)
plt.show()

