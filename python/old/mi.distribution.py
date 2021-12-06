from netCDF4 import Dataset
import numpy as np
from matplotlib import dates as mdates
from datetime import datetime as dt
import re
import math

n0r=8.e6
n0g=4.e6
n0h=4.e4
n0s=2.e6

pi=3.141592
R=0.3

#WSM6
nc = Dataset("/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/wrfout40s/06/wrfout_d03_2017-07-04_06:00:00", "r")
nc_var=nc.variables.keys()
if 'QVAPOR' in nc_var:
    qv=nc.variables['QVAPOR']
if 'QCLOUD' in nc_var:
    qc=nc.variables['QCLOUD']
if 'QRAIN' in nc_var:
    qr=nc.variables['QRAIN']
if 'QICE' in nc_var:
    qi=nc.variables['QICE']
if 'QSNOW' in nc_var:
    qs=nc.variables['QSNOW']
if 'QGRAUP'in nc_var:
    qg=nc.variables['QGURAUP']
if 'QHAIL' in nc_var:
    qh=nc.variables['QHAIL']

if 'P' in nc_var:
    p=nc.variables['P']

if 'T' in nc_var:
    t=nc.variables['T']
"""
#これは温位なので温度に直す
    tc=[]
    for n in t:
        tc.append(t-6)
#よくわからないから大体2~3kmぐらいの温度にしておく
"""

d = np.linspace( 0, 1, 1000)

if 'QRAIN' in nc_var:
    lam_r=(R*t*pi*n0r)/(p*qr)
    n=n0r*math.exp(-1*lam_r*d)
if 'QGRAUP'in nc_var:
    lam_g=(R*t*pi*n0g)/(p*qg)
if 'QHAIL' in nc_var:
    lam_h=(R*t*pi*n0h)/(p*qh)
if 'QSNOW' in nc_var:
    lam_s=(R*t*pi*n0s)/(p*qs)



