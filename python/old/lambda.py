"""
ラムダを求めたい...
"""

from netCDF4 import Dataset
import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt
#matplotlib.colors.cnames
import array
fig = plt.figure()
fig, ax = plt.subplots()

nc = Dataset("/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/wrfout40s/26/wrfout_d03_2017-07-04_06:00:00", "r")

n0r=8.e6
n0g=4.e6
n0h=4.e4
n0s=2.e6

pi=3.141592
R=0.3


nc_var=nc.variables.keys()

time=6*28
print("time")
print(time)

psfc=nc.variables['PSFC'][:]
psfc=psfc[time,:,:]
print("psfc.shape")
print(psfc.shape)
print(np.mean(psfc,axis=(0,1)))
"""
p0=[]
for i in range(40):
    p0.append(psfc[:,:])
p0=np.array(p0)
print("p0.shape")
print(p0.shape)
"""
p=nc.variables['P']
p=p[time,1:20,:,:]
print("p.shape")
print(p.shape)
p=p*100
print(np.mean(p,axis=(1,2)))


theta=nc.variables['T']
theta=theta[time,1:20,:,:]
t2=nc.variables['T2']
t2=t2[time,1:20,:]
print("theta.shape")
print(theta.shape)
print(np.mean(theta, axis=(1,2))+np.mean(t2, axis=(0,1)))

t=theta*(psfc/p)**0.714
print("t.shape")
print(t.shape)
t=np.mean(t,axis=(0,1,2))
print(t)

if 'QRAIN' in nc_var:
    qr=nc.variables['QRAIN']
    qr=qr[time,1:20,:,:]
    print("qr.shape")
    print(qr.shape)
    qr=np.mean(qr,axis=(0,1,2))
    print(qr)
    lam_r=(R*pi*n0r*t)/qr
    print("lam_r")
    print(lam_r)
    if lam_r >8.e4:
        lam_r=8.e4
    d=0.001
    nrx=n0r*np.exp(-lam_r*d)
    print(nrx)
    #print(np.mean(nrx,axis=(1,2)))

    





"""


z=[0.04091,0.08183,0.15841,0.25545,0.37742,0.52973,0.71816,0.94827,1.22537,1.55357,1.93508,2.36998,2.85595, 3.38889,3.96771,4.59579,5.27758,6.01716,6.79568,7.57622,8.34239,9.09342,9.82825,10.54624,11.24723,11.93144,12.59887,13.24895  ,13.88207  ,14.50039  ,15.10758  ,15.70753  ,16.30333  ,16.89835  ,17.49599  ,18.09865  ,18.70798  ,19.32486  ,19.94910  ,20.57838]
print(z)

if 'QVAPOR' in nc_var:
    qv=nc.variables['QVAPOR']
    print(qv)
    qv_zxy=[]
    qv_zxy=qv[time,:,:,:]
    qv_xz=np.mean(qv_zxy, axis=2)
    qv_z=[]
    qv_z=np.mean(qv_xz, axis=1)
    print(qv_z)
    qv_lis=[]
    for n in qv_z:
        qv_lis.append(n*1000)

if 'QCLOUD' in nc_var:
    qc=nc.variables['QCLOUD']
    print(qc)
    qc_zxy=[]
    qc_zxy=qc[time,:,:,:]
    qc_xz=np.mean(qc_zxy, axis=2)
    qc_z=[]
    qc_z=np.mean(qc_xz, axis=1)
    print(qc_z)
    qc_lis=[]
    for n in qc_z:
        qc_lis.append(n*1000)



if 'QICE' in nc_var:
    qi=nc.variables['QICE']
    print(qi)
    qi_zxy=[]
    qi_zxy=qi[time,:,:,:]
    qi_xz=np.mean(qi_zxy, axis=2)
    qi_z=[]
    qi_z=np.mean(qi_xz, axis=1)
    print(qi_z)
    qi_lis=[]
    for n in qi_z:
        qi_lis.append(n*1000)

if 'QSNOW' in nc_var:
    qs=nc.variables['QSNOW']
    print(qs)
    qs_zxy=[]
    qs_zxy=qs[time,:,:,:]
    qs_xz=np.mean(qs_zxy, axis=2)
    qs_z=[]
    qs_z=np.mean(qs_xz, axis=1)
    print(qs_z)
    qs_lis=[]
    for n in qs_z:
        qs_lis.append(n*1000)

if 'QGRAUP' in nc_var:
    qg=nc.variables['QGRAUP']
    print(qg)
    qg_zxy=[]
    qg_zxy=qg[time,:,:,:]
    qg_xz=np.mean(qg_zxy, axis=2)
    qg_z=[]
    qg_z=np.mean(qg_xz, axis=1)
    print(qg_z)
    qg_lis=[]
    for n in qg_z:
        qg_lis.append(n*1000)

if 'QHAIL' in nc_var:
    qh=nc.variables['QHAIL']
    print(qh)
    qh_zxy=[]
    qh_zxy=qh[time,:,:,:]
    qh_xz=np.mean(qh_zxy, axis=2)
    qh_z=[]
    qh_z=np.mean(qh_xz, axis=1)
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
plt.title('Averaged q-profile over d03(WDM7)')

#グラフの軸
ax.set_xlabel('Mixing ratio (g/kg)')
ax.set_ylabel('Height(km)')

#グラフの凡例
ax.legend()


fig.savefig("26_vq_1000.png")
print('fig.saved')
"""