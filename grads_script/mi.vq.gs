**全てリセット
'reinit'

**ファイルの保存場所(よくわかってない)
**outputDir = "home/nakamura_kento/wrf/work/figure"

**ファイルを開く
'open indian01d02.ctl'

**白くする
'set display color white'
'c'

**地図の解像度を上げる
**'set mpdset hires'

**緯度経度高度の設定
**'set lon 100 105'
**'set lat -6  -2'
**'set z 1 23'


**解析した時間,gradsを表示しない
'set timelab off'
'set grads off'
'c'

**シミュレーションの大まかな時間
hour = 11
minute=40
day=25
mon=11
year=2015
frame= 1

**繰り返しの設定（無限レープ）
while (1<2)

**時間、緯度の設定
**'set time 'hour':'minute'Z'day''
**'set z 'height
**'set lat 'lati
'c'


**レーダー反射強度
**'draw title WRF-dbz'
**'color 0 60 4  -kind white-(0)->rainbow'
**'set gxout shade2'
**'d dbz'
**'xcbar -line on -dir v'


**水平、鉛直風のベクトル
**'set gxout vector'
**'d skip(u,25,1);w*5'


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
'set z 1 '
'set x 1 1300'
'set y 1 1300'
'set t 1 145'
'd tloop(aave(qrain, x=1. x=1300, y=1, y=1300))'




**文字を書く
'set strsiz 0.1'
'draw string 7.0  8.3 '  'Time:'hour':'minute'Z'year''mon''day 
**'draw string 9.0  8.3 '  'lat:'lati
**'set strsiz 0.08'
**'draw string 0.5  8.0 '  '0.25, 0.50, 0.75, 1.00, 2.00, 3.00, 4.00, 5.00, 6.00, 7.00, 8.00, 9.00, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0'



**よくわからない
**'run cbar.gs '

**コマンドに操作ガイド
say 'Choose (No:n +1,b -1,s +6,r -6, Print+1:p, Quit:q,)'

**見る時間とかを変える
pull ans
if(ans = p)
'wi dbz'minute+10'.gif'
minute = minute+10 + 10
frame = frame + 1
endif
if(ans = n)
minute = minute + 10
endif
if(ans = b)
minute = minute - 10
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


