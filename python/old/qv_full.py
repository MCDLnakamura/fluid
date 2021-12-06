"""
それぞれのモデルの混合比の領域平均の鉛直プロファイルをプロット
"""

from netCDF4 import Dataset
import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt
#matplotlib.colors.cnames
fig = plt.figure()
fig, ax = plt.subplots()

#モデルの指定
mp=str(6)
mp=str(mp.zfill(2))

nc = Dataset("/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/wrfout40s/"+mp+"/wrfout_d03_2017-07-04_06:00:00", "r")

nc_var=nc.variables.keys()

time=6*28
print(time)

z=[0.04091,0.08183,0.15841,0.25545,0.37742,0.52973,0.71816,0.94827,1.22537,1.55357,1.93508,2.36998,2.85595, 3.38889,3.96771,4.59579,5.27758,6.01716,6.79568,7.57622,8.34239,9.09342,9.82825,10.54624,11.24723,11.93144,12.59887,13.24895  ,13.88207  ,14.50039  ,15.10758  ,15.70753  ,16.30333  ,16.89835  ,17.49599  ,18.09865  ,18.70798  ,19.32486  ,19.94910  ,20.57838]
print(z)


if 'QVAPOR' in nc_var:
    qv=nc.variables['QVAPOR']
    print(qv)
    qv_zxy=[]
    qv_zxy=qv[time,:,:,:]
    qv_z=np.mean(qv_zxy, axis=(1,2))
    print(qv_z)
    qv_lis=[]
    for n in qv_z:
        qv_lis.append(n*1000)

if 'QCLOUD' in nc_var:
    qc=nc.variables['QCLOUD']
    print(qc)
    qc_zxy=[]
    qc_zxy=qc[time,:,:,:]
    qc_z=np.mean(qc_zxy, axis=(1,2))
    print(qc_z)
    qc_lis=[]
    for n in qc_z:
        qc_lis.append(n*1000)

if 'QRAIN' in nc_var:
    qr=nc.variables['QRAIN']
    print(qr)
    qr_zxy=[]
    qr_zxy=qr[time,:,:,:]
    qr_z=np.mean(qr_zxy, axis=(1,2))
    print(qr_z)
    qr_lis=[]
    for n in qr_z:
        qr_lis.append(n*1000)

if 'QICE' in nc_var:
    qi=nc.variables['QICE']
    print(qi)
    qi_zxy=[]
    qi_zxy=qi[time,:,:,:]
    qi_z=np.mean(qi_zxy, axis=(1,2))
    print(qi_z)
    qi_lis=[]
    for n in qi_z:
        qi_lis.append(n*1000)

if 'QSNOW' in nc_var:
    qs=nc.variables['QSNOW']
    print(qs)
    qs_zxy=[]
    qs_zxy=qs[time,:,:,:]
    qs_z=np.mean(qs_zxy, axis=(1,2))
    print(qs_z)
    qs_lis=[]
    for n in qs_z:
        qs_lis.append(n*1000)

if 'QGRAUP' in nc_var:
    qg=nc.variables['QGRAUP']
    print(qg)
    qg_zxy=[]
    qg_zxy=qg[time,:,:,:]
    qg_z=np.mean(qg_zxy, axis=(1,2))
    print(qg_z)
    qg_lis=[]
    for n in qg_z:
        qg_lis.append(n*1000)

if 'QHAIL' in nc_var:
    qh=nc.variables['QHAIL']
    print(qh)
    qh_zxy=[]
    qh_zxy=qh[time,:,:,:]
    qh_z=np.mean(qh_zxy, axis=(1,2))
    print(qh_z)
    qh_lis=[]
    for n in qh_z:
        qh_lis.append(n*1000)


print('plot')

#if 'QVAPOR' in nc_var:
    #ax.plot(qv_lis,z, label="qv")
if 'QCLOUD' in nc_var:
    ax.plot(qc_lis,z, label="qc")
if 'QRAIN' in nc_var:
    ax.plot(qr_lis,z, label="qr")
if 'QICE' in nc_var:
    ax.plot(qi_lis,z, label="qi")
if 'QSNOW' in nc_var:
    ax.plot(qs_lis,z, label="qs")
if 'QGRAUP' in nc_var:
    ax.plot(qg_lis,z, label="qg")
if 'QHAIL' in nc_var:
    ax.plot(qh_lis,z, label="qh")


#軸の最大値、最小値
ax.set_xlim(-0.005, 0.105)
ax.set_ylim(0, 15)

#グラフタイトル
plt.title("Averaged q-profile over d03("+mp+")")

#グラフの軸
ax.set_xlabel('Mixing ratio (g/kg)')
ax.set_ylabel('Height(km)')

#グラフの凡例
ax.legend()


fig.savefig(mp+"_vq_1000.png")
print('fig.saved')
