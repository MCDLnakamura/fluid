**全てリセット
'reinit'

**ファイルを開く
'open mp06d03.ctl'

**白くする
'set display color white'
'c'

**地図の解像度を上げる
'set mpdset hires'

**緯度経度高度の設定
'set lon 130  132  '
'set lat 33   34   '



**解析した時間,gradsを表示しない
'set timelab off'
'set grads off'

**時間
hour = 06
minute=00
day=05
mon=07
year=2017



**24h降水量
'set time 15:00Z05 '
'prepa = rainnc+rainc'

'set time 15:00Z04 '
'prepb = rainnc+rainc'

'color 100 650 50  -kind white-(0)->rainbow'
'set gxout shade2'
'd prepa-prepb'
'xcbar -line on -dir v'

**朝倉に点を打つ
**'set line 0'
**'d mark (6, 130.695, 33.406, 1)'
**'draw mark 6  lon=130.695 lat=33.406 10'


**文字を書く
'set strsiz 0.1'
'draw string 7.0  8.3 '  'WSM6_15Z04-15Z05_'year''mon''day 
