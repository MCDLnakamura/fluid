"""
wrfoutから配列を読み取ってそれぞれの微物理過程のslopeパラメーターを求めて、それを用いて粒径分布を描写する。
密度の求め方はcal_den.f90を参考にする
(後で同様の方法でdbzも求めることが出来る)
その密度をもとに格子点ごとにラムダを求める。
そのラムダを基に粒径を掛けて、指数関数のグラフをかく。
（この時点でラムダマックスがモデルごとに設定されている点に注意する）
"""
mp="WSM7"
path="/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/late_run_041200/"+mp+"/wrfout_d03_2017-07-04_12:00:00"
moment=1
print(mp)

from matplotlib.pyplot import axis
from netCDF4 import Dataset
import numpy as np
from matplotlib import dates as mdates
from datetime import datetime as dt
import re
import math

import datetime
print(datetime.datetime.now())



#見る時間の指定(何コマ目か指定)
time=0

#見る高度の指定
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
rho_c=1000#雲と雨は与えられていないためとりあえず
rho_r=1000#雲と雨は与えられていないためとりあえず


#円周率
pi=3.141592

#ラムダの上限
LAMBDArmax=8.e4
LAMBDAsmax=1.e5
LAMBDAgmax=6.e4
LAMBDAhmax=2.e4


nc = Dataset(path, "r")
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

#ラムダの計算と出力それぞれの粒子についてそのモデルで取扱っているなら考える。------
qr=nc.variables['QRAIN']
if 'QNRAIN' in nc_var:
    n_r=nc.variables['QNRAIN']
v_r=2 #ウプシロンだが便宜的にvにしている
a_r=1 #アルファだが便宜的にaにしている

if moment==1:
    LAMBDA=((pi*rho_r*n0r)/(qr*rho_air))**0.25
elif moment==2:
    LAMBDA=((6/pi)*rho_r*((math.gamma(v_r+3/a_r))/(math.gamma(v_r)))*(n0r/(rho_air*qr)))**(1/3)  


LAMBDA=np.where(LAMBDA>LAMBDArmax,LAMBDArmax,LAMBDA)




np.save('LAMBDA_'+mp,LAMBDA)
print(LAMBDA.shape)
print("np.max(LAMBDA)",np.max(LAMBDA))
print("np.min(LAMBDA)",np.min(LAMBDA))