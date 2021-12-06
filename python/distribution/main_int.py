"""
時間方向にも拡張して、割合を折れ線グラフで図示してみるのが目標
"""

import os 
import numpy as np
from netCDF4 import Dataset
from wrf import *
import os
import sys

import pyximport; pyximport.install(pyimport = True)

print("start")
print(os.system("date"))
# mp_k = ("WSM6","WSM6_h","WDM6","WDM6_h","WSM7","WDM7")
mp_k = ("WDM7","WSM6")
for mp in mp_k:
    print(mp)
    sys.stdout.flush()
    print(os.system("date"))

    path="/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/late_run_041200/"+mp+"/"
    file="wrfout_d03_2017-07-04_12:00:00"
    
    nc = Dataset(path+file, "r")
    qv=nc.variables['QVAPOR'][:]
    idx_time,idx_eta,idx_lat,idx_lon=qv.shape

    """
    #dbz----------------------------------------------------------------------------------
    print("dbz")
    sys.stdout.flush()
    print(os.system("date"))
    
    dbz_int = []
    for a in range(idx_time):
        dbz_loop= getvar(nc, "dbz", timeidx=a)
        dbz_loop= np.ma.masked_array(dbz_loop)
        dbz_int.append(dbz_loop)
    
    #dbz_int=getvar(nc, "dbz", ALL_TIMES)#loopで足していくほうが速い!!
    np.save(path+"dbz_int", dbz_int) #dbzの保存
    """
    dbz_int=np.load(path+"dbz_int.npy", allow_pickle=True) #読み込める
    

    #cors------------------------------------------------------------------------
    print("cors")
    sys.stdout.flush()
    print(os.system("date"))
    from cors import cors
    cors_int=[]
    for a in range(idx_time):
        cors_loop=cors(path+file,a,dbz_int[a,:,:,:])
        cors_loop= np.ma.masked_array(cors_loop)
        cors_int.append(cors_loop)
    
    np.save(path+"cors_int", cors_int) #corsの保存
    cors_int=np.load(path+"cors_int.npy", allow_pickle=True) #読み込める   

    """
    # 上昇流と下降流の判別-------------------------------------------------------------
    print("life")
    sys.stdout.flush()
    print(os.system("date"))
    from cloud_life import life
    life_up_int=[]
    life_dw_int=[]
    for a in range(idx_time):
        life_up,life_dw=life(path+file,a,cors_int[a,:,:,:])
        life_up= np.ma.masked_array(life_up)
        life_dw= np.ma.masked_array(life_dw)
        life_up_int.append(life_up)
        life_dw_int.append(life_dw)

    np.save(path+"life_up_int", life_up_int) 
    cors=np.load(path+"life_up_int.npy", allow_pickle=True) #読み込める

    np.save(path+"life_dw_int", life_dw_int) 
    cors=np.load(path+"life_dw_int.npy", allow_pickle=True) #読み込める
    """
    