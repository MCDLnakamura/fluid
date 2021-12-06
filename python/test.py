from shade_v import * 
import numpy as np
path="/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/late_run_041200/26/wrfout_d03_2017-07-04_12:00:00"
time=6*27
nl, sl, el, wl = 34.5, 32.5, 132, 130 
lev=np.arange(100, 1000, 100) #範囲の設定
variables='RAINNC'
title="rainnc"
name="test.png"
shade(path,time,nl, sl, el, wl,lev,variables,title,name)