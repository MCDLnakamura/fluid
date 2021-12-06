' reinit '
' open mp06d03.ctl '

' set lon 130.9 131.1 '
**1194
' set lat 33.4 33.5 '
**915
' set time 10:00Z05 '
**217


**'set gxout fwrite'
h=1
say 'vapor'
while (h<=40)
' set z 'h' '
' a = aave(qvapor, lon=130.9, lon=131.1, lat=33.4, lat=33.5) '
'd a'
say result
h=h+1 
endwhile

h=1
say 'cloud'
while (h<=40)
' set z 'h' '
' a = aave(qcloud, lon=130.9, lon=131.1, lat=33.4, lat=33.5) '
'd a'
say result
h=h+1 
endwhile

h=1
say 'rain'
while (h<=40)
' set z 'h' '
' a = aave(qrain,  lon=130.9, lon=131.1, lat=33.4, lat=33.5) '
'd a'
say result
h=h+1 
endwhile

h=1
say 'snow'
while (h<=40)
' set z 'h' '
' a = aave(qsnow,  lon=130.9, lon=131.1, lat=33.4, lat=33.5) '
'd a'
say result
h=h+1 
endwhile

h=1
say 'graup'
while (h<=40)
' set z 'h' '
' a = aave(qgraup, lon=130.9, lon=131.1, lat=33.4, lat=33.5) '
'd a'
say result
h=h+1 
endwhile

**h=1
**say 'hail'
**while (h<=40)
**' set z 'h' '
**' a = aave(qhail,  lon=130.9, lon=131.1, lat=33.4, lat=33.5) '
**'d a'
**say result
**h=h+1 
**endwhile
