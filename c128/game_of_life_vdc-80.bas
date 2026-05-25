0 rem c128 vdc 80 col - graphics 5, fast (2mhz cpu)
1 rem lines 1-23 play, 24 blank, 25 pop/gen - vdc default colors only
5 graphics 5
10 scnclr:fast
11 w=82:h=27:wh=w*h:dim c(wh)
12 rw=80:bl=160:sp=32
13 slb=23*rw:sl2=24*rw
20 for i=0 to wh-1:c(i)=0:next
30 gosub 800
40 g=0:gosub 900:gosub 700
50 pn=0:for y=1 to 23:for x=1 to 80:pn=pn+c(y*w+x):next x:next y
55 gosub 1000
60 g=g+1:pn=0
70 for y=1 to 23
80 for x=1 to 80
90 i=y*w+x
100 s=c(i-1)+c(i+1)+c(i-w)+c(i+w)
110 s=s+c(i-w-1)+c(i-w+1)+c(i+w-1)+c(i+w+1)
120 q=0:if s=3 then q=1
130 if c(i) and s=2 then q=1
140 sy=y-1:sx=x-1
150 if q<>c(i) then ad=sy*rw+sx:ch=sp+q*(bl-sp):gosub 2000
160 c(i)=q:pn=pn+q
170 next x:next y
180 gosub 1000
190 goto 60
800 rem seed - 11% of 1840 = 202 cells
805 r=rnd(-ti)
810 cx=40:cy=11
820 for k=0 to 4:read x,y:c((cy+y)*w+cx+x)=1:next
830 cx=5:cy=5
840 for k=0 to 4:read x,y:c((cy+y)*w+cx+x)=1:next
850 for k=1 to 202:y=int(rnd(1)*23)+1:x=int(rnd(1)*80)+1:c(y*w+x)=1:next
895 return
900 rem draw playfield lines 1-23
910 for y=1 to 23
920 sy=y-1
930 for x=1 to 80
940 sx=x-1
950 ad=sy*rw+sx:ch=sp+c(y*w+x)*(bl-sp):gosub 2000
960 next x:next y
990 return
700 rem line 24 blank, line 25 labels
710 for i=0 to 79:ad=slb+i:ch=32:gosub 2000:next
720 ad=sl2:ch=16:gosub 2000:ad=sl2+1:ch=15:gosub 2000
730 ad=sl2+2:ch=16:gosub 2000:ad=sl2+3:ch=58:gosub 2000
740 ad=sl2+65:ch=7:gosub 2000:ad=sl2+66:ch=5:gosub 2000
750 ad=sl2+67:ch=14:gosub 2000:ad=sl2+68:ch=58:gosub 2000
790 return
1000 rem line 25 digits only
1010 t=pn:ad=sl2+4:gosub 1100
1020 t=g:ad=sl2+70:gosub 1100
1090 return
1100 rem 5 digits of t at ad
1110 d=int(t/10000):ch=48+d:gosub 2000:ad=ad+1:t=t-d*10000
1120 d=int(t/1000):ch=48+d:gosub 2000:ad=ad+1:t=t-d*1000
1130 d=int(t/100):ch=48+d:gosub 2000:ad=ad+1:t=t-d*100
1140 d=int(t/10):ch=48+d:gosub 2000:ad=ad+1:ch=48+t-d*10:gosub 2000
1190 return
2000 rem vdc write char only (no color/attr, no lg)
2010 if (peek(54784) and 32)=0 then 2010
2020 poke 54784,18:poke 54785,int(ad/256)
2030 if (peek(54784) and 32)=0 then 2030
2040 poke 54784,19:poke 54785,ad-int(ad/256)*256
2050 if (peek(54784) and 32)=0 then 2050
2060 poke 54784,31:poke 54785,ch
2070 return
3000 data 0,0,1,0,2,0,0,1,1,1
3010 data 0,0,1,1,2,0,2,-1,2,1
