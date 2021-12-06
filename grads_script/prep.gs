**全てリセット
'reinit'

**ファイルを開く
'open /home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/wrfout40s/16/16d03.ctl'

**白くする
'set display color white'

**地図の解像度を上げる
'set mpdset hires'

**緯度経度高度の設定
*'set lon 130 132'
*'set lat 33  34'

'c'
**解析した時間,gradsを表示しない
'set timelab off'
'set grads off'

**時間
year=2017
mon=jul
day=05
hour=15
minute=00

**降水量
'set time 'hour':'minute'Z05'mon year
'prepa = rainnc +rainc'

'set time 'hour-1':'minute'Z05'mon year
'prepb = rainnc +rainc'

'color 10 100 10  -kind white-(0)->rainbow'
'set gxout shade2'
'd prepa - prepb'
'xcbar -line on -dir v'


**文字を書く
'set strsiz 0.1'
'draw string 7.0  8.3 '  'Time:'hour':'minute'Z'day''mon'' year
