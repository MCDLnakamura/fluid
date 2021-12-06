"""
1つのモデルで1つの時間についての対流域と層状域の判定の解析用スクリプト
時間発展させたものが上手く行かないのでとりまこれを使う
"""

import numpy as np

mp="WDM6"
path="/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/late_run_041200/"+mp+"/"
file="wrfout_d03_2017-07-04_12:00:00"
print("import"+path+file)
time=6*22


from wrf import *
from netCDF4 import Dataset
nc = Dataset(path+file, "r")
dbz= getvar(nc, "dbz", timeidx=time)
print("dbz.shape",dbz.shape)
print("np.max(dbz)",np.max(dbz))

#dbzの保存
#一つのndarrayをnpyで保存: np.save()
name="dbz"
np.save(path+name+str(time), dbz) #保存


dbz=np.load(path+name+str(time)+".npy") #読み込める

print(dbz)
print(np.max(dbz))

from cors import cors
cors=cors(path+file,time,dbz)
print(cors)
print(np.max(cors))

name="cors"
np.save(path+name+str(time), cors) #保存
cors=np.load(path+name+str(time)+".npy") #読み込める

print("0",np.count_nonzero(cors==0))
print("1",np.count_nonzero(cors==1))
print("2",np.count_nonzero(cors==2))
print("3",np.count_nonzero(cors==3))


from cloud_life import life
life_up,life_dw=life(path+file,time,cors)


np.save(path+"life_up"+str(time), life_up) #保存
np.save(path+"life_dw"+str(time), life_dw) #保存

life_up=np.load(path+"life_up"+str(time)+".npy") #読み込める
life_dw=np.load(path+"life_dw"+str(time)+".npy") #読み込める

print("up",np.count_nonzero(life_up==1))
print("dw",np.count_nonzero(life_dw==1))