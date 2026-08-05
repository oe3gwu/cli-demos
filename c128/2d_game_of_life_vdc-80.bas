0 rem c128 vdc 80 col - graphics 5, fast (2mhz cpu)
1 rem lines 1-23 play, 24 blank, 25 pop/gen - vdc default colors only
2 rem speed: int arrays + row index; vdc = full addr write (stable)
5 graphics 5,1
10 scnclr 5:fast
11 w=82:h=27:wh=w*h:dim c%(wh),n%(wh)
12 rw=80:bl=160:sp=32:d=128
13 slb=23*rw:sl2=24*rw
14 maxg=20:pf=1840
30 gosub 600
35 gosub 700
40 g=0
50 pn=0:for y=1 to 23:i0=y*w:for x=1 to 80:pn=pn+c%(i0+x):next x:next y
55 gosub 1000
60 g=g+1:pn=0
70 for y=1 to 23
75 i0=y*w:ro=(y-1)*rw
80 for x=1 to 80
90 i=i0+x
100 s=c%(i-1)+c%(i+1)+c%(i-w)+c%(i+w)
110 s=s+c%(i-w-1)+c%(i-w+1)+c%(i+w-1)+c%(i+w+1)
120 q=0:if s=3 then q=1
130 if c%(i) and s=2 then q=1
140 if q=c%(i) then 160
145 ad=ro+x-1:ch=sp+q*d:gosub 2000
160 n%(i)=q:pn=pn+q
170 next x:next y
175 for i=0 to wh-1:c%(i)=n%(i):next
180 gosub 1000
185 if g>=maxg then gosub 600:goto 40
190 goto 60
600 rem restart - clear, seed, redraw field
610 for i=0 to wh-1:c%(i)=0:n%(i)=0:next
620 gosub 800
630 g=0:gosub 900:gosub 700
690 return
800 rem seed - rng 15-20% of pf cells per start
805 r=rnd(-ti)
806 p=15+int(rnd(1)*6)
807 nc=int(pf*p/100)
808 restore 3000
810 cx=40:cy=11
820 for k=0 to 4:read x,y:c%((cy+y)*w+cx+x)=1:next
830 cx=5:cy=5
840 restore 3010
850 for k=0 to 4:read x,y:c%((cy+y)*w+cx+x)=1:next
860 for k=1 to nc:y=int(rnd(1)*23)+1:x=int(rnd(1)*80)+1:c%(y*w+x)=1:next
895 return
900 rem draw playfield lines 1-23
910 for y=1 to 23
920 i0=y*w:ro=(y-1)*rw
930 for x=1 to 80
940 ad=ro+x-1:ch=sp+c%(i0+x)*d:gosub 2000
960 next x:next y
990 return
700 rem line 24 blank, line 25 clear then labels
710 for i=0 to 79:ad=slb+i:ch=sp:gosub 2000:next
715 for i=0 to 79:ad=sl2+i:ch=sp:gosub 2000:next
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
1110 d1=int(t/10000):ch=48+d1:gosub 2000:ad=ad+1:t=t-d1*10000
1120 d1=int(t/1000):ch=48+d1:gosub 2000:ad=ad+1:t=t-d1*1000
1130 d1=int(t/100):ch=48+d1:gosub 2000:ad=ad+1:t=t-d1*100
1140 d1=int(t/10):ch=48+d1:gosub 2000:ad=ad+1:ch=48+t-d1*10:gosub 2000
1190 return
2000 rem vdc write char only — full address each time (stable)
2010 if (peek(54784) and 32)=0 then 2010
2020 poke 54784,18:poke 54785,int(ad/256)
2030 if (peek(54784) and 32)=0 then 2030
2040 poke 54784,19:poke 54785,ad-int(ad/256)*256
2050 if (peek(54784) and 32)=0 then 2050
2060 poke 54784,31:poke 54785,ch
2070 return
3000 data 0,0,1,0,2,0,0,1,1,1
3010 data 0,0,1,1,2,0,2,-1,2,1
