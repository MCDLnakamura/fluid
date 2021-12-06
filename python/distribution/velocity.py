"""
落下速度と粒径の関係の線を引く
1回限りの図（特にこの後使う予定はない）
"""
import numpy as np
from matplotlib import ticker
import matplotlib.pyplot as plt
fig = plt.figure()
fig, ax = plt.subplots()

d = np.linspace( 0, 0.01, 1000)



#軸の最大値、最小値
#ax.set_xlim(-0.005, 0.5)
#ax.set_ylim(0, 18)
"""
v=avtg*d**bvtg*np.exp(-d*gamma_x)
v=avtg*d**bvtg
"""

#graupel
v_g=330*d**0.8
ax.plot(d,v_g, label="graupel")
#den=500 

#hail
v_h=285.0*d**0.8
ax.plot(d,v_h, label="hail")
#den=700 or 912

#snow
v_s=11.72*d**0.41
ax.plot(d,v_s, label="snow")
#den=100

#rain
v_r=841.9*d**0.8
ax.plot(d,v_r, label="rain")
#den=1000

#グラフタイトル
plt.title("velocity-diameter relationship")


# x軸の目盛設定
xaxis_ = ax.xaxis
new_xticks = [0, 0.002, 0.004,0.006,0.008,0.01]  # 点がない場所でも良い
xaxis_.set_major_locator(ticker.FixedLocator(new_xticks))
ax.set_xticklabels([0,2,4,6,8,10])

#グラフの軸
ax.set_xlabel('diameter(mm)')
ax.set_ylabel('velocity(m/s)')

#グラフの凡例
ax.legend()

fig.savefig("v_d_realation.png")
print('fig.saved')
