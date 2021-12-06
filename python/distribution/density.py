"""
wrfoutから配列を読み取って密度を求める
密度の求め方はcal_den.f90を参考にした
"""


from matplotlib.pyplot import axis
from netCDF4 import Dataset
import numpy as np
from matplotlib import dates as mdates
from datetime import datetime as dt
import re
import math

import datetime
dt_now = datetime.datetime.now()
print(dt_now)



#見る時間の指定(何コマ目か指定)
time=6*22

#見る高度の指定(モデルの高さが何番目か)
height=10

#intercept parameter(切片)
#WSM6,WDM6,WSM7,WDM7以外のスキームでは異なる可能性が有る
n0r=8.e4
n0g=4.e6
n0h=4.e4
n0s=2.e6

#density(密度kg/m^3)
rho_g=500
rho_s=100.0
rho_h=912
rho_c=1000#雲
rho_r=1000#雨


#円周率
pi=3.141592

#ラムダの上限
lamdarmax=8.e4
lamdasmax=1.e5
lamdagmax=6.e4
lamdahmax=2.e4

nc = Dataset("/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/wrfout40s/06/wrfout_d03_2017-07-04_06:00:00", "r")
nc_var=nc.variables.keys()


#データの取得-----------------------------------------------------------
#温位から密度を求める
#T00を求める
t0=nc.variables['T00']#THMとの違いは要確認
#print(t0)
t0=t0[:]
print("np.mean(t0)",np.mean(t0),"k")
#float T00(Time)
t0=t0[:,np.newaxis,np.newaxis,np.newaxis]

T=nc.variables['T']#THMとの違いは要確認
#print(theta)
T=T[:,:,:,:]
#idx_time,idx_eta,idx_lat,idx_lon=theta.shape 
theta=T + t0         
print("np.mean(theta)",np.mean(theta),"k")
#float T(Time, bottom_top, south_north, west_east)



pb=nc.variables['PB']#PBとの違いは要確認
p=nc.variables['P']
#print(p)
p=p[:,:,:,:]+pb[:,:,:,:]
print("np.mean(p)",np.mean(p),"Pa")
#float P(Time, bottom_top, south_north, west_east)
qv=nc.variables['QVAPOR']#水蒸気混合比
#float QVAPOR(Time, bottom_top, south_north, west_east)
#print(qv)
qv=qv[:,:,:,:]
print("np.mean(qv)",np.mean(qv),"kg/kg")


#中間数tvの計算と出力---------------------------------------------------------
#tvはよくわからないが一旦出している
tv=theta*((p/1.e5)**0.286e0)*(1.e0+0.61e0*qv)
print("tv.shape",tv.shape)
print("np.mean(tv)",np.mean(tv))
print("tv[time,height,0,0]",tv[time,height,0,0],"K")
#0.286e0はカッパー、0.61は謎



#密度の計算と出力------------------------------------------------------------
#状態方程式を用いてrho_airで密度を求めている
#乾燥空気の気体定数287(j/(kg K))が出てる
rho_air=p/(287.e0*tv)
print("rho_air.shape",rho_air.shape)
print("np.mean(rho_air)",np.mean(rho_air))
print("rho_air[time,height,0,0]",rho_air[time,height,0,0],"kg/m^3")

