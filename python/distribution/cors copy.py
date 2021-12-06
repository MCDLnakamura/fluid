"""
モジュール
wrfoutのnetcdf形式のファイルとdbzのarrayからyoshizumiの手法を参考にした
--- Using the method of Steiner et al. (1995) ---
あるグリッドのレーダー反射強度を周囲の平均反射強度と⽐較
を⾏うことで対流域と層状域を区別している
あるグリッドA 点の反射強度が40 dBZ 以上で
あれば，そのグリッドは対流域であると判別する
10 dBZ ～40 dBZでは，
とA点を中⼼とした半径11 kmの円（Figure 3.3bの緑円）内の
平均反射強度との差がデルタ以上の場合は対流域， 
未満の場合は層状域と判別される
デルタは半径内の平均反射強度の大きさによって決まる
0: initial(最初に与える値(未定義値)および(非降水域))
1: convective(40以上)
2: convective(周囲との比較の結果対流)
3: stratiform(層状)
"""
from netCDF4 import Dataset
import numpy as np

def cors(path,time,dbz):
    nc = Dataset(path, "r")
    xlong=nc.variables['XLONG'][time]
    xlat =nc.variables['XLAT'][time]
    qv=nc.variables['QVAPOR'][time]
    

    #もし形が適合しなければ処理を終了する
    if dbz.shape != qv.shape:
        print("dbz.shape",dbz.shape)
        print("qv.shape",qv.shape)
        print("different shape")
        exit()#プログラム終了)

    idx_eta,idx_lat,idx_lon=dbz.shape
    #解像度の計算(簡単のため経度のみで判断する
    #度からkm/gridに変換している
    #緯度方向で計算したほうが精度が良さげである
    resol_x=(xlong[idx_lon//2,-1]-xlong[idx_lon//2,0])/idx_lon*(40000/360) 
    resol_y=(xlat[-1,idx_lat//2]-xlat[0,idx_lon//2])/idx_lat*(40000/360)

    #あらかじめ時間に対してスライシングを行っている想定
    #どの層がいいのか分からないからとりあえず全部回す

    #半径11kmで判断するから、一番外の11kmは計算範囲から外す
    #念のため1グリッド分少なくする
    #直線で11kmになるグリット数を計算する
    outer=int(max(1+11//resol_x,1+11//resol_y))
    radius=outer-1

    outer^2


    #初期値
    #空の配列を作っておく
    cors=np.empty((idx_eta,idx_lat,idx_lon))
    #cors=np.zeros((idx_eta,idx_lat,idx_lon))
    
    for i in range(idx_eta):
        for j  in range(outer,idx_lat-outer):
            for k in range(outer,idx_lon-outer):
                if dbz[i,j,k]<=10:
                    np.put(cors, [i*idx_lat*idx_lon+j*idx_lon+k], 0)
                    #降水なし


                #ここから対流
                elif dbz[i,j,k]>40:
                    np.put(cors, [i*idx_lat*idx_lon+j*idx_lon+k], 1) 
                else:

                    z_bg=[]
                    
                    for m in range(-radius,radius+1):
                        for n in range(-radius,radius+1):
                            if m+n<=radius^2:
                                z_bg.append(dbz[i,j+m,k+n])
                    z_bg=np.mean(z_bg)

                    if z_bg >= 42.43:
                        np.put(cors, [i*idx_lat*idx_lon+j*idx_lon+k], 2)
                    elif 0<=z_bg<42.43 and 10-(z_bg**2)/180 < abs(dbz[i,j,k]-z_bg):
                        np.put(cors, [i*idx_lat*idx_lon+j*idx_lon+k], 2)
                    elif z_bg<0 and 10 < abs(dbz[i,j,k]-z_bg):
                        np.put(cors, [i*idx_lat*idx_lon+j*idx_lon+k], 2)

                #層状性
                    else:
                        np.put(cors, [i*idx_lat*idx_lon+j*idx_lon+k], 3)
                       

    return cors


                    


                    

                


