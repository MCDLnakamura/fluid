' reinit '
' open mp06d03.ctl '

' set lon 130.9 131.1 '
**1194
' set lat 33.4 33.5 '
**915
' set time 10:00Z05 '
**217

 h=1
**'set gxout fwrite'
while (h<=40)
' set z 'h' '

**' a = aave(qvapor, lon=130.9, lon=131.1, lat=33.4, lat=33.5) '
**' a = aave(qcloud, lon=130.9, lon=131.1, lat=33.4, lat=33.5) '
**' a = aave(qrain,  lon=130.9, lon=131.1, lat=33.4, lat=33.5) '
**' a = aave(qice,   lon=130.9, lon=131.1, lat=33.4, lat=33.5) '
**' a = aave(qsnow,  lon=130.9, lon=131.1, lat=33.4, lat=33.5) '
**' a = aave(qgraup, lon=130.9, lon=131.1, lat=33.4, lat=33.5) '
**' a = aave(qhail,  lon=130.9, lon=131.1, lat=33.4, lat=33.5) '

'd a'
say result
h=h+1 

endwhile


