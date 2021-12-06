"""
それぞれのモデルの混合比の領域平均の鉛直プロファイルをプロット
層状域を取り出す

11/26x軸の最大値を1.05に固定した
文字列のリストを作ってそれをforで回す方法に変更
下に変更前のモノを仮置きしている
"""

from netCDF4 import Dataset
import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt
import os
#matplotlib.colors.cnames
fig = plt.figure()
fig, ax = plt.subplots()

#モデル、時間、パスの指定
mp="WSM6_h"
path="/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/late_run_041200/"+mp+"/"
file="wrfout_d03_2017-07-04_12:00:00"
time=6*22
is_file = os.path.isfile(path+file)

cors=np.load(path+"cors"+str(time)+".npy") #対流かどうかを読み込める
#life_up=np.load(path+"life_up"+str(time)+".npy") #上昇流帯を読み込む
#life_dw=np.load(path+"life_dw"+str(time)+".npy") #下降流帯を読み込む

#print("up",np.count_nonzero(life_up==1))
#print("dw",np.count_nonzero(life_dw==1))


if is_file:#パスにファイルが無ければ処理を飛ばす
    nc = Dataset(path+file, "r")
    nc_var=nc.variables.keys()
    print(time)

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
    print(mp_i)
    if mp_i in nc_var:
        print(mp_i)
        q=nc.variables[mp_i]
        print(q)
        qz=[]
        for k in range(idx_z):
            qh=[]
            for i in range(idx_y):
                for j in range(idx_x):
                    if cors[z_cut,i,j]==3:
                        qh.append(q[time,k,i,j])
            qz.append(np.mean(qh)*1000)
        print(qz)
        ax.plot(qz,z, label=mp_i)

#軸の最大値、最小値
ax.set_xlim(-0.005, 1.05)
ax.set_ylim(0, 18)

#グラフタイトル
plt.title("Averaged q-profile ("+mp+") stratiform")

#グラフの軸
ax.set_xlabel('Mixing ratio (g/kg)')
ax.set_ylabel('Height(km)')

#グラフの凡例
ax.legend()

fig.savefig(mp+"_vq_"+str(time)+"_staratiform.png")
print('fig.saved')

#end------------------------------------------------------------------------------------------------------------------

"""
sha=qr.shape
if 'QCLOUD' in nc_var:
    print('QCLOUD')
    qc=nc.variables['QCLOUD']
    print(qc)
    qcz=[]
    for k in range(sha[1]):
        qch=[]
        for i in range(sha[2]):
            for j in range(sha[3]):
                if cors[z_cut,i,j]==1 or cors[z_cut,i,j]==2:
                    qch.append(qc[time,k,i,j])
        qcz.append(np.mean(qch))
    print(qcz)
    qc_lis=[]
    for n in qcz:
        qc_lis.append(n*1000)
    ax.plot(qc_lis,z, label="qc")

if 'QRAIN' in nc_var:
    print('QRAIN')
    qr=nc.variables['QRAIN']
    qrz=[]
    for k in range(sha[1]):
        qrh=[]
        for i in range(sha[2]):
            for j in range(sha[3]):
                if cors[z_cut,i,j]==1 or cors[z_cut,i,j]==2:
                    qrh.append(qr[time,k,i,j])
        qrz.append(np.mean(qrh))
    print(qrz)
    qr_lis=[]
    for n in qrz:
        qr_lis.append(n*1000)
    ax.plot(qr_lis,z, label="qr")

if 'QICE' in nc_var:
    print('QICE')
    qi=nc.variables['QICE']
    qiz=[]
    for k in range(sha[1]):
        qih=[]
        for i in range(sha[2]):
            for j in range(sha[3]):
                if cors[z_cut,i,j]==1 or cors[z_cut,i,j]==2:
                    qih.append(qi[time,k,i,j])
        qiz.append(np.mean(qih))
    print(qiz)
    qi_lis=[]
    for n in qiz:
        qi_lis.append(n*1000)
    ax.plot(qi_lis,z, label="qi")

if 'QSNOW' in nc_var:
    print('QSNOW')
    qs=nc.variables['QSNOW']
    qsz=[]
    for k in range(sha[1]):
        qsh=[]
        for i in range(sha[2]):
            for j in range(sha[3]):
                if cors[z_cut,i,j]==1 or cors[z_cut,i,j]==2:
                    qsh.append(qs[time,k,i,j])
        qsz.append(np.mean(qsh))
    print(qsz)    
    qs_lis=[]
    for n in qsz:
        qs_lis.append(n*1000)
    ax.plot(qs_lis,z, label="qs")

if 'QGRAUP' in nc_var:
    print('QGRAUP')
    qg=nc.variables['QGRAUP']
    qgz=[]
    for k in range(sha[1]):
        qgh=[]
        for i in range(sha[2]):
            for j in range(sha[3]):
                if cors[z_cut,i,j]==1 or cors[z_cut,i,j]==2:
                    qgh.append(qg[time,k,i,j])
        qgz.append(np.mean(qgh))
    print(qgz)
    qg_lis=[]
    for n in qgz:
        qg_lis.append(n*1000)
    ax.plot(qg_lis,z, label="qg")

if 'QHAIL' in nc_var:
    print('QHAIL')
    qh=nc.variables['QHAIL']
    qhz=[]
    for k in range(sha[1]):
        qhh=[]
        for i in range(sha[2]):
            for j in range(sha[3]):
                if cors[z_cut,i,j]==1 or cors[z_cut,i,j]==2:
                    qhh.append(qh[time,k,i,j])
        qhz.append(np.mean(qhh))
    print(qhz)
    qh_lis=[]
    for n in qhz:
        qh_lis.append(n*1000)
    ax.plot(qh_lis,z, label="qh")
"""
