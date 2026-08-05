0 rem mega65 80-col 1d life — millen/byte YYXYY
1 rem evolution view; wrap ring; restart 20 gen; t@& only, speed
5 if rwindow(2)<>80 then print chr$(27)+"8";
10 speed:print chr$(147):scnclr
11 w=80:dim c&(79),n&(79)
12 bl=160:sp=32:d=128
13 maxg=20
30 gosub 600
40 g=0
50 pn=0:for x=0 to 79:pn=pn+c&(x):next
55 gosub 1000
60 g=g+1:if g>maxg then gosub 600:goto 40
70 gosub 400
80 ry=g:gosub 950
90 for x=0 to 79:c&(x)=n&(x):next
100 pn=0:for x=0 to 79:pn=pn+c&(x):next
110 gosub 1000
120 goto 60
400 rem step: birth ny=2|3, survive ny=2|4 (Y-neighbors only)
410 for x=0 to 79
420 a=x-2:if a<0 then a=a+w
430 b=x-1:if b<0 then b=b+w
440 e=x+1:if e>=w then e=e-w
450 f=x+2:if f>=w then f=f-w
460 ny=c&(a)+c&(b)+c&(e)+c&(f)
470 q=0
480 if c&(x)=0 and(ny=2 or ny=3) then q=1
490 if c&(x)=1 and(ny=2 or ny=4) then q=1
500 n&(x)=q
510 next x
520 return
600 rem restart — clear, seed, draw gen0 on row 0, chrome
610 for x=0 to 79:c&(x)=0:n&(x)=0:next
615 print chr$(147):scnclr
620 gosub 800
630 g=0:ry=0:gosub 900:gosub 700
640 pn=0:for x=0 to 79:pn=pn+c&(x):next:gosub 1000
690 return
800 rem seed — ~28-35% live
805 r=rnd(-ti)
806 sd=28+int(rnd(1)*8)
810 for x=0 to 79:if rnd(1)*100<sd then c&(x)=1
820 next x
895 return
900 rem draw array c&() on screen row ry
910 for x=0 to 79:t@&(x,ry)=sp+c&(x)*d:next
930 return
950 rem draw array n&() on screen row ry
960 for x=0 to 79:t@&(x,ry)=sp+n&(x)*d:next
980 return
700 rem line 24 blank, line 25: POP left, SEED center, GEN right
710 for i=0 to 79:t@&(i,23)=32:t@&(i,24)=32:next
720 t@&(0,24)=16:t@&(1,24)=15:t@&(2,24)=16:t@&(3,24)=58
740 t@&(35,24)=19:t@&(36,24)=5:t@&(37,24)=5:t@&(38,24)=4:t@&(39,24)=58
750 t@&(65,24)=7:t@&(66,24)=5:t@&(67,24)=14:t@&(68,24)=58
790 return
1000 rem digits: pop@4, seed%@40, gen@70
1010 t=pn:sx=4:gosub 1100
1015 t=sd:sx=40:gosub 1100
1020 t=g:sx=70:gosub 1100
1090 return
1100 rem 5 digits of t at col sx, row 24
1110 d1=int(t/10000):t@&(sx,24)=48+d1:sx=sx+1:t=t-d1*10000
1120 d1=int(t/1000):t@&(sx,24)=48+d1:sx=sx+1:t=t-d1*1000
1130 d1=int(t/100):t@&(sx,24)=48+d1:sx=sx+1:t=t-d1*100
1140 d1=int(t/10):t@&(sx,24)=48+d1:t@&(sx+1,24)=48+t-d1*10
1190 return
