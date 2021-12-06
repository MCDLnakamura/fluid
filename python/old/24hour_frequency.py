"""
wrfoutから積算降水量の領域内の最大値をプロットするプログラム
観測地が1時間ごとの値であるので余裕があれば10分ごとの値を手入力したほうが美しくなる
→そうしたつもりだが、何故か積算値が小さいので一旦保留
"""
"""
11/16
最大値を見る場合に地点を変えない方がいいという指摘を受けたため書き直す
np.argmax()が使える
"""


from netCDF4 import Dataset
import numpy as np
from matplotlib import dates as mdates
from datetime import datetime as dt
import re


prep=[0,0,0,0,0,0,0,0,1.5,0.5,4.0,17.5,88.5,46.5,67.5,106,22.5,22.0,44.0,59,33.5,0.5,2.0,0.5]


prep144=[]
for i in range(24):
    for j in range(6):
        prep144.append(prep[i])
print(prep144)

"""
prep144=[
    0,0,0,0,0,0,
    0,0,0,0,0,0,
    0,0,0,0,0,0,
    0,0,0,0,0,0,
    0,0,0,0,0,0,
    0,0,0,0,0,0,
    0,0,0,0,0,0,
    0,0,0,0,0,0,
    0.5,1,0,0,0,0,
    0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.5, 0.0, 0.0, 0.5, 0.5, 10.0, 17.0, 13.0, 0.0, 0.5, 24.0, 21.0, 14.0, 12.0, 0.5, 11.0, 0.5, 0.5, 13.0, 11.0, 0.0, 0.5, 0.5, 17.0, 27.0, 26.0, 25.0, 23.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 17.0, 0.0, 0.5, 0.5, 0.0, 0.5, 0.5, 0.0, 0.0, 18.0, 0.0, 10.0, 0.5, 10.0, 0.0, 21.0, 0.0, 0.5, 19.0, 0.5, 0.5, 14.0, 12.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0]
"""

time=[]
for i in range(144):
    time.append(i+1)

acu =[prep[0]]
for i in range(1,24):
    acu.append(prep[i]+acu[i-1])

"""
acu144=[prep144[0]]
for i in range(1,144):
    acu144.append(prep144[i]+acu144[i-1])
print(acu144)
"""
acu144=[]
for i in range(24):
    for j in range(6):
        acu144.append(acu[i])

s_time=6*9
e_time=6*33
print(str(s_time)+'~'+str(e_time))


#print(time)

#1モデル目
nc = Dataset("/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/wrfout40s/06/wrfout_d03_2017-07-04_06:00:00", "r")
nc_var=nc.variables.keys()
if 'RAINNC'in nc_var:
    rainnc=nc.variables['RAINNC']
    #print(rainnc)
    rainnc=rainnc[s_time:e_time,:,:]
    rainnc=rainnc-rainnc[0,:,:]    
    place=np.unravel_index(np.argmax(rainnc[(e_time-s_time-1),:,:]), rainnc[(e_time-s_time-1),:,:].shape)
    max_06=rainnc[:,place[0],place[1]]
    #print(max_06)

    rainnc06=rainnc[(e_time-s_time-1),:,:] #度数分布のための配列

#2モデル目
nc = Dataset("/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/wrfout40s/16/wrfout_d03_2017-07-04_06:00:00", "r")
nc_var=nc.variables.keys()
if 'RAINNC'in nc_var:
    rainnc=nc.variables['RAINNC']
    #print(rainnc)
    rainnc=rainnc[s_time:e_time,:,:]
    rainnc=rainnc-rainnc[0,:,:]
    place=np.unravel_index(np.argmax(rainnc[(e_time-s_time-1),:,:]), rainnc[(e_time-s_time-1),:,:].shape)
    max_16=rainnc[:,place[0],place[1]]
    #print(max_16)

    rainnc16=rainnc[(e_time-s_time-1),:,:] #度数分布のための配列


#3モデル目
nc = Dataset("/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/wrfout40s/24/wrfout_d03_2017-07-04_06:00:00", "r")
nc_var=nc.variables.keys()
if 'RAINNC'in nc_var:
    rainnc=nc.variables['RAINNC']
    #print(rainnc)
    rainnc=rainnc[s_time:e_time,:,:]
    rainnc=rainnc-rainnc[0,:,:]    
    place=np.unravel_index(np.argmax(rainnc[(e_time-s_time-1),:,:]), rainnc[(e_time-s_time-1),:,:].shape)
    max_24=rainnc[:,place[0],place[1]]
    #print(max_24)

    rainnc24=rainnc[(e_time-s_time-1),:,:] #度数分布のための配列

#4モデル目
nc = Dataset("/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/wrfout40s/26/wrfout_d03_2017-07-04_06:00:00", "r")
nc_var=nc.variables.keys()
if 'RAINNC'in nc_var:
    rainnc=nc.variables['RAINNC']
    #print(rainnc)
    rainnc=rainnc[s_time:e_time,:,:]
    rainnc=rainnc-rainnc[0,:,:]    
    place=np.unravel_index(np.argmax(rainnc[(e_time-s_time-1),:,:]), rainnc[(e_time-s_time-1),:,:].shape)
    max_26=rainnc[:,place[0],place[1]]
    #print(max_26)

    rainnc26=rainnc[(e_time-s_time-1),:,:] #度数分布のための配列


from matplotlib import colors
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.dates import DateFormatter
fig = plt.figure()
fig, ax = plt.subplots()
#ax2 = ax.twinx()
"""
#軸の最大値、最小値
ax.set_xlim(0, 24*6)
ax.set_ylim(0, 200)
ax2.set_ylim(0, 600)

# x軸の目盛設定
xaxis_ = ax.xaxis
new_xticks = [0, 6*3, 6*6,6*9,6*12,6*15,6*18,6*21,6*24]  # 点がない場所でも良い
xaxis_.set_major_locator(ticker.FixedLocator(new_xticks))
ax.set_xticklabels([0,3,6,9,12,15,18,21,24])

#グラフタイトル
plt.title('precipitation')

#グラフの軸
ax.set_xlabel('Time 7/5 (JST)')
ax.set_ylabel('Hourly Rainfall(mm/h)')
ax2.set_ylabel('Accumlated Rainfall(mm)')

#プロット

#prep144_kai=[]
#for n in prep144:
#    prep144_kai.append(n*6)

ax.bar(time, prep144, width=1, color="blue")
ax2.plot(time,acu144, label="amedas(asakura)", color="black")
ax2.plot(time,max_06, label="WSM6 max")
ax2.plot(time,max_16, label="WDM6 max")
ax2.plot(time,max_24, label="WSM7 max")
ax2.plot(time,max_26, label="WDM7 max")

#グラフの凡例
ax2.legend()

fig.savefig("hour_maxpoint.png")
"""

"""
24時時点の降水量について度数分布も書いてみる
"""
#WSM6
rainnc06=np.ravel(rainnc06)
rainnc06.sort()
#rainnc06=rainnc06[200000:]
print(rainnc06)
plt.title('WSM6')
plt.yscale("log")
ax.set_xlim(0, 600)
ax.set_ylim(1, 300000)
ax.hist(rainnc06, bins=12, histtype='barstacked', ec='black',range=(0,600))
fig.savefig("frequency06.png")
plt.gca().clear()

#WDM6
rainnc16=np.ravel(rainnc16)
rainnc16.sort()
#rainnc06=rainnc06[200000:]
print(rainnc16)
plt.title('WDM6')
plt.yscale("log")
ax.set_xlim(0, 600)
ax.set_ylim(1, 300000)
ax.hist(rainnc16, bins=12, histtype='barstacked', ec='black',range=(0,600))
fig.savefig("frequency16.png")
plt.gca().clear()

#WSM7
rainnc24=np.ravel(rainnc24)
rainnc24.sort()
#rainnc24=rainnc24[200000:]
print(rainnc24)
plt.title('WSM7')
plt.yscale("log")
ax.set_xlim(0, 600)
ax.set_ylim(1, 300000)
ax.hist(rainnc24, bins=12, histtype='barstacked', ec='black',range=(0,600))
fig.savefig("frequency24.png")
plt.gca().clear()

#WDM7
rainnc26=np.ravel(rainnc26)
rainnc26.sort()
#rainnc26=rainnc26[200000:]
print(rainnc26)
plt.title('WDM7')
plt.yscale("log")
ax.set_xlim(0, 600)
ax.set_ylim(1, 300000)
ax.hist(rainnc26, bins=12, histtype='barstacked', ec='black',range=(0,600))
fig.savefig("frequency26.png")
plt.gca().clear()