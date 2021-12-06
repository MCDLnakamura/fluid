"""
wrfoutのnetcdf形式のファイルに自分で計算したarrayを新しいファイルに書き込む方法
追記の方法は分からなかったのでまた今度する

python tutorial の作成を待つ
"""
from netCDF4 import Dataset
import numpy as np

def dbz(path,name,idx_time,idx_eta,idx_lat,idx_lon,Times,XLAT,XLONG,ZNW,var):

    # オブジェクトを作成し，各次元数を設定します．

    nc = Dataset(path+name, 'w', format='NETCDF3_CLASSIC')
    nc.createDimension('ntime', idx_time)  # e.g. time_out = [0, 1, ...]
    #nc.createDimensions('ntime', None)        # unlimitedにする場合
    nc.createDimension('xi', idx_lon)
    nc.createDimension('yi', idx_lat)                 # e.g. x = 10
    nc.createDimension('eta', idx_eta)                

    # その後，各変数を定義します．
    # 以下の例では，時間，緯度，経度，3次元変数を定義します．

    Times = nc.createVariable('Times', dtype('int32').char, ('ntime',))

    XLAT = nc.createVariable('XLONG', dtype('double').float, ('eta', 'xi'))
    XLAT.long_name = 'east longitude'
    XLAT.units = 'degree of east longitude'

    XLAT = nc.createVariable('XLAT', dtype('double').float, ('eta', 'xi'))
    XLONG.long_name = 'north latitude'
    XLONG.units = 'degree of north latitude'

    ZNW = nc.createVariable('ZNW', dtype('double').float, ('eta', 'xi'))
    ZNW.long_name = 'north latitude'
    ZNW.units = 'degree of north latitude'    

    var = nc.createVariable('varname', dtype('double').float, ('ntime', 'eta', 'xi'))
    var.long_name = 'test variable'
    var.units = 'unit of test variable'

    # 最後に，予め np.ndarray 等で作成しておいた値を代入します．

    Times[:,:] = Times
    XLAT[:,:,:] = XLAT
    XLONG[:,:,:] = XLONG
    ZNW[:,:] = ZNW
    var[:,:,:,:] = var

    nc.close()
