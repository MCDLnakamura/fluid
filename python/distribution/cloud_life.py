"""
Steinerの手法を用いて判別した対流域に対して、さらに上昇速度の鉛直分布によって発達期､成熟期､衰退期に区別するモジュール
ある対流域のグリッドの上昇速度の鉛直分布より、上昇速度が閾値を超えた層の厚さが1.5km以上のときに上昇流（下降流）があると判断する。閾値は1.0m/sと-0.5m/sである。
上昇流と下降流の有無によってグリッドのライフステージを決定する。
上昇のみは発達期
下降は衰退期
両方は成熟期
どちらにも当てはまらないものは考えない

今までのは汎用性が高かったがこのモジュールは高度をベタ打ちしていて、40層のこのモデルのみで有効な形である。

また、現段階ではcorsを用いて条件を絞っていないため、対流雲以外の場所の上昇下降もカウントしている可能性が有るため、この点には注意すること。
"""
from netCDF4 import Dataset
import numpy as np
from wrf import *
def life(path,time,cors):
    w_max=1.0#上昇流の閾値
    w_min=-0.5#下降流の閾値
    
    nc = Dataset(path, "r")
    w=nc.variables['W'][time]
    w=w[0:-1,:,:]
    
    #wrf.pythonを用いてz座標ごとの高度を得る
    
    nc = Dataset(path, "r")
    nc_var=nc.variables.keys()
    z = getvar(nc, "z", units="m")
    z.to_masked_array()
    z=np.mean(z,axis=(1,2))[:]*0.001
    print(z)
    """
    変数"W"の情報
    float W(Time, bottom_top_stag, south_north, west_east) ;
    W:FieldType = 104 ;
    W:MemoryOrder = "XYZ" ;
    W:description = "z-wind component" ;
    W:units = "m s-1" ;
    W:stagger = "Z" ;
    W:coordinates = "XLONG XLAT XTIME" ;
    """

    #もし形が適合しなければ処理を終了する
    if cors.shape != w.shape:
        print("cors",cors.shape)
        print("w",w.shape)
        print("different shape")
        exit()#プログラム終了)

    idx_eta,idx_lat,idx_lon=cors.shape
    #初期値
    #空の配列を作っておく
    #life=np.empty((idx_eta,idx_lat,idx_lon))
    life_up=np.zeros((idx_lat,idx_lon))
    life_dw=np.zeros((idx_lat,idx_lon))
    for i in range(idx_lat):
        for j in range(idx_lon):
            bot_up=0
            bot_dw=0
            top_up=0
            top_dw=0            
            for k in range(idx_eta-1):
                #上昇流の判定
                if w[k,i,j]>=w_max:
                    if w[k+1,i,j]<w_max:
                        top_up=k
                elif w[k+1,i,j]>=w_max:
                    #上昇流が当てはまらない無い場合に次の層が上昇流だったら底を定義しなおす
                    bot_up=k+1

                #下降流の判定
                if w[k,i,j]<=w_min:
                    if w[k+1,i,j]>w_max:
                        top_dw=k
                elif w[k+1,i,j]<=w_min:
                    #下降流が当てはまらない無い場合に次の層が上昇流だったら底を定義しなおす
                    bot_dw=k+1

                #条件に適合する場合は変数を書き換える        
                if z[top_up]-z[bot_up]>1.5:
                    #上昇帯がある場合は1(True)にする
                    np.put(life_up, [i,j], 1)
                if z[top_dw]-z[bot_dw]>1.5:
                    #下降帯がある場合は1(True)にする
                    np.put(life_dw, [i,j], 1)
    return life_up, life_dw
    #それぞれ別の値として返す。このため返り値が2つあることに注意すること
                    
                

                