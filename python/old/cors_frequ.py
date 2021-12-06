import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt
fig = plt.figure()
fig, ax = plt.subplots()
time=6*22

#dbz=np.load(path+"dbz"+str(time)+".npy") #読み込める
mp="06h"
path="/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/late_run_041200/"+mp+"/"
cors=np.load(path+"cors"+str(time)+".npy") #読み込める
l_06h=np.count_nonzero(cors==1)+np.count_nonzero(cors==2)
r_06h=np.count_nonzero(cors==3)

mp="06g"
path="/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/late_run_041200/"+mp+"/"
cors=np.load(path+"cors"+str(time)+".npy") #読み込める
l_06g=np.count_nonzero(cors==1)+np.count_nonzero(cors==2)
r_06g=np.count_nonzero(cors==3)

mp="16h"
path="/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/late_run_041200/"+mp+"/"
cors=np.load(path+"cors"+str(time)+".npy") #読み込める
l_16h=np.count_nonzero(cors==1)+np.count_nonzero(cors==2)
r_16h=np.count_nonzero(cors==3)

mp="16g"
path="/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/late_run_041200/"+mp+"/"
cors=np.load(path+"cors"+str(time)+".npy") #読み込める
l_16g=np.count_nonzero(cors==1)+np.count_nonzero(cors==2)
r_16g=np.count_nonzero(cors==3)

mp="24"
path="/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/late_run_041200/"+mp+"/"
cors=np.load(path+"cors"+str(time)+".npy") #読み込める
l_24=np.count_nonzero(cors==1)+np.count_nonzero(cors==2)
r_24=np.count_nonzero(cors==3)

mp="26"
path="/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/late_run_041200/"+mp+"/"
cors=np.load(path+"cors"+str(time)+".npy") #読み込める
l_26=np.count_nonzero(cors==1)+np.count_nonzero(cors==2)
r_26=np.count_nonzero(cors==3)

#print("0",np.count_nonzero(cors==0))
#print("1",np.count_nonzero(cors==1))
#print("2",np.count_nonzero(cors==2))
#print("3",np.count_nonzero(cors==3))

#度数分布のグラフを描く----------------------------------------------------------------------------
height1 = [l_06h, l_06g, l_16h, l_16g, l_24, l_26]  
height2 = [r_06h, r_06g, r_16h, r_16g, r_24, r_26]   
 
left = np.arange(len(height1))  # numpyで横軸を設定
labels = ['WSM6-h', 'WSM6-g', 'WDM6-h', 'WDM6-g', 'WSM7', 'WDM7']
 
width = 0.3
 
plt.bar(left, height1, color='r', width=width, align='center', label="convectinve")
plt.bar(left+width, height2, color='b', width=width, align='center' ,label="stratiform")
 
plt.xticks(left + width/2, labels)

title="cors"+str(time)
ax.set_title(title,  fontsize=10)#タイトルの表示
ax.legend(loc="best", fontsize=8)



#図の保存(解像度等も指定できる)
fig.savefig("cors_fre", dpi=500)
print('save.fig')
plt.gca().clear()
plt.close()

#-----------------------------------------------------------------------------------------