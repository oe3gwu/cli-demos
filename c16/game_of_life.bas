0 rem c16/plus4 ted - 40x23, black bg/border, boot-lilac fg
1 rem basic 3.5; compact arrays (16k-safe); double buffer
2 rem kernal TED init: $FF19=$6E = color 15 (dark blue), lum 6 — not purple/5
5 graphic 0
10 color 0,1:color 4,1:color 1,15,6:print chr$(147)
11 w=40:wh=920:dim c(wh),n(wh)
12 sc=3072:cr=2048:bl=160:sp=32:d=128:lg=110


13 slb=sc+23*40:sl2=sc+24*40:clb=cr+23*40:cl2=cr+24*40
14 maxg=20:pf=920
30 gosub 600
35 gosub 700
40 g=0
50 pn=0:for y=1 to 23:i0=(y-1)*w:for x=1 to 40:pn=pn+c(i0+x-1):next x:next y
55 gosub 1000
60 g=g+1:pn=0
70 for y=1 to 23
75 i0=(y-1)*w:so=sc+i0:co=cr+i0
80 for x=1 to 40
90 i=i0+x-1
100 s=0
110 if x>1 then s=s+c(i-1)
120 if x<40 then s=s+c(i+1)
130 if y>1 then s=s+c(i-w)
140 if y<23 then s=s+c(i+w)
150 if y>1 and x>1 then s=s+c(i-w-1)
155 if y>1 and x<40 then s=s+c(i-w+1)
160 if y<23 and x>1 then s=s+c(i+w-1)
165 if y<23 and x<40 then s=s+c(i+w+1)
170 q=0:if s=3 then q=1
175 if c(i) and s=2 then q=1
180 if q=c(i) then 190
185 poke so+x-1,sp+q*d:poke co+x-1,lg
190 n(i)=q:pn=pn+q
195 next x:next y
200 for i=0 to wh-1:c(i)=n(i):next
210 gosub 1000
215 if g>=maxg then gosub 600:goto 40
220 goto 60
600 rem restart - clear, seed, redraw field
610 for i=0 to wh-1:c(i)=0:n(i)=0:next
620 gosub 800
630 g=0:gosub 900
690 return
800 rem seed - rng 15-20% of pf cells per start
805 r=rnd(-ti)
806 p=15+int(rnd(1)*6)
807 nc=int(pf*p/100)
808 restore
810 cx=20:cy=11
820 for k=0 to 4:read x,y:c((cy+y-1)*w+cx+x-1)=1:next
830 cx=5:cy=5
840 for k=0 to 4:read x,y:c((cy+y-1)*w+cx+x-1)=1:next
860 for k=1 to nc:y=int(rnd(1)*23)+1:x=int(rnd(1)*40)+1:c((y-1)*w+x-1)=1:next
895 return
900 rem lines 1-23 only (screen rows 0-22)
910 for y=1 to 23
920 i0=(y-1)*w:so=sc+i0:co=cr+i0
930 for x=1 to 40
950 poke so+x-1,sp+c(i0+x-1)*d:poke co+x-1,lg
960 next x:next y
990 return
700 rem line 24 blank, line 25 labels (once)
710 for i=0 to 39:poke slb+i,sp:poke clb+i,lg:next
720 for i=0 to 39:poke sl2+i,sp:poke cl2+i,lg:next
730 poke sl2,16:poke sl2+1,15:poke sl2+2,16:poke sl2+3,58
735 poke sl2+31,7:poke sl2+32,5:poke sl2+33,14:poke sl2+34,58
790 return
1000 rem line 25 digits only
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
