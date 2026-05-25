0 rem c128 vic-ii 40 col only - not vdc 80 col
1 rem vice: graphics 0, view vic window, 80col off
5 graphics 0
10 print chr$(147):poke 53280,0:poke 53281,0
11 w=42:h=27:wh=w*h:dim c(wh)
12 sc=1024:cr=55296:bl=160:sp=32:lg=13
13 slb=sc+23*40:sl2=sc+24*40:clb=cr+23*40:cl2=cr+24*40
20 for i=0 to wh-1:c(i)=0:next
30 gosub 800
40 g=0:gosub 900:gosub 700
50 pn=0:for y=1 to 23:for x=1 to 40:pn=pn+c(y*w+x):next x:next y
55 gosub 1000
60 g=g+1:pn=0
70 for y=1 to 23
80 for x=1 to 40
90 i=y*w+x
100 s=c(i-1)+c(i+1)+c(i-w)+c(i+w)
110 s=s+c(i-w-1)+c(i-w+1)+c(i+w-1)+c(i+w+1)
120 q=0:if s=3 then q=1
130 if c(i) and s=2 then q=1
140 sy=y-1:sx=x-1
150 if q<>c(i) then poke sc+sy*40+sx,sp+q*(bl-sp):poke cr+sy*40+sx,lg
160 c(i)=q:pn=pn+q
170 next x:next y
180 gosub 1000
190 goto 60
800 rem seed - 11% of 920 = 101 cells
805 r=rnd(-ti)
810 cx=20:cy=11
820 for k=0 to 4:read x,y:c((cy+y)*w+cx+x)=1:next
830 cx=5:cy=5
840 for k=0 to 4:read x,y:c((cy+y)*w+cx+x)=1:next
850 for k=1 to 101:y=int(rnd(1)*23)+1:x=int(rnd(1)*40)+1:c(y*w+x)=1:next
895 return
900 rem lines 1-23 only (screen rows 0-22)
910 for y=1 to 23
920 sy=y-1
930 for x=1 to 40
940 sx=x-1
950 poke sc+sy*40+sx,sp+c(y*w+x)*(bl-sp):poke cr+sy*40+sx,lg
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
1110 d=int(t/10000):poke lp,48+d:t=t-d*10000
1120 d=int(t/1000):poke lp+1,48+d:t=t-d*1000
1130 d=int(t/100):poke lp+2,48+d:t=t-d*100
1140 d=int(t/10):poke lp+3,48+d:poke lp+4,48+t-d*10
1190 return
2000 data 0,0,1,0,2,0,0,1,1,1
2010 data 0,0,1,1,2,0,2,-1,2,1
