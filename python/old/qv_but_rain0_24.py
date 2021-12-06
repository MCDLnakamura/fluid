"""
それぞれのモデルの混合比の領域平均の鉛直プロファイルをプロット
rain=0を除いたよ
"""

from netCDF4 import Dataset
import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt
#matplotlib.colors.cnames
fig = plt.figure()
fig, ax = plt.subplots()

#モデルの指定
mp=str(24)
mp=str(mp.zfill(2))

nc = Dataset("/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/wrfout40s/"+mp+"/wrfout_d03_2017-07-04_06:00:00", "r")

nc_var=nc.variables.keys()

time=6*28
print(time)

z=[0.04091,0.08183,0.15841,0.25545,0.37742,0.52973,0.71816,0.94827,1.22537,1.55357,1.93508,2.36998,2.85595, 3.38889,3.96771,4.59579,5.27758,6.01716,6.79568,7.57622,8.34239,9.09342,9.82825,10.54624,11.24723,11.93144,12.59887,13.24895  ,13.88207  ,14.50039  ,15.10758  ,15.70753  ,16.30333  ,16.89835  ,17.49599  ,18.09865  ,18.70798  ,19.32486  ,19.94910  ,20.57838]
print(z)

###rainが(13)番目の層において0の地点は除外するようにする
##forとifで2重に囲んで探索する形にする 
##QVAPOR(Time, bottom_top, south_north, west_east)であることを考えて、
z_cut=13 #番目(0インデックスだよ)
qr=nc.variables['QRAIN']
qrz=[]
sha=qr.shape

if 'QCLOUD' in nc_var:
    print('QCLOUD')
    qc=nc.variables['QCLOUD']
    qcz=[]
    for k in range(sha[1]):
        qch=[]
        for i in range(sha[2]):
            for j in range(sha[3]):
                if qr[time,z_cut,i,j]>0:
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
                if qr[time,z_cut,i,j]>0:
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
                if qr[time,z_cut,i,j]>0:
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
                if qr[time,z_cut,i,j]>0:
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
                if qr[time,z_cut,i,j]>0:
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
                if qr[time,z_cut,i,j]>0:
                    qhh.append(qh[time,k,i,j])
        qhz.append(np.mean(qhh))
    print(qhz)
    qh_lis=[]
    for n in qhz:
        qh_lis.append(n*1000)
    ax.plot(qh_lis,z, label="qh")

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


fig.savefig(mp+"_vq_1000_but_rain0.png")
print('fig.saved')
