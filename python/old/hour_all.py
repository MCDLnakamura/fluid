"""
wrfoutから積算降水量の領域平均の24時間の時間発展をプロットするプログラム
解析雨量から観測地の近似値を求めようとしたがnetCDFファイルに変換してそれを見ると値がおかしいため、grib2より直接読み込む方法を試してみる11/13

"""

from netCDF4 import Dataset
from matplotlib import dates as mdates
from datetime import datetime as dt
import re
from matplotlib import colors
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.dates import DateFormatter
import struct
from itertools import repeat
fig = plt.figure()
fig, ax = plt.subplots()


s_time=6*9
e_time=6*33
print(str(s_time)+'~'+str(e_time))
time=[]
for i in range(6*24):
    time.append(i)
#積算降水量の領域合計を計算して時系列でプロットする

#1モデル目
nc = Dataset("/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/wrfout40s/06/wrfout_d03_2017-07-04_06:00:00", "r")
nc_var=nc.variables.keys()
if 'RAINNC'in nc_var:
    rainnc=nc.variables['RAINNC']
    print(rainnc)
    acu_sum_x=[]
    acu_sum_x=np.mean(rainnc, axis=1)
    acu_one=[]
    acu_one=np.mean(acu_sum_x, axis=1)
    acu_one=acu_one[s_time:e_time]
    print(acu_one)

#2モデル目
nc = Dataset("/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/wrfout40s/16/wrfout_d03_2017-07-04_06:00:00", "r")
nc_var=nc.variables.keys()
if 'RAINNC'in nc_var:
    rainnc=nc.variables['RAINNC']
    print(rainnc)
    acu_sum_x=[]
    acu_sum_x=np.mean(rainnc, axis=1)
    acu_two=[]
    acu_two=np.mean(acu_sum_x, axis=1)
    acu_two=acu_two[s_time:e_time]
    print(acu_two)


#3モデル目
nc = Dataset("/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/wrfout40s/24/wrfout_d03_2017-07-04_06:00:00", "r")
nc_var=nc.variables.keys()
if 'RAINNC'in nc_var:
    rainnc=nc.variables['RAINNC']
    print(rainnc)
    acu_sum_x=[]
    acu_sum_x=np.mean(rainnc, axis=1)
    acu_three=[]
    acu_three=np.mean(acu_sum_x, axis=1)
    acu_three=acu_three[s_time:e_time]
    print(acu_three)

#4モデル目
nc = Dataset("/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/wrfout40s/26/wrfout_d03_2017-07-04_06:00:00", "r")
nc_var=nc.variables.keys()
if 'RAINNC'in nc_var:
    rainnc=nc.variables['RAINNC']
    print(rainnc)
    acu_sum_x=[]
    acu_sum_x=np.mean(rainnc, axis=1)
    acu_four=[]
    acu_four=np.mean(acu_sum_x, axis=1)
    acu_four=acu_four[s_time:e_time]
    print(acu_four)

#解析雨量wgrib2のnetCDFは使えないようである
"""
kaiseki=[]
for i in (4,5):
    for j in range(24):
        k=str(j).zfill(2)

        #00分の分
        nc= Dataset("/home/nakamura_kento/temporary/R0"+str(i)+k+"00.nc","r")
            #print(nc)
                #<class 'netCDF4._netCDF4.Dataset'>
                #root group (NETCDF3_CLASSIC data model, file format NETCDF3):
                #Conventions: COARDS
                #History: created by wgrib2
                #GRIB2_grid_template: 0
                #dimensions(sizes): latitude(3360), longitude(2560), time(1)
                #variables(dimensions): float64 latitude(latitude), float64 longitude(longitude), float64 time(time), float32 var0_1_200_surface(time, latitude, longitude)
                #groups: 
        rainfall=nc.variables['var0_1_200_surface']
            #print(rainfall)
                #<class 'netCDF4._netCDF4.Variable'>
                #float32 var0_1_200_surface(time, latitude, longitude)
                #_FillValue: 9.999e+20
                #short_name: var0_1_200_surface
                #long_name: desc
                #level: surface
                #units: unit
                #unlimited dimensions: time
                #current shape = (1, 3360, 2560)
                #filling on
        rainfall=np.mean(rainfall, axis=(1,2))
            #print(rainfall)
                #[7.338187e+20]
        kaiseki.append(float(rainfall))
        
        #30分の分
        nc= Dataset("/home/nakamura_kento/temporary/R0"+str(i)+k+"00.nc","r")
        #print(nc)
        rainfall=nc.variables['var0_1_200_surface']
        #print(rainfall)
        #current shape = (1, 3360, 2560)
        rainfall=np.mean(rainfall, axis=(1,2))
        kaiseki.append(float(rainfall))

print(len(kaiseki))
kaiseki=kaiseki[2*15:2*(15+24)]
print(len(kaiseki))
print(kaiseki)

#積算量に変更する(1/6が必要)
acu_kai=[]
for i in range(48):
    if i ==0:
        for j in range(3):
            acu_kai.append(kaiseki[i]/6)
    else:
        for j in range (3):
            acu_kai.append(kaiseki[i]/6 + acu_kai[i-1])
#print(acu_kai)
"""

#grib2.binから直接読み込む方か良さげである
"""未完成です
file="~/temporary/Z__C_RJTD_20170701000000_SRF_GPV_Ggis1km_Prr60lv_ANAL_grib2.bin"
def load_jmara_grib2(file):
    r
    with open(file, 'rb') as f:
        binary = f.read()
    len_ = {'sec0':16, 'sec1':21, 'sec3':72, 'sec4':82, 'sec6':6}

    end4 = len_['sec0'] + len_['sec1'] + len_['sec3'] + len_['sec4'] - 1
    len_['sec5'] = struct.unpack_from('>I', binary, end4+1)[0]
    section5 = binary[end4:(end4+len_['sec5']+1)]
    power = section5[17]
    print(power)
    
    end6 = end4 + len_['sec5'] + len_['sec6']
    len_['sec7'] = struct.unpack_from('>I', binary, end6+1)[0]
    section7 = binary[end6:(end6+len_['sec7']+1)]
    
    highest_level = struct.unpack_from('>H', section5, 13)[0]
    level_table = _set_table(section5)
    decoded = np.fromiter(
        _decode_runlength(section7[6:], highest_level), dtype=np.int16
    ).reshape((3360, 2560))
"""


#軸の最大値、最小値
ax.set_xlim(0, 24*6)
ax.set_ylim(0, 20)

# x軸の目盛設定
xaxis_ = ax.xaxis
new_xticks = [0, 6*3, 6*6,6*9,6*12,6*15,6*18,6*21,6*24]  # 点がない場所でも良い
xaxis_.set_major_locator(ticker.FixedLocator(new_xticks))
ax.set_xticklabels([0,3,6,9,12,15,18,21,24])

#グラフタイトル
plt.title('averaged precipitation')

#グラフの軸
ax.set_xlabel('Time 7/5 (JST)')
ax.set_ylabel('averaged Rainfall(mm)')

#プロット
#ax.plot(time,obs, label="amedas", color="black")
ax.plot(time,acu_one-acu_one[0], label="WSM6")
ax.plot(time,acu_two-acu_two[0], label="WDM6")
ax.plot(time,acu_three-acu_three[0], label="WSM7")
ax.plot(time,acu_four-acu_four[0], label="WDM7")
#ax.plot(time,acu_kai,label="OBS")

#グラフの凡例
ax.legend()

fig.savefig("hour_all.png")