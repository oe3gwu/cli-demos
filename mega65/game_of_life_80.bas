0 rem mega65 80x25 native text - no color cmds (native blue/white)
1 rem lines 1-23 play, 24 blank, 25 pop/gen - t@& only, speed 40mhz
5 if rwindow(2)<>80 then print chr$(27)+"8";
10 speed:print chr$(147):scnclr
11 w=82:h=27:wh=w*h:dim c&(wh),n&(wh)
12 bl=160:sp=32
13 maxg=20:pf=1840
30 gosub 600
35 gosub 700
40 g=0
50 pn=0:for y=1 to 23:i0=y*w:for x=1 to 80:pn=pn+c&(i0+x):next x:next y
55 gosub 1000
60 g=g+1:pn=0
70 for y=1 to 23
75 i0=y*w
80 for x=1 to 80
90 i=i0+x
100 s=c&(i-1)+c&(i+1)+c&(i-w)+c&(i+w)
110 s=s+c&(i-w-1)+c&(i-w+1)+c&(i+w-1)+c&(i+w+1)
120 q=0:if s=3 then q=1
130 if c&(i) and s=2 then q=1
140 if q<>c&(i) then t@&(x-1,y-1)=sp+q*(bl-sp)
150 n&(i)=q:pn=pn+q
160 next x:next y
165 for i=0 to wh-1:c&(i)=n&(i):next
170 gosub 1000
180 if g>=maxg then gosub 600:goto 40
190 goto 60
600 rem restart - clear, seed, redraw field
610 for i=0 to wh-1:c&(i)=0:n&(i)=0:next
620 gosub 800
630 g=0:gosub 900:gosub 700
690 return
800 rem seed - rng 15-20% of pf cells per start
805 r=rnd(-ti)
806 p=15+int(rnd(1)*6)
807 nc=int(pf*p/100)
808 restore 3000
810 cx=40:cy=11
820 for k=0 to 4:read x,y:c&((cy+y)*w+cx+x)=1:next
830 cx=5:cy=5
840 restore 3010
850 for k=0 to 4:read x,y:c&((cy+y)*w+cx+x)=1:next
860 for k=1 to nc:y=int(rnd(1)*23)+1:x=int(rnd(1)*80)+1:c&(y*w+x)=1:next
895 return
900 rem draw playfield lines 1-23
910 for y=1 to 23
920 i0=y*w
925 for x=1 to 80
930 t@&(x-1,y-1)=sp+c&(i0+x)*(bl-sp)
940 next x:next y
990 return
700 rem line 24 blank, line 25 clear then labels
710 for i=0 to 79:t@&(i,23)=32:t@&(i,24)=32:next
720 t@&(0,24)=16:t@&(1,24)=15:t@&(2,24)=16:t@&(3,24)=58
730 t@&(65,24)=7:t@&(66,24)=5:t@&(67,24)=14:t@&(68,24)=58
790 return
1000 rem line 25 digits only
1010 t=pn:sx=4:gosub 1100
1020 t=g:sx=70:gosub 1100
1090 return
1100 rem 5 digits of t at col sx, row 24
1110 d=int(t/10000):t@&(sx,24)=48+d:sx=sx+1:t=t-d*10000
1120 d=int(t/1000):t@&(sx,24)=48+d:sx=sx+1:t=t-d*1000
1130 d=int(t/100):t@&(sx,24)=48+d:sx=sx+1:t=t-d*100
1140 d=int(t/10):t@&(sx,24)=48+d:t@&(sx+1,24)=48+t-d*10
1190 return
3000 data 0,0,1,0,2,0,0,1,1,1
3010 data 0,0,1,1,2,0,2,-1,2,1
