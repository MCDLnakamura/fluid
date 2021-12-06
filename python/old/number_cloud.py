"""
それぞれのモデルの数密度の領域平均の鉛直プロファイルをプロット
"""

from netCDF4 import Dataset
import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt
#matplotlib.colors.cnames
fig = plt.figure()
fig, ax = plt.subplots()



time=6*28
print("time")
print(time)


#高さはモデルから得られた方がうれしいい
z=[0.04091,0.08183,0.15841,0.25545,0.37742,0.52973,0.71816,0.94827,1.22537,1.55357,1.93508,2.36998,2.85595, 3.38889,3.96771,4.59579,5.27758,6.01716,6.79568,7.57622,8.34239,9.09342,9.82825,10.54624,11.24723,11.93144,12.59887,13.24895  ,13.88207  ,14.50039  ,15.10758  ,15.70753  ,16.30333  ,16.89835  ,17.49599  ,18.09865  ,18.70798  ,19.32486  ,19.94910  ,20.57838]
print("z")
print(z)
print(len(z))

#1モデル目(WSM6)
nc = Dataset("/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/wrfout40s/06/wrfout_d03_2017-07-04_06:00:00", "r")
nc_var=nc.variables.keys()
"""
if 'QNCCN' in nc_var:
    a_qccn=nc.variables['QNCCN']
    #print(a_qccn)
    a_qccn=a_qccn[time,:,:,:]
    a_qccn_z=[]
    a_qccn_z=np.mean(a_qccn, axis=(1,2))
    print("a_qccn_z")
    print(a_qccn_z)
"""

"""
if 'QNCLOUD' in nc_var:
    a_qnc=nc.variables['QNCLOUD']
    #print(a_qnc)
    a_qnc=a_qnc[time,:,:,:]
    a_qnc_z=[]
    a_qnc_z=np.mean(a_qnc, axis=(1,2))
    print("a_qnc_z")
    print(a_qnc_z)
"""
a_qnc_z=[]
for i in range(40):
    a_qnc_z.append(300e6)
print("a_qnc_z")
print(a_qnc_z)

"""
if 'QNRAIN' in nc_var:
    a_qnr=nc.variables['QNRAIN']
    #print(a_qnr)
    a_qnr=a_qnr[time,:,:,:]
    a_qnr_z=[]
    a_qnr_z=np.mean(a_qnr, axis=(1,2))
    print("a_qnr_z")
    print(a_qnr_z)
"""
"""
a_qnr_z=[]
for i in range(40):
    a_qnr_z.append(8.0e6)
print("a_qnr_z")
print(a_qnr_z)
"""
#2モデル目
nc = Dataset("/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/wrfout40s/16/wrfout_d03_2017-07-04_06:00:00", "r")
nc_var=nc.variables.keys()
if 'QNCCN' in nc_var:
    b_qccn=nc.variables['QNCCN']
    #print(b_qccn)
    b_qccn=b_qccn[time,:,:,:]
    b_qccn_z=[]
    b_qccn_z=np.mean(b_qccn, axis=(1,2))
    print("b_qccn_z")
    print(b_qccn_z)

if 'QNCLOUD' in nc_var:
    b_qnc=nc.variables['QNCLOUD']
    #print(b_qnc)
    b_qnc=b_qnc[time,:,:,:]
    b_qnc_z=[]
    b_qnc_z=np.mean(b_qnc, axis=(1,2))
    print("b_qnc_z")
    print(b_qnc_z)

if 'QNRAIN' in nc_var:
    b_qnr=nc.variables['QNRAIN']
    #print(b_qnr)
    b_qnr=b_qnr[time,:,:,:]
    b_qnr_z=[]
    b_qnr_z=np.mean(b_qnr, axis=(1,2))
    print("b_qnr_z")
    print(b_qnr_z)

#3モデル目
nc = Dataset("/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/wrfout40s/24/wrfout_d03_2017-07-04_06:00:00", "r")
nc_var=nc.variables.keys()
if 'QNCCN' in nc_var:
    c_qccn=nc.variables['QNCCN']
    #print(c_qccn)
    c_qccn=c_qccn[time,:,:,:]
    c_qccn_z=[]
    c_qccn_z=np.mean(c_qccn, axis=(1,2))
    print("c_qccn_z")
    print(c_qccn_z)

if 'QNCLOUD' in nc_var:
    c_qnc=nc.variables['QNCLOUD']
    #print(c_qnc)
    c_qnc=c_qnc[time,:,:,:]
    c_qnc_z=[]
    c_qnc_z=np.mean(c_qnc, axis=(1,2))
    print("c_qnc_z")
    print(c_qnc_z)

if 'QNRAIN' in nc_var:
    c_qnr=nc.variables['QNRAIN']
    #print(c_qnr)
    c_qnr=c_qnr[time,:,:,:]
    c_qnr_z=[]
    c_qnr_z=np.mean(c_qnr, axis=(1,2))
    print("c_qnr_z")
    print(c_qnr_z)

#4モデル目
nc = Dataset("/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/wrfout40s/26/wrfout_d03_2017-07-04_06:00:00", "r")
nc_var=nc.variables.keys()
if 'QNCCN' in nc_var:
    d_qccn=nc.variables['QNCCN']
    #print(d_qccn)
    d_qccn=d_qccn[time,:,:,:]
    d_qccn_z=[]
    d_qccn_z=np.mean(d_qccn, axis=(1,2))
    print("d_qccn_z")
    print(d_qccn_z)

if 'QNCLOUD' in nc_var:
    d_qnc=nc.variables['QNCLOUD']
    #print(d_qnc)
    d_qnc=d_qnc[time,:,:,:]
    d_qnc_z=[]
    d_qnc_z=np.mean(d_qnc, axis=(1,2))
    print("d_qnc_z")
    print(d_qnc_z)

if 'QNRAIN' in nc_var:
    d_qnr=nc.variables['QNRAIN']
    #print(d_qnr)
    d_qnr=d_qnr[time,:,:,:]
    d_qnr_z=[]
    d_qnr_z=np.mean(d_qnr, axis=(1,2))
    print("d_qnr_z")
    print(d_qnr_z)



print('plot')

ax.plot(a_qnc_z,z,label="cloud WSM6 and WSM7")
ax.plot(b_qnc_z,z,label="cloud WDM6")
#ax.plot(c_qnc_z,z,label="cloud WSM7")
ax.plot(d_qnc_z,z,label="cloud WDM7")

#ax.plot(b_qnr_z,z,label="rain WDM6")
#ax.plot(d_qnr_z,z,label="rain WDM7")

#軸の最大値、最小値
ax.set_xlim(0, 3e9)
ax.set_ylim(0, 15)

#グラフタイトル
plt.title('Averaged number concentration over d03(WDM7)')

#グラフの軸
ax.set_xlabel('number concentration ($\mathrm{m^{-3}}$)')
ax.set_ylabel('Height(km)')

#グラフの凡例
ax.legend()


fig.savefig("number_qnc.png")
print('fig.saved')