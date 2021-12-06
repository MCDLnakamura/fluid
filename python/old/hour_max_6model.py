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
"""




#処理の開始時刻を表示させる(分かりやすくするためであって、特に意味はない)---------------------------------
from datetime import datetime 
dt_now = datetime.now()
print(dt_now)

import numpy as np
import re
import os
import subprocess

#20170705(JST)の時間ごとの降水量の観測地(朝倉のアメダス)
prep=[0,0,0,0,0,0,0,0,1.5,0.5,4.0,17.5,88.5,46.5,67.5,106,22.5,22.0,44.0,59,33.5,0.5,2.0,0.5]

#時間単位のものを10分単位で出力しなおす
prep144=[]
for i in range(24):
    for j in range(6):
        prep144.append(prep[i])
print(prep144)


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

"""
#20170705(JST)の10分ごとの降水量のベタ打ち
#確認しなおしてから使う
prep144=[
    0,0,0,0,0,0,
    0,0,0,0,0,0,
    0,0,0,0,0,0,
    0,0,0,0,0,0,
    0,0,0,0,0,0,
    0,0,0,0,0,0,
    0,0,0,0,0,0,
    0,0,0,0,0,0,
     0.0,  5.0,  1.0,  0.0,  0.0,  0.0,
     0.0,  0.0,  0.0,  0.5,  0.0,  0.0,
     0.0,  0.0,  0.0,  0.0,  0.5,  0.5,
     0.5,  0.0,  0.0,  0.5,  0.5, 10.0,
    17.0, 13.0,  0.0,  0.5, 24.0, 21.0,
    14.0, 12.0,  0.5, 11.0,  0.5,  0.5, 
    13.0, 11.0,  0.0,  0.5,  0.5, 17.0, 
    27.0, 26.0, 25.0, 23.0,  0.5,  0.0, 
     0.0,  0.0,  0.0,  0.0,  0.0, 17.0, 
     0.0,  0.5,  0.5,  0.0,  0.5,  0.5, 
     0.0,  0.0, 18.0,  0.0, 10.0,  0.5, 
    10.0,  0.0, 21.0,  0.0,  0.5, 19.0, 
     0.5,  0.5, 14.0, 12.0,  0.0,  0.0, 
     0.0,  0.0,  0.0,  0.0,  0.5,  0.0, 
     0.0,  0.0,  0.0,  0.0,  0.0,  0.0, 
     0.0,  0.0,  0.0,  0.5,  0.0,  0.0]

acu144=[prep144[0]]
for i in range(1,144):
    acu144.append(prep144[i]+acu144[i-1])
print(acu144)

"""

#時間変数144までの順番の数
time=[]
for i in range(144):
    time.append(i+1)
#print(time)

#上で入力した数の和
acu =[prep[0]]
for i in range(1,24):
    acu.append(prep[i]+acu[i-1])

#144個に直す
acu144=[]
for i in range(24):
    for j in range(6):
        acu144.append(acu[i])

#開始時間終了時間の定義
s_time=6*3
e_time=6*27
print(str(s_time)+'~'+str(e_time))




#データーの読み込み-------------------------------------------------------------------------------------
from netCDF4 import Dataset

from shade import * #この事例のシェイドを描くための自作モジュール(読み込みながら図を描く)
#シェイドのための共通変数を定義
nl, sl, el, wl = 34.5, 32.5, 132, 130 #図示する範囲の設定
lev=np.arange(100, 1000, 100) #範囲の設定
variables='RAINNC'

import matplotlib.pyplot as plt
#1モデル目
path="06h/wrfout_d03_2017-07-04_12:00:00"
is_file = os.path.isfile(path)
if is_file:#パスにファイルが無ければ処理を飛ばす
    nc = Dataset(path, "r")
    nc_var=nc.variables.keys()
    if 'RAINNC'in nc_var:
        rainnc=nc.variables['RAINNC']
        print(rainnc)
        # print(type(rainnc[:]))
        rainnc=rainnc[s_time:e_time,:,:]
        # print(type(rainnc))
        rainnc=rainnc-rainnc[0,:,:]
        lat_idx, lon_idx, = np.unravel_index(np.argmax(rainnc[-1,:,:]), rainnc[-1,:,:].shape)
        max_06_h=rainnc[:,lat_idx,lon_idx]
        print(max_06_h)
        
        acu_sum_06_h=np.mean(rainnc, axis=(1,2))#積算降水量の領域平均の時間発展の配列

        rainnc06_h=rainnc[-1,:,:] #度数分布のための配列の為にメモリーに保存させる
        
        for i in range(3,28):
            #rainncの図を描く
            title="rainnc"+path+"_"+str(i)
            name="06h"+str(str(i-3).zfill(2))+".png"
            #name=path+"_"+str(i)+".png"
            shade(path,6*i,nl, sl, el, wl,lev,variables,title,name)
            plt.close()
        
        del nc, rainnc, lat_idx, lon_idx #念のため変数の中身を削除する




#2モデル目
path="06g/wrfout_d03_2017-07-04_12:00:00"
is_file = os.path.isfile(path)
if is_file:#パスにファイルが無ければ処理を飛ばす
    nc = Dataset(path, "r")
    nc_var=nc.variables.keys()
    if 'RAINNC'in nc_var:
        rainnc=nc.variables['RAINNC']
        print(rainnc)
        rainnc=rainnc[s_time:e_time,:,:]
        rainnc=rainnc-rainnc[0,:,:]
        lat_idx, lon_idx, = np.unravel_index(np.argmax(rainnc[-1,:,:]), rainnc[-1,:,:].shape)
        max_06_g=rainnc[:,lat_idx,lon_idx]
        
        acu_sum_06_g=np.mean(rainnc, axis=(1,2))#積算降水量の領域平均の時間発展の配列

        rainnc06_g=rainnc[-1,:,:] #度数分布のための配列の為にメモリーに保存させる

       
        for i in range(3,28):
            #rainncの図を描く
            title="rainnc"+path+"_"+str(i)
            name="06g"+str(str(i-3).zfill(2))+".png"
            shade(path,6*i,nl, sl, el, wl,lev,variables,title,name)
            plt.close()

        del nc, rainnc, lat_idx, lon_idx #念のため変数の中身を削除する

#3モデル目
path="16h/wrfout_d03_2017-07-04_12:00:00"
is_file = os.path.isfile(path)
if is_file:#パスにファイルが無ければ処理を飛ばす
    nc = Dataset(path, "r")
    nc_var=nc.variables.keys()
    if 'RAINNC'in nc_var:
        rainnc=nc.variables['RAINNC']
        print(rainnc)
        rainnc=rainnc[s_time:e_time,:,:]
        rainnc=rainnc-rainnc[0,:,:]    
        lat_idx, lon_idx, = np.unravel_index(np.argmax(rainnc[-1,:,:]), rainnc[-1,:,:].shape)
        max_16_h=rainnc[:,lat_idx,lon_idx]
        print(max_16_h)

        acu_sum_16_h=np.mean(rainnc, axis=(1,2))#積算降水量の領域平均の時間発展の配列

        rainnc16_h=rainnc[-1,:,:] #度数分布のための配列の為にメモリーに保存させる

        for i in range(3,28):
            #rainncの図を描く
            title="rainnc"+path+"_"+str(i)
            name="16h"+str(str(i-3).zfill(2))+".png"
            shade(path,6*i,nl, sl, el, wl,lev,variables,title,name)
            plt.close()

        del nc, rainnc, lat_idx, lon_idx #念のため変数の中身を削除する

#4モデル目
path="16g/wrfout_d03_2017-07-04_12:00:00"
is_file = os.path.isfile(path)
if is_file:#パスにファイルが無ければ処理を飛ばす
    nc = Dataset(path, "r")
    nc_var=nc.variables.keys()
    if 'RAINNC'in nc_var:
        rainnc=nc.variables['RAINNC']
        print(rainnc)
        rainnc=rainnc[s_time:e_time,:,:]
        rainnc=rainnc-rainnc[0,:,:]    
        lat_idx, lon_idx, = np.unravel_index(np.argmax(rainnc[-1,:,:]), rainnc[-1,:,:].shape)
        max_16_g=rainnc[:,lat_idx,lon_idx]
        print(max_16_g)

        acu_sum_16_g=np.mean(rainnc, axis=(1,2))#積算降水量の領域平均の時間発展の配列

        rainnc16_g=rainnc[-1,:,:] #度数分布のための配列の為にメモリーに保存させる

        for i in range(3,28):
            #rainncの図を描く
            title="rainnc"+path+"_"+str(i)
            name="16g"+str(str(i-3).zfill(2))+".png"
            shade(path,6*i,nl, sl, el, wl,lev,variables,title,name)
            plt.close()

        del nc, rainnc, lat_idx, lon_idx #念のため変数の中身を削除する


#5モデル目
path="24/wrfout_d03_2017-07-04_12:00:00"
is_file = os.path.isfile(path)
if is_file:#パスにファイルが無ければ処理を飛ばす
    nc = Dataset(path, "r")
    nc_var=nc.variables.keys()
    if 'RAINNC'in nc_var:
        rainnc=nc.variables['RAINNC']
        print(rainnc)
        rainnc=rainnc[s_time:e_time,:,:]
        rainnc=rainnc-rainnc[0,:,:]
        lat_idx, lon_idx, = np.unravel_index(np.argmax(rainnc[-1,:,:]), rainnc[-1,:,:].shape)
        max_24=rainnc[:,lat_idx,lon_idx]
        print(max_24)

        acu_sum_24=np.mean(rainnc, axis=(1,2))#積算降水量の領域平均の時間発展の配列

        rainnc24=rainnc[-1,:,:] #度数分布のための配列の為にメモリーに保存させる

        for i in range(3,28):
            #rainncの図を描く
            title="rainnc"+path+"_"+str(i)
            name="24"+str(str(i-3).zfill(2))+".png"
            #name=path+"_"+str(i)+".png"
            shade(path,6*i,nl, sl, el, wl,lev,variables,title,name)
            plt.close()

        del nc, rainnc, lat_idx, lon_idx #念のため変数の中身を削除する


#6モデル目
path="26/wrfout_d03_2017-07-04_12:00:00"
is_file = os.path.isfile(path)
if is_file:#パスにファイルが無ければ処理を飛ばす
    nc = Dataset(path, "r")
    nc_var=nc.variables.keys()
    if 'RAINNC'in nc_var:
        rainnc=nc.variables['RAINNC']
        print(rainnc)
        rainnc=rainnc[s_time:e_time,:,:]
        rainnc=rainnc-rainnc[0,:,:]
        lat_idx, lon_idx, = np.unravel_index(np.argmax(rainnc[-1,:,:]), rainnc[-1,:,:].shape)
        max_26=rainnc[:,lat_idx,lon_idx]
        print(max_26)

        acu_sum_26=np.mean(rainnc, axis=(1,2))#積算降水量の領域平均の時間発展の配列

        rainnc26=rainnc[-1,:,:] #度数分布のための配列の為にメモリーに保存させる

        for i in range(3,28):
            #rainncの図を描く
            title="rainnc"+path+"_"+str(i)
            name="26"+str(str(i-3).zfill(2))+".png"
            #name=path+"_"+str(i)+".png"
            shade(path,6*i,nl, sl, el, wl,lev,variables,title,name)
            plt.close()

        del nc, rainnc, lat_idx, lon_idx #念のため変数の中身を削除する


#図のためのモジュール--------------------------------------------------------------------------------
from matplotlib import colors
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.dates import DateFormatter
fig = plt.figure()
fig, ax = plt.subplots()
ax2 = ax.twinx()


#日本時間の24時時点で最大値の地点の24時間降水量の時間発展-----------------------------------------------

#軸の最大値、最小値
ax.set_xlim(0, 24*6)
ax.set_ylim(0, 200)
ax2.set_ylim(0, 800)

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
"""
prep144_kai=[]
for n in prep144:
    prep144_kai.append(n*6)
"""
ax.bar(time, prep144, width=1, color="blue")
ax2.plot(time,acu144, label="amedas(asakura)", color="black")
if 'max_06_h' in globals() or 'max_06_h' in locals():#変数が無い場合は処理を行わない
    ax2.plot(time,max_06_h, label="WSM6-hail max")
if 'max_06_g' in globals() or 'max_06_g' in locals():#変数が無い場合は処理を行わない
    ax2.plot(time,max_06_g, label="WSM6-graupel max")
if 'max_16_h' in globals() or 'max_16_h' in locals():#変数が無い場合は処理を行わない
    ax2.plot(time,max_16_h, label="WDM6-hail max")
if 'max_16_g' in globals() or 'max_16_g' in locals():#変数が無い場合は処理を行わない
    ax2.plot(time,max_16_g, label="WDM6-graupel max")
if 'max_24' in globals() or 'max_24' in locals():#変数が無い場合は処理を行わない
    ax2.plot(time,max_24, label="WSM7 max")
if 'max_26' in globals() or 'max_26' in locals():#変数が無い場合は処理を行わない
    ax2.plot(time,max_26, label="WDM7 max")

#ax2.plot(time,ana_acu, label="RRAP")

#グラフの凡例
ax2.legend()

fig.savefig("hour_maxpoint.png")

#書いたグラフの削除

plt.close()
#------------------------------------------------------------------------------------------------



#度数分布のグラフを描く----------------------------------------------------------------------------
#WSM6_hail
import matplotlib.pyplot as plt
fig = plt.figure()
fig, ax = plt.subplots()
if 'rainnc06_h' in globals() or 'rainnc06_h' in locals():#変数が無い場合は処理を行わない
    rainnc06_h=np.ravel(rainnc06_h)
    #rainnc06.sort()#printで出力させるなら並べ替えた方が分かりやすい
    #print(rainnc06)
    plt.title('WSM6_hail')
    plt.yscale("log")
    ax.set_xlim(0, 800)
    ax.set_ylim(1, 300000)
    ax.hist(rainnc06_h, bins=16, histtype='barstacked', ec='black',range=(0,800))
    fig.savefig("frequency06_h.png")
    
plt.close()
import matplotlib.pyplot as plt
fig = plt.figure()
fig, ax = plt.subplots()
#WSM6_graupel
if 'rainnc06_g' in globals() or 'rainnc06_g' in locals():#変数が無い場合は処理を行わない
    rainnc06_g=np.ravel(rainnc06_g)
    #rainnc06.sort()#printで出力させるなら並べ替えた方が分かりやすい
    #print(rainnc06)
    plt.title('WSM6_graupel')
    plt.yscale("log")
    ax.set_xlim(0, 800)
    ax.set_ylim(1, 300000)
    ax.hist(rainnc06_g, bins=16, histtype='barstacked', ec='black',range=(0,800))
    fig.savefig("frequency06_g.png")
    
plt.close()
import matplotlib.pyplot as plt
fig = plt.figure()
fig, ax = plt.subplots()
#WDM6_hail
if 'rainnc16_h' in globals() or 'rainnc16_h' in locals():#変数が無い場合は処理を行わない
    rainnc16_h=np.ravel(rainnc16_h)
    #rainnc16.sort()#printで出力させるなら並べ替えた方が分かりやすい
    #print(rainnc16)
    plt.title('WDM6_hail')
    plt.yscale("log")
    ax.set_xlim(0, 800)
    ax.set_ylim(1, 300000)
    ax.hist(rainnc16_h, bins=16, histtype='barstacked', ec='black',range=(0,800))
    fig.savefig("frequency16_h.png")
    
plt.close()
import matplotlib.pyplot as plt
fig = plt.figure()
fig, ax = plt.subplots()
#WDM6_graupel
if 'rainnc16_g' in globals() or 'rainnc16_g' in locals():#変数が無い場合は処理を行わない
    rainnc16_g=np.ravel(rainnc16_g)
    #rainnc16.sort()#printで出力させるなら並べ替えた方が分かりやすい
    #print(rainnc16)
    plt.title('WDM6_graupel')
    plt.yscale("log")
    ax.set_xlim(0, 800)
    ax.set_ylim(1, 300000)
    ax.hist(rainnc16_g, bins=16, histtype='barstacked', ec='black',range=(0,800))
    fig.savefig("frequency16_g.png")
    
plt.close()
import matplotlib.pyplot as plt
fig = plt.figure()
fig, ax = plt.subplots()
#WSM7
if 'rainnc24' in globals() or 'rainnc24' in locals():#変数が無い場合は処理を行わない
    rainnc24=np.ravel(rainnc24)
    #rainnc24.sort()#printで出力させるなら並べ替えた方が分かりやすい
    #print(rainnc24)
    plt.title('WSM7')
    plt.yscale("log")
    ax.set_xlim(0, 800)
    ax.set_ylim(1, 300000)
    ax.hist(rainnc24, bins=16, histtype='barstacked', ec='black',range=(0,800))
    fig.savefig("frequency24.png")
    
plt.close()
import matplotlib.pyplot as plt
fig = plt.figure()
fig, ax = plt.subplots()
#WDM7
if 'rainnc26' in globals() or 'rainnc26' in locals():#変数が無い場合は処理を行わない
    rainnc26=np.ravel(rainnc26)
    #rainnc26.sort()#printで出力させるなら並べ替えた方が分かりやすい
    #print(rainnc26)
    plt.title('WDM7')
    plt.yscale("log")
    ax.set_xlim(0, 800)
    ax.set_ylim(1, 300000)
    ax.hist(rainnc26, bins=16, histtype='barstacked', ec='black',range=(0,800))
    fig.savefig("frequency26.png")
    
plt.close()

#---------------------------------------------------------------------------------------------------------------


#積算降水量の領域平均を計算して時系列でプロットする----------------------------------------------------------------
#範囲を絞ったほうがいいとの指摘を受けている
#acu_sum_06_h=np.mean(rainnc, axis=(1,2))#積算降水量の領域平均の時間発展の配列--のように書いた
import matplotlib.pyplot as plt
fig = plt.figure()
fig, ax = plt.subplots()
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
if 'acu_sum_06_h' in globals() or 'acu_sum_06_h' in locals():#変数が無い場合は処理を行わない
    ax.plot(time,acu_sum_06_h, label="WSM6_hail")
if 'acu_sum_06_g' in globals() or 'acu_sum_06_g' in locals():#変数が無い場合は処理を行わない    
    ax.plot(time,acu_sum_06_g, label="WSM6_graupel")
if 'acu_sum_16_h' in globals() or 'acu_sum_16_h' in locals():#変数が無い場合は処理を行わない
    ax.plot(time,acu_sum_16_h, label="WDM6_hail")
if 'acu_sum_16_g' in globals() or 'acu_sum_16_g' in locals():#変数が無い場合は処理を行わない
    ax.plot(time,acu_sum_16_g, label="WDM6_graupel")
if 'acu_sum_24' in globals() or 'acu_sum_24' in locals():#変数が無い場合は処理を行わない
    ax.plot(time,acu_sum_24, label="WSM7")
if 'acu_sum_26' in globals() or 'acu_sum_26' in locals():#変数が無い場合は処理を行わない
    ax.plot(time,acu_sum_26, label="WDM7")
#ax.plot(time,acu_kai,label="OBS")

#グラフの凡例
ax.legend()

fig.savefig("hour_all.png")

plt.close()

#-----------------------------------------------------------------------------------------------------------------