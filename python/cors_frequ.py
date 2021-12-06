import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt
fig = plt.figure()
fig, ax = plt.subplots()
time=6*22

height1 = []  
height2 = [] 
mp=("WSM6","WSM6_h","WDM6","WDM6_h","WSM7","WDM7")
for mp_i in mp:
    print(mp_i)
    path="/home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/late_run_041200/"+mp_i+"/"
    cors=np.load(path+"cors"+str(time)+".npy") #読み込める
    l=np.count_nonzero(cors==1)+np.count_nonzero(cors==2)
    height1.append(l)
    r=np.count_nonzero(cors==3)
    height2.append(r)

#度数分布のグラフを描く----------------------------------------------------------------------------
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
fig.savefig("cors_fre", dpi=500, bbox_inches='tight', pad_inches=0.1)
print('save.fig')
plt.gca().clear()
plt.close()

#-----------------------------------------------------------------------------------------