0 rem c64 1d life — millen/byte YYXYY (outer totalistic 624)
1 rem evolution view: each gen a screen row; wrap ring; restart 20 gen
10 print chr$(147):poke 53280,0:poke 53281,0
11 w=40:dim c(39),n(39)
12 sc=1024:cr=55296:bl=160:sp=32:d=128:lg=14
13 slb=sc+23*40:sl2=sc+24*40:clb=cr+23*40:cl2=cr+24*40
14 maxg=20
30 gosub 600
40 g=0
50 pn=0:for x=0 to 39:pn=pn+c(x):next
55 gosub 1000
60 g=g+1:if g>maxg then gosub 600:goto 40
70 gosub 400
80 ry=g:gosub 950
90 for x=0 to 39:c(x)=n(x):next
100 pn=0:for x=0 to 39:pn=pn+c(x):next
110 gosub 1000
120 goto 60
400 rem step: birth ny=2|3, survive ny=2|4 (Y-neighbors only)
410 for x=0 to 39
420 a=x-2:if a<0 then a=a+w
430 b=x-1:if b<0 then b=b+w
440 e=x+1:if e>=w then e=e-w
450 f=x+2:if f>=w then f=f-w
460 ny=c(a)+c(b)+c(e)+c(f)
470 q=0
480 if c(x)=0 and(ny=2 or ny=3) then q=1
490 if c(x)=1 and(ny=2 or ny=4) then q=1
500 n(x)=q
510 next x
520 return
600 rem restart — clear, seed, draw gen0 on row 0, chrome
610 for x=0 to 39:c(x)=0:n(x)=0:next
615 print chr$(147)
620 gosub 800
630 g=0:ry=0:gosub 900:gosub 700
640 pn=0:for x=0 to 39:pn=pn+c(x):next:gosub 1000
690 return
800 rem seed — ~28-35% live
805 r=rnd(-ti)
806 sd=28+int(rnd(1)*8)
810 for x=0 to 39:if rnd(1)*100<sd then c(x)=1
820 next x
895 return
900 rem draw array c() on screen row ry
910 so=sc+ry*40:co=cr+ry*40
920 for x=0 to 39:poke so+x,sp+c(x)*d:poke co+x,lg:next
930 return
950 rem draw array n() on screen row ry
960 so=sc+ry*40:co=cr+ry*40
970 for x=0 to 39:poke so+x,sp+n(x)*d:poke co+x,lg:next
980 return
700 rem line 24 blank, line 25: POP left, SEED center, GEN right
710 for i=0 to 39:poke slb+i,sp:poke clb+i,lg:next
720 for i=0 to 39:poke sl2+i,sp:poke cl2+i,lg:next
730 poke sl2,16:poke sl2+1,15:poke sl2+2,16:poke sl2+3,58
740 poke sl2+15,19:poke sl2+16,5:poke sl2+17,5:poke sl2+18,4:poke sl2+19,58
750 poke sl2+31,7:poke sl2+32,5:poke sl2+33,14:poke sl2+34,58
790 return
1000 rem digits: pop@4, seed%@20, gen@35
1010 t=pn:lp=sl2+4:gosub 1100
1015 t=sd:lp=sl2+20:gosub 1100
1020 t=g:lp=sl2+35:gosub 1100
1090 return
1100 rem 5 digits of t at lp
1110 d1=int(t/10000):poke lp,48+d1:t=t-d1*10000
1120 d1=int(t/1000):poke lp+1,48+d1:t=t-d1*1000
1130 d1=int(t/100):poke lp+2,48+d1:t=t-d1*100
1140 d1=int(t/10):poke lp+3,48+d1:poke lp+4,48+t-d1*10
1190 return
