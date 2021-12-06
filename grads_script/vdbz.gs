**全てリセット
'reinit'

**シュミレーション番号の選択
mp=26

**ファイルを開く
'open /home/nakamura_kento/wrf/work/TR_Nkyushu_20170705/late_run_041200/'mp'/0519JST.ctl'

**白くする
'set display color white'


**緯度経度高度の設定
'set lon 129.9 133.6'
**'set lat -6  -2'
'set z 0 40'

**シミュレーションの大まかな時間
hour = 10
minute=00
day=05
mon=07
year=2017
lati=33.4

**繰り返しの設定（無限レープ）
while (1<2)
'c'

**解析した時間,gradsを表示しない
'set timelab off'
'set grads off'


**時間、緯度の設定
'set time 'hour':'minute'Z'day''
**'set z 'height
'set lat 'lati


**レーダー反射強度
**'draw title WRF-dbz'
'color 0 60 5  -kind white-(0)->rainbow'
'set gxout shade2'
'd dbz'
'xcbar -line on -dir v'


**水平、鉛直風のベクトル
'set gxout vector'
'set arrlab off'
'd skip(u,50,1);w*5'


**上昇流を書く
**'set  gxout contour'
**'set  clevs  0.3'
**'set  ccolor 1'
**'set  clab  off'
**'d w'


**霰の密度を書く
**'set  gxout contour'
**'set  clevs  0.01'
**'set  ccolor 1'
**'set  clab  off'
**'d tc'

**文字を書く'
'set strsiz 0.1'
'draw string 7.0  8.3 '  'Time:'hour':'minute'Z'year''mon''day 
'draw string 9.0  8.3 '  'mp:'mp'  lat:'lati

**よくわからない
'run cbar.gs '

**コマンドに操作ガイド
say 'Choose (lat:k +1,m -1, No:n +1,b -1,s +6,r -6, Print+1:p, Quit:q,)'

**見る時間とかを変える
pull ans
if(ans = p)
'wi vdbz'mp'_'hour''minute'.png'
endif
if(ans = n)
minute = minute + 10
endif
if(ans = b)
minute = minute - 10
endif
if(ans = k)
lati = lati + 0.005
endif
if(ans = m)
lati = lati - 0.005
endif
if(ans = s)
hour = hour + 1
endif
if(ans = r)
hour = hour - 1
endif
if(ans = q)
exit
endif

endwhile


