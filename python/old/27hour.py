"""
gradsで出力した積算降水量の最大値をプロットしている
"""

from matplotlib import dates as mdates
from datetime import datetime as dt
import re

a=open('amedas.txt','r')


prep=[0,0,0,0,0,0,0,0,1.5,0.5,4.0,17.5,88.5,46.5,67.5,106,22.5,22.0,44.0,59,33.5,0.5,2.0,0.5]

time=[]
for i in range(24):
    time.append(i+1)

acu =[prep[0]]
for i in range(1,24):
    acu.append(prep[i]+acu[i-1])

#print(prep)
print(time)
print(acu)

#WSM6の積算降水量の取得
acu_sm6=[]
sm6=open('06.txt','r')
while True:
    data = sm6.readline()
    if data == '':
        break
    elif 'Min, Max = 0' in data: 
        acu_sm6.append(re.sub(r"[^\d.]", "", data[12:20]))
sm6.close()
#print(acu_sm6)
del acu_sm6[0:6*9]
del acu_sm6[6*33:6*36]
SM6=[]
for i in range(24):
    SM6.append(float(acu_sm6[i*6])-float(acu_sm6[6*9]))
print(SM6)

#WDM6の積算降水量の取得
acu_dm6=[]
dm6=open('16.txt','r')
while True:
    data = dm6.readline()
    if data == '':
        break
    elif 'Min, Max = 0' in data: 
        acu_dm6.append(re.sub(r"[^\d.]", "", data[12:20]))
dm6.close()
#print(acu_dm6)
del acu_dm6[0:6*9]
del acu_dm6[6*33:6*36]
DM6=[]
for i in range(24):
    DM6.append(float(acu_dm6[i*6])-float(acu_dm6[6*9]))
print(DM6)

#WSM7の積算降水量の取得
acu_sm7=[]
sm7=open('24.txt','r')
while True:
    data = sm7.readline()
    if data == '':
        break
    elif 'Min, Max = 0' in data: 
        acu_sm7.append(re.sub(r"[^\d.]", "", data[12:20]))
sm7.close()
#print(acu_sm7)
del acu_sm7[0:6*9]
del acu_sm7[6*33:6*36]
SM7=[]
for i in range(24):
    SM7.append(float(acu_sm7[i*6])-float(acu_sm7[6*9]))
print(SM7)

#WDM7の積算降水量の取得
acu_dm7=[]
dm7=open('26.txt','r')
while True:
    data = dm7.readline()
    if data == '':
        break
    elif 'Min, Max = 0' in data: 
        acu_dm7.append(re.sub(r"[^\d.]", "", data[12:20]))
dm7.close()
#print(acu_dm7)
del acu_dm7[0:6*9]
del acu_dm7[6*33:6*36]
DM7=[]
for i in range(24):
    DM7.append(float(acu_dm7[i*6])-float(acu_dm7[6*9]))
print(DM7)

from matplotlib import colors
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.dates import DateFormatter
fig = plt.figure()
fig, ax = plt.subplots()
ax2 = ax.twinx()

#軸の最大値、最小値
ax.set_xlim(0, 24)
#ax.set_ylim(0, 120)

# x軸の目盛設定
ax.set_xticks([0,3,6,9,12,15,18,21,24])

#グラフタイトル
plt.title('precipitation')

#グラフの軸
ax.set_xlabel('Time 7/5 (JST)')
ax.set_ylabel('Hourly Rainfall(mm)')

#プロット
ax.bar(time, prep, width=0.3, color="blue")
ax2.plot(time,acu, label="amedas", color="black")
ax2.plot(time,SM6, label="WSM6")
ax2.plot(time,DM6, label="WDM6")
ax2.plot(time,SM7, label="WSM7")
ax2.plot(time,DM7, label="WDM7")

#グラフの凡例
ax2.legend()

fig.savefig("hour.png")