"""
wrfoutから積算降水量の領域内の最大値をプロットするプログラム
観測地が1時間ごとの値であるので余裕があれば10分ごとの値を手入力したほうが美しくなる
→そうしたつもりだが、何故か積算値が小さいので一旦保留

11/16
最大値を見る場合に地点を変えない方がいいという指摘を受けたため書き直す
np.argmax()が使える
前に作った図と最大値が異なる点は解決した

11/20
6モデル（6クラスのhailモードに対応した）に変更
度数分布と領域平均も同時に出力するように変更
パスが通ってない場合にはエラーが出らずにそのまま処理をするように変更した。
11/28
一括処理を分けた
"""
#処理の開始時刻を表示させる(特に意味はない)
from datetime import datetime 
print(datetime.now())

import numpy as np
import re
import os
import subprocess

ana_max=np.load("/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/late_run_041200/maxpoint.npy")
print(len(ana_max))
ana_144=[]
for i in range(48):
    for j in range(4):
        ana_144.append(ana_max[i])
print("ana_144",len(ana_144),ana_144)
ana_acu=[ana_144[0]]
for i in range(1,144):
    ana_acu.append(ana_acu[i-1]+ana_144[i]/3)
print(ana_acu)

##20170705(JST)の10分ごとの降水量の観測地(朝倉のアメダス)-------------------------------
prep144=[
    0,0,0,0,0,0,
    0,0,0,0,0,0,
    0,0,0,0,0,0,
    0,0,0,0,0,0,
    0,0,0,0,0,0,
    0,0,0,0,0,0,
    0,0,0,0,0,0,
    0,0,0,0,0,0,
     0.0,  0.5,  1.0,  0.0,  0.0,  0.0,
     0.0,  0.0,  0.0,  0.5,  0.0,  0.0,
     0.0,  0.0,  0.0,  0.0,  3.5,  0.5,
     0.5,  0.0,  0.0,  0.5,  6.5, 10.0,
    17.0, 13.0,  4.0,  3.5, 24.5, 21.0,
    14.0, 12.5,  5.5, 11.5,  1.5,  1.5, 
    13.5, 11.0,  8.0,  9.5,  8.5, 17.0, 
    27.0, 26.0, 25.5, 23.0,  3.5,  1.0, 
     0.0,  0.0,  0.0,  0.0,  5.0, 17.5, 
     6.0,  2.5,  3.5,  4.0,  0.5,  0.5, 
     0.0,  3.0, 18.0,  4.0, 10.5,  8.5, 
    10.0,  3.0, 21.5,  2.0,  3.5, 19.0, 
     2.5,  4.5, 14.5, 12.0,  0.0,  0.0, 
     0.0,  0.0,  0.0,  0.0,  0.5,  0.0, 
     0.0,  0.0,  0.0,  0.0,  0.0,  2.0, 
     0.0,  0.0,  0.0,  0.5,  0.0,  0.0]
import pickle
f = open('prep144.txt', 'wb')
pickle.dump(prep144, f) #保存
acu144=[prep144[0]]
for i in range(1,144):
    acu144.append(prep144[i]+acu144[i-1])
print(acu144)
#-----------------------------------------------------------------------------------


#時間変数144までの順番の数
time = list(range(0, 144))
#print(time)

#開始時間終了時間の定義
s_time=6*3
e_time=6*27
print(str(s_time)+'~'+str(e_time))


#データーの読み込み-------------------------------------------------------------------------------------
#シェイドのための共通変数を定義
nl, sl, el, wl = 34.5, 32.5, 132, 130 #図示する範囲の設定
lev=np.arange(100, 1000, 100) #範囲の設定
variables='RAINNC'

#日本時間の24時時点で最大値の地点の24時間降水量の時間発展-----------------------------------------------
from matplotlib import colors
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.dates import DateFormatter
from matplotlib import colors

mp_k = ("WSM6","WSM6_h","WDM6","WDM6_h","WSM7","WDM7")
for mp in mp_k:
    print(mp)
    from netCDF4 import Dataset
    import os
    path="/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/late_run_041200/"+mp+"/"
    file="wrfout_d03_2017-07-04_12:00:00"
    is_file = os.path.isfile(path+file)

    if is_file:#パスにファイルが無ければ処理を飛ばす
        nc = Dataset(path+file, "r")
        nc_var=nc.variables.keys()
        if 'RAINNC'in nc_var:
            rainnc=nc.variables['RAINNC']
            print(rainnc)
            rainnc=rainnc[s_time:e_time,:,:]
            rainnc=rainnc-rainnc[0,:,:]
            lat_idx, lon_idx, = np.unravel_index(np.argmax(rainnc[-1,:,:]), rainnc[-1,:,:].shape)
            max=rainnc[:,lat_idx,lon_idx]
            print(max)
            # rainncのshadeの図----------------------------------------------------------
            for i in range(3,28):
                from shade import * #この事例のシェイドを描くための自作モジュール(読み込みながら図を描く)
                #rainncの図を描く
                title="rainnc"+file+"_"+str(i)
                name=mp+str(str(i-3).zfill(2))+".png"
                #name=path+"_"+str(i)+".png"
                shade(path+file,6*i,nl, sl, el, wl,lev,variables,title,name)
                plt.close()


            #度数分布のグラフ---------------------------------
            from matplotlib import colors
            import numpy as np
            import matplotlib.pyplot as plt
            from matplotlib import ticker
            from matplotlib.dates import DateFormatter
            fig = plt.figure()
            ax = fig.add_subplot()
            rainnc=rainnc[-1,:,:] #最後の時刻についての2次元の降水量
            rainnc=np.ravel(rainnc)
            #rainnc06.sort()#printで出力させるなら並べ替えた方が分かりやすい
            #print(rainnc06)
            plt.title(mp)
            plt.yscale("log")
            ax.set_xlim(0, 800)
            ax.set_ylim(1, 300000)
            ax.hist(rainnc, bins=16, histtype='barstacked', ec='black',range=(0,800))
            fig.savefig("frequency"+mp+".png", bbox_inches='tight', pad_inches=0.1)
 

#ax2.plot(time,ana_acu, label="RRAP")

#end---------------------------------------------------------------------------------------