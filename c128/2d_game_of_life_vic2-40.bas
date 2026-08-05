0 rem c128 vic-ii 40 col only - not vdc 80 col
1 rem vice: graphics 0, view vic window, 80col off
2 rem speed: int arrays, row index, dirty poke only
5 graphics 0
10 print chr$(147):poke 53280,0:poke 53281,0:slow
11 w=42:h=27:wh=w*h:dim c%(wh),n%(wh)
12 sc=1024:cr=55296:bl=160:sp=32:lg=13:d=128
13 slb=sc+23*40:sl2=sc+24*40:clb=cr+23*40:cl2=cr+24*40
14 maxg=20:pf=920
30 gosub 600
35 gosub 700
40 g=0
50 pn=0:for y=1 to 23:i0=y*w:for x=1 to 40:pn=pn+c%(i0+x):next x:next y
55 gosub 1000
60 g=g+1:pn=0
70 for y=1 to 23
75 i0=y*w:so=sc+(y-1)*40:co=cr+(y-1)*40
80 for x=1 to 40
90 i=i0+x
100 s=c%(i-1)+c%(i+1)+c%(i-w)+c%(i+w)
110 s=s+c%(i-w-1)+c%(i-w+1)+c%(i+w-1)+c%(i+w+1)
120 q=0:if s=3 then q=1
130 if c%(i) and s=2 then q=1
140 if q=c%(i) then 160
150 poke so+x-1,sp+q*d:poke co+x-1,lg
160 n%(i)=q:pn=pn+q
170 next x:next y
175 for i=0 to wh-1:c%(i)=n%(i):next
180 gosub 1000
185 if g>=maxg then gosub 600:goto 40
190 goto 60
600 rem restart - clear, seed, redraw field
610 for i=0 to wh-1:c%(i)=0:n%(i)=0:next
620 gosub 800
630 g=0:gosub 900
690 return
800 rem seed - rng 15-20% of pf cells per start
805 r=rnd(-ti)
806 p=15+int(rnd(1)*6)
807 nc=int(pf*p/100)
808 restore 2000
810 cx=20:cy=11
820 for k=0 to 4:read x,y:c%((cy+y)*w+cx+x)=1:next
830 cx=5:cy=5
840 restore 2010
850 for k=0 to 4:read x,y:c%((cy+y)*w+cx+x)=1:next
860 for k=1 to nc:y=int(rnd(1)*23)+1:x=int(rnd(1)*40)+1:c%(y*w+x)=1:next
895 return
900 rem lines 1-23 only (screen rows 0-22)
910 for y=1 to 23
920 i0=y*w:so=sc+(y-1)*40:co=cr+(y-1)*40
930 for x=1 to 40
950 poke so+x-1,sp+c%(i0+x)*d:poke co+x-1,lg
960 next x:next y
990 return
700 rem line 24 blank, line 25 labels (once)
710 for i=0 to 39:poke slb+i,sp:poke clb+i,lg:next
720 for i=0 to 39:poke sl2+i,sp:poke cl2+i,lg:next
730 poke sl2,16:poke sl2+1,15:poke sl2+2,16:poke sl2+3,58
735 poke sl2+31,7:poke sl2+32,5:poke sl2+33,14:poke sl2+34,58
790 return
1000 rem line 25 digits only (pn=population, not pop keyword)
1010 t=pn:lp=sl2+4:gosub 1100
1020 t=g:lp=sl2+35:gosub 1100
1090 return
1100 rem 5 digits of t at lp
1110 d1=int(t/10000):poke lp,48+d1:t=t-d1*10000
1120 d1=int(t/1000):poke lp+1,48+d1:t=t-d1*1000
1130 d1=int(t/100):poke lp+2,48+d1:t=t-d1*100
1140 d1=int(t/10):poke lp+3,48+d1:poke lp+4,48+t-d1*10
1190 return
2000 data 0,0,1,0,2,0,0,1,1,1
2010 data 0,0,1,1,2,0,2,-1,2,1
