# -*- coding: utf-8 -*-
"""#11 論文紹介: 自作の要約グラフ（大腿周径 % 基準値比）1080x1350"""
from PIL import Image, ImageDraw, ImageFont
FB=r"C:\Windows\Fonts\BIZ-UDGothicB.ttc"; FR=r"C:\Windows\Fonts\BIZ-UDGothicR.ttc"
INK=(58,62,58); BLUE=(45,127,184); BLUED=(31,95,139); CREAM=(247,243,236); GREY=(185,180,172); LGREY=(225,222,216)
W,H=1080,1350
im=Image.new("RGB",(W,H),CREAM); d=ImageDraw.Draw(im)
def tw(s,f): l,t,r,b=d.textbbox((0,0),s,font=f); return r-l
def ctext(y,s,f,fill=INK): d.text(((W-tw(s,f))/2,y),s,font=f,fill=fill)
f1=ImageFont.truetype(FB,78); f2=ImageFont.truetype(FR,36); f3=ImageFont.truetype(FR,30); f4=ImageFont.truetype(FB,34); f5=ImageFont.truetype(FR,26)
ctext(90,"手術後の腫れを、",f1); ctext(190,"数字で見る。",f1)
d.rounded_rectangle((W/2-110,300,W/2+110,308),radius=4,fill=BLUE)
ctext(330,"論文になりました（2026年・英文誌）",f2,BLUED)
# chart
x0,y0,x1,y1=130,470,W-80,1030
# axis: 98%..108%
ymin,ymax=100,108
def Y(v): return y1-(v-ymin)/(ymax-ymin)*(y1-y0)
for v in range(100,109,2):
    yy=Y(v); d.line((x0,yy,x1,yy),fill=LGREY,width=2); d.text((x0-95,yy-16),f"{v}%",font=f3,fill=INK)
d.line((x0,Y(100),x1,Y(100)),fill=GREY,width=3)
labels=["術後1日目","術後5日目（腫れのピーク）"]
ctrl=[104.7,106.9]; sup=[102.2,103.7]
n=2; gw=(x1-x0)/n; bw=120
for i in range(n):
    cx=x0+gw*(i+0.5)
    for k,(val,col) in enumerate(((ctrl[i],GREY),(sup[i],BLUE))):
        bx=cx-bw-12 if k==0 else cx+12
        d.rounded_rectangle((bx,Y(val),bx+bw,Y(100)),radius=6,fill=col)
        d.text((bx+bw/2-tw(f"{val:.1f}",f5)/2,Y(val)-34),f"{val:.1f}",font=f5,fill=INK)
    d.text((cx-tw(labels[i],f3)/2,y1+14),labels[i],font=f3,fill=INK)
    d.text((cx-tw("**",f4)/2,y0-40),"**",font=f4,fill=BLUED)
# legend
ly=1095
d.rounded_rectangle((200,ly,240,ly+30),radius=4,fill=GREY); d.text((252,ly-4),"着用なし（64人）",font=f3,fill=INK)
d.rounded_rectangle((560,ly,600,ly+30),radius=4,fill=BLUE); d.text((612,ly-4),"サポーター着用（77人）",font=f3,fill=INK)
ctext(1150,"手術した側の太ももの太さ（手術前＝100%）　**：群間差 p<0.01",f5,BLUED)
ctext(1190,"単一施設・後ろ向き比較研究　2週以降は群間差なし",f5,BLUED)
band=84; d.rectangle((0,H-band,W,H),fill=(238,233,224))
ctext(H-band+24,"整形外科専門医が開発｜トータルHipサポーター",f3)
im.save("posts/11_paper_1080x1350.jpg",quality=92); print("ok")
