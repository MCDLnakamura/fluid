"""
それぞれのモデルの数密度の領域平均の鉛直プロファイルをプロット
Hong et al 2010に習って雲域を0.01g/kgとして特定の時間について
この範囲で調べる
"""
from netCDF4 import Dataset
import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt
fig = plt.figure()
fig, ax = plt.subplots()



time=6*22
print("time")
print(time)

#wrf.pythonを用いてz座標ごとの高度を得る
from wrf import *
nc = Dataset("WDM6_h/wrfout_d03_2017-07-04_12:00:00", "r")
nc_var=nc.variables.keys()
z = getvar(nc, "z", units="m")
z.to_masked_array()
z=np.mean(z,axis=(1,2))[:]*0.001
print("z",z,)

"""
#1モデル目(1モーメント)
qnr_z_1=[]
for i in range(40):
    qnr_z_1.append(300e6)
print("qnr_z_1")
print(qnr_z_1)
"""

#2モデル目以降
mp_k = ("WDM6","WDM6_h","WDM7")
for mp in mp_k:
    print(mp)
    from netCDF4 import Dataset
    nc = Dataset(mp+"/wrfout_d03_2017-07-04_12:00:00", "r")
    nc_var=nc.variables.keys()
    if 'QNRAIN' in nc_var:
        qnr=nc.variables['QNRAIN']
        #print(b_qnr)
        idx_time,idx_z,idx_y,idx_x=qnr.shape
        qnr_z=[]
        for k in range(idx_z):
                qnr_h=[]
                for i in range(idx_y):
                    for j in range(idx_x):
                        if qnr[time,k,i,j]>0.00001:
                            qnr_h.append(qnr[time,k,i,j])
                qnr_z.append(np.mean(qnr_h))
        print(qnr_z)
        ax.plot(qnr_z,z,label="cloud"+mp)
        del qnr_z, idx_time, idx_z, idx_y, idx_x #念のため変数の中身を削除する

#軸の最大値、最小値
#ax.set_xlim(0, max(np.max(qnc_z_1), np.max(qnc_z_2), np.max(qnc_z_3), np.max(qnc_z_4)))
ax.set_ylim(0, 15)

#グラフタイトル
plt.title('Averaged number concentration over 0.01g/kg')

#グラフの軸
ax.set_xlabel('number concentration ($\mathrm{m^{-3}}$)')
ax.set_ylabel('Height(km)')

#グラフの凡例
ax.legend()


fig.savefig("number_qnr_ov.png", bbox_inches='tight', pad_inches=0.1)
print('fig.saved')

