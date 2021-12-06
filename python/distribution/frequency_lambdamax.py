"""
粒径分布をlambda_maxを仮定して描く
"""

import numpy as np
from matplotlib import ticker
import matplotlib.pyplot as plt
fig = plt.figure()
fig, ax = plt.subplots()

d = np.linspace( 0, 0.005, 1000)#長さはm単位

"""
n_x=n0_x*np.exp(-1*lambda_x_max*d_x) #1モーメントの場合
"""

#円周率
pi=3.141592

# p_k = ('QCLOUD','QRAIN','QICE','QSNOW','QGRAUP','QHAIL')
p_k = ('QRAIN','QSNOW','QGRAUP','QHAIL')
# LAMBDAmax=[8.e4,1.e5,6.e4,2.e4]
LAMBDAmax=[2238,1.e5,6.e4,2.e4]
n0=[8.e6,2.e6,4.e6,4.e4]
i=0
for mp_i in p_k:
    print(i)
    LAMBDA=LAMBDAmax[i]
    n0_x=n0[i]
    n=n0_x*np.exp(-1*LAMBDA*d)
    ax.plot(d,n, label=mp_i)
    i=i+1


#グラフタイトル
plt.title("number distribution(lambda_max)")

plt.yscale('log')

#軸の最大値、最小値
ax.set_xlim(0, 0.005)
ax.set_ylim(1, 1.e7)

# x軸の目盛設定(mとmmの換算)
xaxis_ = ax.xaxis
new_xticks = [0, 0.001, 0.002,0.003,0.004,0.005]  # 点がない場所でも良い
xaxis_.set_major_locator(ticker.FixedLocator(new_xticks))
ax.set_xticklabels([0,1,2,3,4,5])

#グラフの軸
ax.set_xlabel('diameter(mm)')
ax.set_ylabel('number concentration(m^-3)')

#グラフの凡例
ax.legend()

fig.savefig("number distribution.png")
print('fig.saved')
