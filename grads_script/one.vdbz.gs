**全てリセット
'reinit'

**シュミレーション番号の選択
mp=26

**ファイルを開く
'open /home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/late_run_041200/'mp'/0519JST.ctl'
**白くする
'set display color white'


**緯度経度高度の設定
'set z 1 40'


**解析した時間,gradsを表示しない
'set timelab off'
'set grads off'
'c'

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


**レーダー反射強度
'color 0 60 4  -kind white-(0)->rainbow'
'set gxout shade2'
'd dbz'
'xcbar -line on -dir v'


**水平、鉛直風のベクトル
'set gxout vector'
'set arrlab off'
'd skip(u,50,1);w*5'


**文字を書く'
'set strsiz 0.1'
**'draw string 5.0  8.3 '  'WSM7-dbz Time:'hour':'minute'Z'year''mon''day 
'draw string 9.0  8.3 '  'lat:'lati

**よくわからない
'run cbar.gs '

'wi 'mp'.png'
