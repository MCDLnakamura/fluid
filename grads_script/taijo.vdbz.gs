**全てリセット
'reinit'

**ファイルを開く
'open mp26d03.ctl'

**白くする
'set display color white'


**緯度経度高度の設定
'set z 1 40'


**解析した時間,gradsを表示しない
'c'
'set timelab off'
'set grads off'


**シミュレーションの大まかな時間
hour = 10
minute=00
day=05
mon=07
year=2017
lati=33.38


**時間、緯度の設定
'set time 'hour':'minute'Z'day''
**'set z 'height
'set lat ' lati
'set lon 129.5 133.5'

**レーダー反射強度
'color 5 60 5  -kind white-(0)->rainbow'
'set gxout shade2'
'd ave(dbz, lat=33 ,lat=33.39 )'
'xcbar -line on -dir v'


**水平、鉛直風のベクトル
**'set gxout vector'
**'set arrlab off'
**'d skip(u,50,1);w*5'


**文字を書く'
'set strsiz 0.1'
'draw string 5.0  8.3 '  'WDM7-dbz-33.35_33.55 Time:'hour':'minute'Z'year''mon''day 
**'draw string 9.0  8.3 '  'lat:'lati

**よくわからない
'run cbar.gs '
