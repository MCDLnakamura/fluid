"""
それぞれのモデルの混合比の領域平均の鉛直プロファイルをプロット
rain=0を除いたよ
"""

from netCDF4 import Dataset
import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt
import os
#matplotlib.colors.cnames
fig = plt.figure()
fig, ax = plt.subplots()

#モデルの指定
mp="24"
path=mp+"/wrfout_d03_2017-07-04_12:00:00"
is_file = os.path.isfile(path)
if is_file:#パスにファイルが無ければ処理を飛ばす
    nc = Dataset(path, "r")
    nc_var=nc.variables.keys()

    time=6*22
    print(time)

    #時間の取得
    tmp = ""
    times = nc.variables["Times"]
    for i in times[time]:
        tmp += i.decode()

    #wrf.pythonを用いてz座標ごとの高度を得る
    from wrf import *
    z = getvar(nc, "z", units="m")
    z.to_masked_array()
    z=np.mean(z,axis=(1,2))[:]*0.001 #(kmにするために0.001をかける)
    print("z",z,)

    ###rainが(13)番目の層において0の地点は除外するようにする
    ##forとifで2重に囲んで探索する形にする 
    ##QVAPOR(Time, bottom_top, south_north, west_east)であることを考えて、
    z_cut=13 #番目(0インデックスだよ)
    qr=nc.variables['QRAIN']
    qrz=[]
    idx_time,idx_z,idx_y,idx_x=qr.shape

else:#パスが通ってない場合には処理を終了する
    print("ファイルなし")
    exit()#プログラム終了



p_k = ('QCLOUD','QRAIN','QICE','QSNOW','QGRAUP','QHAIL')
for mp_i in p_k:
    if mp_i in nc_var:
        q=nc.variables[mp_i]
        print(q)
        qz=[]
        for k in range(idx_z):
            qh=[]
            for i in range(idx_y):
                for j in range(idx_x):
                    if qr[time,z_cut,i,j]>0:
                        qh.append(q[time,k,i,j])
            qz.append(np.mean(qh)*1000)
        print(qz)
        ax.plot(qz,z, label="qc")

#軸の最大値、最小値
ax.set_xlim(-0.005, 0.5)
ax.set_ylim(0, 18)

#グラフタイトル
plt.title("Averaged q-profile over d03 but rain=0("+mp+")")

#グラフの軸
ax.set_xlabel('Mixing ratio (g/kg)')
ax.set_ylabel('Height(km)')

#グラフの凡例
ax.legend()


fig.savefig(mp+"_vq_"+tmp+"_rain0.png")
print('fig.saved')
