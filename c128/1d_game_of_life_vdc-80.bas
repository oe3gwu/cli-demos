0 rem c128 vdc 80 col 1d life — millen/byte YYXYY
1 rem evolution view; wrap ring; restart 20 gen; vdc default colors
5 graphics 5,1
10 scnclr 5:fast
11 w=80:dim c%(79),n%(79)
12 rw=80:bl=160:sp=32:d=128
13 slb=23*rw:sl2=24*rw
14 maxg=20
30 gosub 600
40 g=0
50 pn=0:for x=0 to 79:pn=pn+c%(x):next
55 gosub 1000
60 g=g+1:if g>maxg then gosub 600:goto 40
70 gosub 400
80 ry=g:gosub 950
90 for x=0 to 79:c%(x)=n%(x):next
100 pn=0:for x=0 to 79:pn=pn+c%(x):next
110 gosub 1000
120 goto 60
400 rem step: birth ny=2|3, survive ny=2|4 (Y-neighbors only)
410 for x=0 to 79
420 a=x-2:if a<0 then a=a+w
430 b=x-1:if b<0 then b=b+w
440 e=x+1:if e>=w then e=e-w
450 f=x+2:if f>=w then f=f-w
460 ny=c%(a)+c%(b)+c%(e)+c%(f)
470 q=0
480 if c%(x)=0 and(ny=2 or ny=3) then q=1
490 if c%(x)=1 and(ny=2 or ny=4) then q=1
500 n%(x)=q
510 next x
520 return
600 rem restart — clear, seed, draw gen0 on row 0, chrome
610 for x=0 to 79:c%(x)=0:n%(x)=0:next
615 scnclr 5
620 gosub 800
630 g=0:ry=0:gosub 900:gosub 700
640 pn=0:for x=0 to 79:pn=pn+c%(x):next:gosub 1000
690 return
800 rem seed — ~28-35% live
805 r=rnd(-ti)
806 sd=28+int(rnd(1)*8)
810 for x=0 to 79:if rnd(1)*100<sd then c%(x)=1
820 next x
895 return
900 rem draw array c%() on screen row ry
910 for x=0 to 79:ad=ry*rw+x:ch=sp+c%(x)*d:gosub 2000:next
930 return
950 rem draw array n%() on screen row ry
960 for x=0 to 79:ad=ry*rw+x:ch=sp+n%(x)*d:gosub 2000:next
980 return
700 rem line 24 blank, line 25: POP left, SEED center, GEN right
710 for i=0 to 79:ad=slb+i:ch=sp:gosub 2000:next
715 for i=0 to 79:ad=sl2+i:ch=sp:gosub 2000:next
720 ad=sl2:ch=16:gosub 2000:ad=sl2+1:ch=15:gosub 2000
725 ad=sl2+2:ch=16:gosub 2000:ad=sl2+3:ch=58:gosub 2000
740 ad=sl2+35:ch=19:gosub 2000:ad=sl2+36:ch=5:gosub 2000
745 ad=sl2+37:ch=5:gosub 2000:ad=sl2+38:ch=4:gosub 2000:ad=sl2+39:ch=58:gosub 2000
750 ad=sl2+65:ch=7:gosub 2000:ad=sl2+66:ch=5:gosub 2000
755 ad=sl2+67:ch=14:gosub 2000:ad=sl2+68:ch=58:gosub 2000
790 return
1000 rem digits: pop@4, seed%@40, gen@70 (not @75 — last col often clipped)
1010 t=pn:ad=sl2+4:gosub 1100
1015 t=sd:ad=sl2+40:gosub 1100
1020 t=g:ad=sl2+70:gosub 1100
1090 return
1100 rem 5 digits of t at ad
1110 d1=int(t/10000):ch=48+d1:gosub 2000:ad=ad+1:t=t-d1*10000
1120 d1=int(t/1000):ch=48+d1:gosub 2000:ad=ad+1:t=t-d1*1000
1130 d1=int(t/100):ch=48+d1:gosub 2000:ad=ad+1:t=t-d1*100
1140 d1=int(t/10):ch=48+d1:gosub 2000:ad=ad+1:ch=48+t-d1*10:gosub 2000
1190 return
2000 rem vdc write char — full address each time (stable)
2010 if (peek(54784) and 32)=0 then 2010
2020 poke 54784,18:poke 54785,int(ad/256)
2030 if (peek(54784) and 32)=0 then 2030
2040 poke 54784,19:poke 54785,ad-int(ad/256)*256
2050 if (peek(54784) and 32)=0 then 2050
2060 poke 54784,31:poke 54785,ch
2070 return
