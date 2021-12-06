"""
wrfoutからshadeをプロットするモジュール

"""
from netCDF4 import *
from wrf import *
import numpy as np

from matplotlib.colors import *
from matplotlib.dates import *
from matplotlib.ticker import *
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.cm as cm
import matplotlib.ticker as mticker
fig = plt.figure()
fig, ax = plt.subplots()

def shade(path,time,nl, sl, el, wl,lev,variables,title,name):
    

    nc = Dataset(path, "r")
    nc_var=nc.variables.keys()

    #latとlonはいつでも同じなので定数として扱って問題ない--------------------------------------------------------
    lat = nc.variables["XLAT"]
    lat = lat[time,:,:]
    lon = nc.variables["XLONG"]
    lon = lon[time,:,:]
    #--------------------------------------------------------------------------------------------------------

    #wrf.vertcross(field3d, vert, levels=None, missing=<MagicMock name='mock().item()' id='139691447841424'>, wrfin=None, timeidx=0, stagger=None, projection=None, ll_point=None, pivot_point=None, angle=None, start_point=None, end_point=None, latlon=False, autolevels=100, cache=None, meta=True)
    #を使うころで2点間の鉛直断面の絵を書くことが出来る

    a=wrf.vertcross("dbz", "z", levels=None, wrfin=None, timeidx=0, stagger=None, projection=None, ll_point=None, pivot_point=None, angle=None, start_point=None, end_point=None, latlon=False, autolevels=100, cache=None, meta=True)

    # 描画部分---------------------------------------------------------------------------------------------------
    #各種指定
    fontsize = 5
    #nl, sl, el, wl = 34.5, 32.5, 132, 130 #図示する範囲の設定

   #図の大きさを決める
    fig = plt.figure(figsize=(4, 4))
    fig.subplots_adjust(right=0.85)#右に隙間を空ける(多分)
    ax = fig.add_subplot(1, 1, 1)

    #海岸線を描く
    ax.coastlines(linewidths=0.3, zorder=0) 
    #ax.stock_img() # 陸海を表示

    #決めた角度ごとに線を引く
    angle=0.25
    xticks = np.arange(0, 360.1, angle)
    yticks = np.arange(-90, 90.1, angle)
    ax.set_xticks(xticks, crs=proj)
    ax.set_yticks(yticks, crs=proj)

    ax.xaxis.set_major_formatter(LongitudeFormatter(zero_direction_label=True))
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    ax.xaxis.set_minor_locator(MultipleLocator(2.5))
    ax.yaxis.set_minor_locator(MultipleLocator(2.5))
    #緯度経度の範囲設定
    ax.set_extent([wl, el, sl, nl], crs=ccrs.PlateCarree())

    ax.tick_params(direction='out', length=3, width=0.7, colors='k',grid_color='k', grid_alpha=0.5, labelsize=fontsize)
    ax.tick_params(which='minor', axis='x', length=2, color='k')
    ax.tick_params(which='minor', axis='y', length=2, color='k')

    gl = ax.gridlines(draw_labels=False, linewidth=0.5, linestyle='--', color='gray', alpha=0.5)
    gl.xlocator = FixedLocator(xticks) # 経度線を描く値
    gl.ylocator = FixedLocator(yticks) # 緯度線を描く値

    #lev=np.arange(100, 1000, 100) #範囲の設定
    #シェイドを描く
    shade_plot = ax.contourf(lon,lat,shade,levels=lev, cmap=cm.jet)
    #その他のオプション ,zorder=0,corner_mask=True, alpha=1, cmap=newcmp
    #ax.clabel(shade_plot,fmt='%d',inline=True, fontsize=5,colors='black', zorder=1,) # 等値線のラベルを付ける


    #カラーバーを描く
    cax = ax.inset_axes([1.04, 0.3, 0.03, 0.4], transform=ax.transAxes)#cbarの座標
    cbar = plt.colorbar(shade_plot, cax = cax, orientation='vertical',extendfrac = 'auto', ticks=lev )
    cbar.ax.tick_params(labelsize=fontsize)


    #ax.gridlines()#グリッドの表示
    #title="rainnc"
    ax.set_title(title,  fontsize=fontsize)#タイトルの表示


    #図の保存(解像度等も指定できる)
    fig.savefig(name, dpi=250, bbox_inches='tight', pad_inches=0.1)
    print('save.fig')
    plt.gca().clear()
    plt.close()
    #----------------------------------------------------------------------------------------------------------------
