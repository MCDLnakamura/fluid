"""
wrfoutのnetcdf形式のファイルから指定された時刻のdbzを求めるモジュール
ARWpostを参考に作成
    cname    = "dbz"
    cdesc    = "Reflectivity"
    cunits   = "-"

11/26に
wrf.pythonにてdbzが容易に計算できることを発見（恐らくこれ以降は使わないであろう）
"""
from netCDF4 import Dataset
import numpy as np

def dbz(path,time): 

    #変数の定義
    #実際にモデルで使われている数字はコメントアウトしてある

    #density(密度kg/m^3)
    rho_g=400
    #rho_g=500
    rho_s=100
    #rho_h=912
    RHOWAT=1000
    rho_c=RHOWAT#雲 #rho_r = RHOWATとあった
    rho_r=RHOWAT#雨
    
    r1 = 1.e-15
    ron = 8.e6
    ron2 = 1.e10
    son = 2.e7
    gon = 5.e7
    ron_min = 8.e6
    ron_qr0 = 0.00010
    ron_delqr0 = 0.25*ron_qr0
    ron_const1r = (ron2-ron_min)*0.5
    ron_const2r = (ron2+ron_min)*0.5

    gamma_seven = 720
    alpha = 0.224

    CELKEL = 273.15 #絶対零度
    PI=3.14159265358979
    
    nc = Dataset(path, "r")
    nc_var=nc.variables.keys()
    qv=nc.variables['QVAPOR'][time]
    qr=nc.variables['QRAIN'][time]
    qs = 0.0
    qg = 0.0
    if 'QSNOW' in nc_var:
        qs=nc.variables['QSNOW'][time]
    if 'QGRAUP' in nc_var:
        qg=nc.variables['QGRAUP'][time]
    
    #temperature in Kを求める
    #温位を求める#T00を求める
    t0=nc.variables['T00'][time]
    t0=t0[np.newaxis,np.newaxis,np.newaxis]
    T=nc.variables['T'][time]
    theta=T + t0
    idx_eta,idx_lat,idx_lon=theta.shape
    pb=nc.variables['PB'][time]
    p=nc.variables['P'][time]
    p=p+pb
    tmk=theta*((p/1.e5)**0.286e0)#yoshizumiを参考にした
    prs=p
    
    """
    今回は雪と霰を分けたものしか考えていないから（6クラス以上）この部分は要らない
    3,5クラスをするなら必要

    if ( np.max(qs) == 0.0 and np.max(qg) == 0.0 ):#No ice in this run
        if (tmk < CELKEL): #temperature in Kを取ってくる
            qr = 0.0
            qs = qr
    """

    """
    多分負の値は無かったからこれはしなくて問題ないと思う(未定義値の扱いがどうか?)
    qv = max(np.max(qv), 0.0)
    qr = max(np.max(qr), 0.0)
    qs = max(np.max(qs), 0.0)
    qg = max(np.max(qg), 0.0)
    """
    factor_r = gamma_seven * 1.e18 * (1./(PI*rho_r))**1.75
    factor_s = gamma_seven * 1.e18 * (1./(PI*rho_s))**1.75 * (rho_s/RHOWAT)**2 * alpha
    factor_g = gamma_seven * 1.e18 * (1./(PI*rho_g))**1.75 * (rho_g/RHOWAT)**2 * alpha

    #密度の計算(yoshizumiの方法に変更)
    tv=theta*((p/1.e5)**0.286e0)*(1.e0+0.61e0*qv)
    rhoair=p/(287.e0*tv)
    """
    Adjust factor for brightband, where snow or graupel particle
    scatters like liquid water (alpha=1.0) because it is assumed to
    have a liquid skin.
    """
    #空の配列を作っておく
    SCR=np.empty((idx_eta,idx_lat,idx_lon)) 

    #あらかじめ時間に対してスライシングを行っている想定
    for i in range(idx_eta):
        for j  in range(idx_lat):
            for k in range(idx_lon):
                if (tmk[i,j,k] > CELKEL):
                    factorb_s=factor_s/alpha
                    factorb_g=factor_g/alpha
                else:
                    factorb_s=factor_s
                    factorb_g=factor_g
    #Calculate variable intercept parameters
                temp_c =min(-0.001, tmk[i,j,k]-CELKEL)
                sonv   =min(2.0e8, 2.0e6*np.exp(-0.12*temp_c))

                gonv = gon
                if (qg[i,j,k] > r1):
                    gonv = 2.38*(PI*rho_g/(rhoair[i,j,k]*qg[i,j,k]))**0.92
                    gonv = max(1.e4, min(gonv,gon))
                
                ronv = ron2
                if (qr[i,j,k]> r1):
                    ronv = ron_const1r*np.tanh((ron_qr0-qr[i,j,k])/ron_delqr0) + ron_const2r
            
    #Total equivalent reflectivity factor (z_e, in mm^6 m^-3) is the sum of z_e for each hydrometeor species
                z_e =   factor_r  * (abs(rhoair[i,j,k]*qr[i,j,k]))**1.75 /abs(ronv)**.75 + factorb_s * abs((rhoair[i,j,k]*qs[i,j,k]))**1.75 /abs(sonv)**.75 + factorb_g * (abs(rhoair[i,j,k]*qg[i,j,k]))**1.75 /abs(gonv)**.75

    #Adjust small values of Z_e so that dBZ is no lower than -30
                z_e = max(z_e, 0.001)

    #Convert to dBZ
                np.put(SCR, [i*idx_lat*idx_lon+j*idx_lon+k], 10*np.log10(z_e)) 
    
    return SCR