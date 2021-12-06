**全てリセット
'reinit'

**ファイルの保存場所(よくわかってない)
**outputDir = "home/nakamura_kento/wrf/work/figure"

**ファイルを開く
'open mp24d03.ctl'

**白くする
'set display color white'
'c'

**地図の解像度を上げる
'set mpdset hires'

**緯度経度高度の設定
**'set lon 100 105'
**'set lat -6  -2'



**解析した時間,gradsを表示しない
'set timelab off'
'set grads off'
'c'

**シミュレーションの大まかな時間
hour = 06
minute=00
day=05
mon=07
year=2017
height = 12
**frame= 1

**繰り返しの設定（無限レープ）
while (1<2)

**時間、緯度の設定
'set time 'hour':'minute'Z'day''
'set z ' height
'c'


**レーダー反射強度
**'draw title WRF-dbz'
'color 5 60 5  -kind white-(0)->rainbow'
'set gxout shade2'
'd dbz'
**'xcbar -line on -dir v'


**水平風のベクトル
**'set gxout vector'
**'set arrlab on'
**'set arrscl 1 20'
**'d skip(u,25,25)*0.5;v*0.5'


**文字を書く
**'set strsiz 0.1'
**'draw string 6.0  8.3 '  'WSM6_dbz_Time:'hour':'minute'Z'year''mon''day 
**'draw string 9.0  8.3 '  'Height:'height
**'set strsiz 0.08'
**'draw string 0.5  8.0 '  '0.25, 0.50, 0.75, 1.00, 2.00, 3.00, 4.00, 5.00, 6.00, 7.00, 8.00, 9.00, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0'


**よくわからない
**'run cbar.gs '

**コマンドに操作ガイド
say 'Choose (Lv:h +1,l -1, No:n +1,b -1,s +6,r -6, Print+1:p, Quit:q,)'

**見る時間とかを変える
pull ans
if(ans = p)
'wi 06dbz_'hour+9'00.png'
hour = hour + 1
**frame = frame + 1
endif
if(ans = n)
minute = minute + 10
endif
if(ans = b)
minute = minute - 10
endif
if(ans = h)
height = height + 1
endif
if(ans = l)
height = height - 1
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
