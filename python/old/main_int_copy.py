"""
時間方向にも拡張して、割合を折れ線グラフで図示してみる
mpだけしか変わらないからモジュール化したほうがスマートかもしれない
"""

import os 
import numpy as np
from netCDF4 import Dataset

#自作モジュールのインポート
from dbz import *
from cors import *

mp="06h"
path="/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/late_run_041200/"+mp+"/"
file="wrfout_d03_2017-07-04_12:00:00"

nc = Dataset(path+file, "r")
qv=nc.variables['QVAPOR'][:]
idx_time,idx_eta,idx_lat,idx_lon=qv.shape


#dbz----------------------------------------------------------------------------------
for a in range(idx_time):#moduleと同じ変数でforしないほうがいいのかな？
    dbz_loop=dbz(path+file,a)
    dbz_loop = np.expand_dims(dbz_loop, axis = 0)
    if a==0:
        dbz_int = dbz_loop   
    else:
        dbz_int = np.append(dbz_int, dbz_loop, axis=0)


#一つのndarrayをnpyで保存: np.save()
name="dbz"
np.save(path+name, dbz_int) #dbzの保存
#dbz=np.load(path+name".npy") #読み込める

print(dbz_int.shape)
print(np.max(dbz_int))


#cors------------------------------------------------------------------------------------

#モジュールとの干渉があったら困るので読み直している
qv=nc.variables['QVAPOR'][:]
idx_time,idx_eta,idx_lat,idx_lon=qv.shape    

for a in range(idx_time):#moduleと同じ変数でforしないほうがいいのかな？
    cors_loop=cors(path+file,a,dbz_int[a,:,:,:])
    cors_loop = np.expand_dims(cors_loop, axis = 0)
    if a==0:
        cors_int = cors_loop
    else:
        cors_int = np.append(cors_int, cors_loop, axis=0)

#一つのndarrayをnpyで保存: np.save()
name="cors"
np.save(path+name, cors) #corsの保存
#cors=np.load(path+name".npy") #読み込める

print(cors.shape)
print(np.max(cors))    

#print("0",np.count_nonzero(cors==0))
print("1",np.count_nonzero(cors==1))
print("2",np.count_nonzero(cors==2))
print("3",np.count_nonzero(cors==3))



