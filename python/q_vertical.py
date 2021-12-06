"""
それぞれのモデルの混合比の領域平均の鉛直プロファイルをプロット

11/26x軸の最大値を1.05に固定した
文字列のリストを作ってそれをforで回す方法に変更

11/27
保守の観点からconvec,stratiform,rain0を同一のこのファイルで行うことにした。
実行の際はif文の中の条件式とfig.saveing,titleのコメントアウトを変更する。
"""


print("kaishi")
criterion=("convective","stratiform","rain0")
criterion_number=2
creterion=criterion[criterion_number]

#モデル、時間、パスの指定
mp_k = ("WSM6","WSM6_h","WDM6","WDM6_h","WSM7","WDM7")
for mp in mp_k:
    print(mp)
    from netCDF4 import Dataset
    import numpy as np
    from matplotlib import colors
    import matplotlib.pyplot as plt
    import os
    #matplotlib.colors.cnames
    fig = plt.figure()
    fig, ax = plt.subplots()

    path="/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/late_run_041200/"+mp+"/"
    file="wrfout_d03_2017-07-04_12:00:00"
    time=6*22
    is_file = os.path.isfile(path+file)

    cors=np.load(path+"cors"+str(time)+".npy") #対流かどうかを読み込める
    #life_up=np.load(path+"life_up"+str(time)+".npy") #上昇流帯を読み込む
    #life_dw=np.load(path+"life_dw"+str(time)+".npy") #下降流帯を読み込む

    #print("up",np.count_nonzero(life_up==1))
    #print("dw",np.count_nonzero(life_dw==1))


    if is_file:#パスにファイルが無ければ処理を飛ばす
        nc = Dataset(path+file, "r")
        nc_var=nc.variables.keys()
        print(time)

        #時間の取得
        tmp = ""
        times = nc.variables["Times"]
        for i in times[time]:
            tmp += i.decode()

        #wrf.pythonを用いてz座標ごとの高度を得る
        from wrf import *
        z = getvar(nc, "z", units="m")
        z.to_masked_array()
        z=np.mean(z,axis=(1,2))[:]*0.001 #(kmにするために0.001をかける)
        print("z",z,)

        ###rainが(13)番目の層において0の地点は除外するようにする
        ##forとifで2重に囲んで探索する形にする 
        ##QVAPOR(Time, bottom_top, south_north, west_east)であることを考えて、
        z_cut=13 #番目(0インデックスだよ)
        qr=nc.variables['QRAIN']
        qrz=[]
        idx_time,idx_z,idx_y,idx_x=qr.shape
        

    else:#パスが通ってない場合には処理を終了する
        print("ファイルなし")
        exit()#プログラム終了

    p_k = ('QCLOUD','QRAIN','QICE','QSNOW','QGRAUP','QHAIL')
    for mp_i in p_k:
        print(mp_i)
        if mp_i in nc_var:
            q=nc.variables[mp_i]
            print(q)
            qz=[]
            for k in range(idx_z):
                qh=[]
                for i in range(idx_y):
                    for j in range(idx_x):
                        if (criterion_number==0) and (cors[z_cut,i,j]==1 or cors[z_cut,i,j]==2): #対流の有無
                            qh.append(q[time,k,i,j])
                        elif (criterion_number==1) and (cors[z_cut,i,j]==3): #層状の有無
                            qh.append(q[time,k,i,j])
                        elif (criterion_number==2) and (qr[time,z_cut,i,j]>0): #雨の有無
                            qh.append(q[time,k,i,j])
                qz.append(np.mean(qh)*1000)
            print(qz)
            ax.plot(qz,z, label=mp_i)

    #軸の最大値、最小値
    ax.set_xlim(-0.005, 1.05)
    ax.set_ylim(0, 18)

    #グラフタイトル
    plt.title("Averaged q-profile ("+mp+")"+criterion[criterion_number])

    #グラフの軸
    ax.set_xlabel('Mixing ratio (g/kg)')
    ax.set_ylabel('Height(km)')

    #グラフの凡例
    ax.legend()

    fig.savefig(mp+"_vq_"+tmp+"_"+criterion[criterion_number]+".png", bbox_inches='tight', pad_inches=0.1) 
    print('fig.saved')
    plt.close()
    plt.gca().clear()
    
    del qz, z, mp_i, qr, idx_time,idx_z,idx_y,idx_x, q


#end------------------------------------------------------------------------------------------------------------------

