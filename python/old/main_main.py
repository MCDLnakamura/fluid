"""
main_int.pyをmpで回しただけのプログラム
後で図を描く
"""

import os 
import numpy as np
from netCDF4 import Dataset

print("kaishi")

#自作モジュールのインポート
from main_int import *

results = []
mps = ("06h", "06g", "16h", "16g", "24", "26")
for imp in mps:
    print(imp)
    cors_int=cors_int(ims)
    np.save(imp+"cors_int",cors_int) #保存
    results.append(cors_int(imp))
    # cors_int(mps)

# print("06h")
# WSM6_h=cors_int("06h")
# print("06g")
# WSM6_g=cors_int("06g")
# print("16h")
# WDM6_h=cors_int("16h")
# print("16g")
# WDM6_g=cors_int("16g")
# print("24")
# WSM7  =cors_int("24")
# print("26")
# WDM7  =cors_int("26")

#恐らくここまで出来れば一旦ファイルが出来上がっているので図はすぐに描けるはず
