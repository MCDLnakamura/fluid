**全てリセット
'reinit'

mp=26

**ファイルを開く
'open mp'mp'd03.ctl'

**白くする
'set display color white'
'c'

**緯度経度高度の設定
'set lon 129.95 132.05'
**'set lat -6  -2'
'set z 1 36'


**シミュレーションの大まかな時間
hour = 5
minute=00
day=05
mon=07
year=2017
lati=33.47

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


**水平、鉛直風のベクトル
**'set gxout vector'
**'d skip(u,50,1);w*5'
**'set arrlab off '

**混合比を書く
'color 1 10 1  -kind white-(0)->rainbow'
'set  gxout shade2'
'qall=qcloud+qrain+qice+qsnow+qgraup+qhail'
**'qall=qvapor+qcloud+qrain+qice+qsnow+qgraup+qhail'
'd qall*1000'
**'qnall=qnccn+qncloud+qnrain'


**文字を書く'
'set strsiz 0.1'
'draw string 7.0  8.3 '  'Time:'hour':'minute'Z'year''mon''day 
'draw string 9.0  8.3 '  'mp'mp'_'lati'n'
**'set strsiz 0.08'
**'draw string 0.5  8.0 '  '0.25, 0.50, 0.75, 1.00, 2.00, 3.00, 4.00, 5.00, 6.00, 7.00, 8.00, 9.00, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0'


**よくわからない
'run cbar.gs '

**コマンドに操作ガイド
say 'Choose (lat:k +1,m -1, No:n +1,b -1,s +6,r -6, Print+1:p, Quit:q,)'

**見る時間とかを変える
pull ans
if(ans = p)
'wi mp'mp'_'lati'_'hour''minute'.png' 
endif
if(ans = n)
minute = minute + 10
endif
if(ans = b)
minute = minute - 10
endif
if(ans = k)
lati = lati + 0.001
endif
if(ans = m)
lati = lati - 0.001
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


