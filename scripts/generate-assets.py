#!/usr/bin/env python3
"""Original LAST LOGIN raster pixel art. All output stays in this project.

The procedural base is drawn at native resolution. Curated PNG overrides are
merged in staging and validated before the resulting assets are published.
"""
from pathlib import Path
import math
import random
import hashlib
import shutil
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'src' / 'assets'
OUT = ROOT / '.cache' / 'generated-art'
CURATED = ROOT / 'art' / 'curated'
QA = ROOT / 'test-results' / 'art-review'
P = {
 'void':'#111722','ink':'#202336','navy':'#29334b','blue0':'#354761','blue1':'#4b6480','blue2':'#69879b','blue3':'#92a9b2','blue4':'#c1c9be',
 'plum0':'#372f42','plum1':'#4e4258','plum2':'#6b5770','plum3':'#8f7592','plum4':'#b29ca9',
 'brown0':'#362c2c','brown1':'#503b34','brown2':'#705044','brown3':'#94664e','brown4':'#b9835d','brown5':'#d2a071',
 'skin0':'#955d52','skin1':'#ba7e65','skin2':'#d79e7a','skin3':'#ebbc91','skin4':'#f2d1a4',
 'green0':'#283d3b','green1':'#3e574d','green2':'#587462','green3':'#789279','green4':'#a4b396',
 'gold0':'#75573d','gold1':'#9e7747','gold2':'#c49a56','gold3':'#e2bc73','gold4':'#f4d998',
 'cream0':'#9a8b77','cream1':'#b5a58c','cream2':'#cfbea0','cream3':'#e6d4b2','cream4':'#f4e4c1',
 'red0':'#673e43','red1':'#90585a','red2':'#bb7d75','red3':'#d6a194',
 'gray0':'#4b4b52','gray1':'#68666a','gray2':'#8c8985','gray3':'#b4afa2','white':'#fff0cf'
}
COLORS=list(P.values())


def rgb(c):
 c=P.get(c,c)
 return tuple(int(c[i:i+2],16) for i in (1,3,5))

class Canvas:
 def __init__(self,w=320,h=200,bg='void',transparent=False):
  self.im=Image.new('RGBA',(w,h),(0,0,0,0) if transparent else rgb(bg)+(255,)); self.d=ImageDraw.Draw(self.im); self.w=w; self.h=h
 def r(self,x,y,w,h,c):
  if w>0 and h>0:self.d.rectangle((int(x),int(y),int(x+w-1),int(y+h-1)),fill=rgb(c))
 def p(self,pts,c):self.d.polygon([(int(x),int(y)) for x,y in pts],fill=rgb(c))
 def l(self,pts,c,width=1):self.d.line([(int(x),int(y)) for x,y in pts],fill=rgb(c),width=width)
 def e(self,x,y,w,h,c):
  if w>0 and h>0:self.d.ellipse((int(x),int(y),int(x+w-1),int(y+h-1)),fill=rgb(c))
 def dot(self,x,y,c):self.d.point((int(x),int(y)),fill=rgb(c))
 def tex(self,box,colors,n,seed=1,shape='fleck'):
  rr=random.Random(seed); x,y,w,h=box
  for _ in range(n):
   xx=rr.randrange(int(x),int(x+w)); yy=rr.randrange(int(y),int(y+h)); cc=rr.choice(colors)
   if shape=='grain':self.l([(xx,yy),(xx+rr.randrange(2,10),yy)],cc)
   elif shape=='weave':self.l([(xx,yy),(xx+1,yy+1)],cc)
   else:self.dot(xx,yy,cc)
 def paste(self,im,x,y):self.im.alpha_composite(im,(int(x),int(y)));self.d=ImageDraw.Draw(self.im)
 def text(self,s,x,y,c='cream3',scale=1):
  # Pillow's built-in bitmap font, only decorative English text in pictures.
  f=ImageFont.load_default(size=10)
  mask=Image.new('L',(max(12,len(s)*7),13));ImageDraw.Draw(mask).text((0,-1),s,font=f,fill=255,stroke_width=0)
  mask=mask.point(lambda q:255 if q>96 else 0)
  if scale!=1:mask=mask.resize((mask.width*scale,mask.height*scale),Image.Resampling.NEAREST)
  layer=Image.new('RGBA',mask.size,rgb(c)+(255,));self.im.paste(layer,(x,y),mask);self.d=ImageDraw.Draw(self.im)
 def save(self,path):
  p=OUT/path;p.parent.mkdir(parents=True,exist_ok=True);self.im.save(p,optimize=True)


def wood(c,box,seed=0,dark=False):
 x,y,w,h=box; c.r(x,y,w,h,'brown1' if dark else 'brown3')
 colors=['brown2','brown3'] if dark else ['brown2','brown4']
 c.tex(box,colors,int(w*h/(230 if dark else 150)),seed,'grain')
 rr=random.Random(seed)
 for yy in range(int(y)+1,int(y+h),13):
  c.l([(x,yy),(x+w,yy+rr.choice([-1,0,1]))],'brown0' if dark else 'brown2')
  c.l([(x,yy+1),(x+w,yy+1)],'brown2' if dark else 'brown4')
 for _ in range(max(1,int(w*h/4000))):
  xx=rr.randrange(int(x)+4,int(x+w)-4);yy=rr.randrange(int(y)+3,int(y+h)-3)
  c.e(xx-4,yy-1,10,3,'brown1' if dark else 'brown2');c.l([(xx-8,yy),(xx+10,yy)],'brown2' if dark else 'brown4')


def fabric(c,box,base='plum2',shadow='plum1',hi='plum3',seed=2):
 x,y,w,h=box;c.r(x,y,w,h,base)
 c.r(x,y,3,h,shadow);c.r(x+w-3,y,3,h,shadow);c.r(x,y+h-3,w,3,shadow)
 c.l([(x+4,y+2),(x+w-5,y+2)],hi)
 for yy in range(int(y)+6,int(y+h)-3,6):
  for xx in range(int(x)+5,int(x+w)-4,6):
   c.dot(xx,yy,hi);c.dot(xx+1,yy+1,shadow)
 c.tex((x+4,y+4,w-8,h-8),[shadow,base],max(1,int(w*h/180)),seed)


def tree(c,x,y,h=70,season='green',night=False):
 # A connected crown, exposed trunk, then clipped hand-sized leaf clusters.
 rr=random.Random(x*11+y*3+h)
 if night: shades=['green0','green1','green2']
 elif season=='autumn': shades=['gold0','gold1','gold2','gold3']
 else: shades=['green1','green2','green3','green4']
 w=int(h*.75); c.p([(x+w//2-4,y+h),(x+w//2-3,y+30),(x+w//2+4,y+30),(x+w//2+6,y+h)],'brown1')
 c.l([(x+w//2-1,y+h-2),(x+w//2-1,y+h*.57)],'brown3',2)
 for xx,yy in [(x+w//2-18,y+h*.46),(x+w//2+20,y+h*.42)]:c.l([(x+w//2,y+h-21),(xx,yy)],'brown1',4)
 ch=int(h*.7);mask=Image.new('L',(w+14,ch+5));md=ImageDraw.Draw(mask)
 for box in [(6,12,w-3,ch-6),(0,ch//3,w//2+15,ch-4),(w//3,0,w-11,ch//2+8),(w//2-8,ch//4,w+8,ch-9),(w//5,4,w*3//4,ch-2)]:md.ellipse(box,fill=255)
 foliage=Canvas(w+14,ch+5,shades[0]);foliage.r(0,0,w+14,ch+5,shades[0])
 for _ in range(max(80,int(h*1.2))):
  xx=rr.randrange(0,w+10);yy=rr.randrange(0,ch);sz=rr.randrange(5,16)
  bright=yy<ch*.5 and xx<w*.65
  col=rr.choice(shades[1:]) if bright else rr.choice(shades[:3])
  foliage.p([(xx,yy+2),(xx+3,yy),(xx+sz-3,yy),(xx+sz,yy+3),(xx+sz-2,yy+6),(xx+3,yy+7),(xx,yy+5)],col)
  if bright and rr.random()>.5:foliage.l([(xx+3,yy+1),(xx+sz-4,yy+1)],shades[-1])
  if rr.random()>.75:foliage.dot(xx+2,yy+3,shades[0])
 foliage.im.putalpha(mask);c.paste(foliage.im,x-3,y)


def plant(c,x,y,s=1):
 # Terracotta with individual leaves, rim and soil.
 c.e(x-3*s,y+23*s,31*s,8*s,'brown0')
 c.p([(x,y+12*s),(x+25*s,y+12*s),(x+21*s,y+28*s),(x+5*s,y+28*s)],'brown3')
 c.p([(x+2*s,y+14*s),(x+10*s,y+14*s),(x+10*s,y+26*s),(x+5*s,y+25*s)],'brown4')
 c.e(x-1*s,y+10*s,27*s,6*s,'brown4');c.e(x+2*s,y+10*s,21*s,4*s,'brown1')
 for ex,ey in [(2,-7),(10,-16),(20,-11),(30,-3),(2,1),(23,6)]:
  c.l([(x+13*s,y+12*s),(x+ex*s,y+ey*s)],'green1',max(1,s))
  c.p([(x+ex*s,y+ey*s),(x+(ex-7)*s,y+(ey-4)*s),(x+(ex-10)*s,y+(ey-1)*s),(x+(ex-5)*s,y+(ey+4)*s)],'green2')
  c.l([(x+(ex-7)*s,y+(ey-2)*s),(x+ex*s,y+ey*s)],'green3',s)


def landscape(c,box,night=True):
 x,y,w,h=box;c.r(x,y,w,h,'navy' if night else 'blue3')
 c.r(x,y+h*.55,w,h*.45,'blue0' if night else 'blue2')
 rr=random.Random(int(x+y+w))
 if night:
  for _ in range(45):c.dot(rr.randrange(int(x),int(x+w)),rr.randrange(int(y),int(y+h*.55)),rr.choice(['blue2','blue3']))
 for depth in range(2):
  pts=[(x,y+h)]
  for xx in range(int(x),int(x+w)+15,15):pts.append((xx,y+h*.5+rr.randrange(-12,15)+depth*12))
  pts.extend([(x+w,y+h),(x,y+h)]);c.p(pts,'blue0' if depth==0 else 'navy')
 for xx in range(int(x)+5,int(x+w)-25,28):
  by=y+h-rr.randrange(7,23); hh=rr.randrange(7,15)
  c.r(xx,by,20,hh,'ink' if night else 'green1');c.p([(xx-2,by),(xx+8,by-5),(xx+22,by)],'navy')
  for wx in [xx+4,xx+12]:c.r(wx,by+3,3,3,'gold2' if night else 'blue3')


def window(c,box,night=True):
 x,y,w,h=box
 c.r(x-4,y-4,w+8,h+8,'brown0');c.r(x-2,y-2,w+4,h+4,'cream0');c.r(x,y,w,h,'gray0')
 landscape(c,(x+4,y+4,w-8,h-8),night)
 c.l([(x+1,y+h-1),(x+w-1,y+h-1),(x+w-1,y+2)],'cream2')
 c.l([(x+4,y+4),(x+w-5,y+4)],'ink',2)
 c.l([(x+7,y+9),(x+7,y+h-12)],'blue2')
 for i in range(3):c.l([(x+12+i,y+10),(x+5+i,y+h-10)],'blue1' if night else 'blue4')
 c.r(x+int(w*.57),y+2,5,h-4,'gray0');c.r(x+int(w*.57)+1,y+3,1,h-7,'gray2')
 c.r(x+3,y+h*.6,w-6,3,'gray0');c.r(x+4,y+h*.6, w-8,1,'gray1')


def bird(c,x,y,s=1):
 # Original small rounded blue bird, five-tone stepped feather silhouette.
 pts=[(1,21),(6,20),(8,16),(8,11),(11,7),(15,5),(22,5),(27,9),(28,13),(33,15),(28,18),(26,25),(20,29),(11,28),(7,25),(2,25)]
 c.p([(x+a*s,y+b*s) for a,b in pts],'blue0')
 for pts2,col in [([(9,16),(10,11),(13,8),(21,7),(25,10),(25,16),(22,21),(11,23)],'blue2'), ([(10,20),(15,24),(21,23),(25,19),(24,25),(20,27),(12,26)],'blue3'), ([(12,16),(17,13),(22,15),(21,20),(16,23),(11,20)],'blue1'), ([(13,15),(18,15),(20,17),(16,20),(13,19)],'blue0')]:c.p([(x+a*s,y+b*s)for a,b in pts2],col)
 c.r(x+22*s,y+11*s,2*s,3*s,'ink');c.dot(x+22*s,y+11*s,'cream4')
 c.p([(x+27*s,y+14*s),(x+34*s,y+16*s),(x+27*s,y+18*s)],'gold2')
 c.l([(x+12*s,y+29*s),(x+11*s,y+32*s),(x+15*s,y+32*s)],'brown2',s)
 c.l([(x+22*s,y+28*s),(x+23*s,y+31*s),(x+27*s,y+31*s)],'brown2',s)


def bust(who='ivy', outfit='default'):
 c=Canvas(104,150,transparent=True)
 hair=(['gold0','gold1','gold2','gold3'] if who=='ivy' else ['brown0','brown1','brown2','brown3'] if who=='maya' else ['ink','brown0','brown1','brown2'])
 top=['plum0','plum1','plum2','plum3','plum4'] if who=='ivy' else (['green0','green1','green2','green3','green4'] if who=='maya' else ['brown1','gold0','gold1','gold2','gold3'])
 if who=='ivy' and outfit=='travel':top=['brown1','red0','red1','red2','red3']
 if who=='ivy' and outfit=='home':top=['blue0','blue1','blue2','blue3','blue4']
 if who=='ivy' and outfit=='outdoor':top=['green0','green1','green2','green3','green4']
 # Shoulder outline and draped fabric are deliberately asymmetric.
 c.p([(8,150),(8,112),(13,101),(29,92),(38,88),(65,89),(76,94),(91,105),(98,124),(100,150)],'ink')
 c.p([(12,150),(12,114),(17,104),(33,96),(41,94),(64,94),(75,100),(86,107),(93,127),(95,150)],top[2])
 c.p([(12,119),(19,109),(23,111),(25,150),(12,150)],top[1]);c.p([(76,102),(85,109),(91,129),(94,149),(77,149),(72,123)],top[1])
 c.p([(24,107),(33,99),(41,101),(62,101),(67,109),(66,138),(28,137)],top[3])
 c.p([(29,139),(65,140),(72,150),(27,150)],top[2])
 for pts in [[(24,118),(27,128),(26,145)],[(71,114),(68,127),(70,136)],[(34,133),(44,136),(52,134)],[(16,138),(21,137),(23,140)]]:c.l(pts,top[1])
 for pts in [[(23,105),(31,100),(34,100)],[(29,115),(30,128)],[(79,119),(81,130)],[(39,141),(57,141)]]:c.l(pts,top[4])
 # Hair behind face, then ears and neck.
 silhouette=[(26,13),(37,7),(58,6),(73,11),(82,23),(85,42),(82,66),(77,79),(68,86),(29,85),(19,76),(15,55),(16,32),(20,22)]
 if who in ('nora','ivy'):silhouette=[(25,14),(36,7),(60,7),(75,15),(82,30),(82,60),(86,92),(76,110),(67,97),(30,99),(19,108),(15,86),(18,57),(17,33)]
 c.p(silhouette,hair[0]);c.p([(25,22),(36,12),(57,10),(71,15),(78,26),(79,55),(74,76),(62,81),(31,78),(22,61),(21,38)],hair[1])
 if who=='maya':
  for x,y,r in [(19,18,14),(12,31,13),(11,47,13),(15,61,16),(21,73,13),(65,12,13),(74,23,15),(77,41,13),(76,58,14),(69,72,15)]:
   c.e(x,y,r,r,hair[0]);c.l([(x+3,y+3),(x+r-6,y+2),(x+r-3,y+5)],hair[2])
 c.e(21,40,10,19,'skin1');c.e(72,40,10,19,'skin0');c.l([(24,46),(27,45),(26,54)],'skin3')
 c.p([(39,70),(64,70),(65,91),(71,96),(61,107),(47,109),(33,96),(39,91)],'skin2')
 c.p([(40,72),(63,73),(62,83),(51,88),(40,84)],'skin0');c.p([(43,82),(60,84),(59,96),(48,101),(41,94)],'skin3')
 # Skin planes, chamfered outline, cheeks, chin and warm-left highlight.
 c.p([(29,27),(39,19),(58,20),(71,28),(75,42),(73,61),(67,72),(58,79),(45,80),(34,73),(28,62),(26,43)],'skin1')
 c.p([(31,29),(40,23),(58,24),(68,31),(70,44),(68,62),(62,73),(53,77),(43,75),(34,67),(30,55)],'skin2')
 c.p([(32,34),(39,27),(50,26),(53,35),(49,48),(51,61),(45,69),(36,64),(32,53)],'skin3')
 c.l([(33,33),(36,29),(40,27)],'skin4');c.r(33,54,5,2,'skin4');c.r(37,63,5,2,'skin3')
 # Eye sockets, eyebrows, eyes and single-pixel highlights.
 c.l([(34,40),(39,38),(44,39)],hair[1]);c.l([(57,39),(62,38),(67,40)],hair[1])
 c.l([(33,45),(36,43),(43,44),(45,46)],'skin0');c.l([(57,45),(61,43),(67,44),(69,46)],'skin0')
 c.r(35,45,9,4,'cream3');c.r(59,45,8,4,'cream3');c.r(38,44,4,6,'blue1' if who=='ivy' else 'green2' if who=='nora' else hair[0]);c.r(61,44,4,6,'blue1' if who=='ivy' else 'green2' if who=='nora' else hair[0]);c.dot(39,45,'white');c.dot(62,45,'cream4')
 if who=='maya':
  c.l([(34,39),(44,40)],hair[0]);c.l([(57,40),(67,39)],hair[0]);c.l([(35,44),(43,44)],hair[0]);c.l([(59,44),(67,44)],hair[0])
 elif who=='nora':
  c.l([(34,40),(38,39),(44,40)],hair[0]);c.l([(58,40),(62,39),(67,41)],hair[0]);c.r(38,45,4,6,'green2');c.r(61,45,4,6,'green2');c.dot(39,46,'cream3');c.dot(62,46,'cream3')
 c.l([(35,50),(43,50)],'skin0');c.l([(59,50),(67,50)],'skin0')
 c.l([(52,48),(51,55),(54,57)],'skin1');c.r(50,56,2,1,'skin4');c.r(52,59,4,1,'skin0')
 c.r(33,56,6,2,'red3');c.r(65,56,5,2,'red2')
 c.l([(44,65),(48,66),(55,66),(59,64)],'skin0');c.l([(48,68),(55,68)],'skin3');c.dot(59,64,'red1')
 if who=='maya':c.l([(44,64),(48,66),(54,66),(59,63)],'red0');c.l([(47,65),(55,65)],'cream3')
 elif who=='nora':c.l([(44,65),(49,66),(55,66),(58,65)],'skin2');c.l([(47,66),(56,66)],'skin0')
 # Bangs break the forehead silhouette, strand bundles catch left lamp.
 bangs=[(22,32),(24,21),(32,15),(48,12),(65,15),(74,22),(77,37),(68,35),(65,28),(60,25),(53,31),(48,34),(45,27),(39,33),(32,36),(27,42),(25,57),(21,55)]
 c.p(bangs,hair[1]);c.p([(26,27),(31,20),(42,17),(56,16),(62,18),(47,20),(39,25),(32,31),(27,35)],hair[2])
 c.l([(29,25),(34,21),(43,19)],hair[3]);c.l([(27,31),(30,27),(37,23)],hair[3]);c.l([(48,16),(58,17),(66,21)],hair[2])
 c.l([(22,37),(21,52),(24,68),(29,77)],hair[2],2);c.l([(23,47),(24,61),(27,68)],hair[3])
 c.l([(77,38),(77,55),(73,69),(70,74)],hair[2]);c.l([(73,29),(76,36),(77,44)],hair[0],2)
 if who in ('nora','ivy'):
  c.p([(21,55),(27,69),(32,78),(30,91),(24,103),(19,100),(17,85)],hair[1]);c.l([(21,67),(23,87),(21,96)],hair[2]);c.l([(77,59),(76,87),(79,98)],hair[2],2)
 if who=='maya':
  for x,y in [(23,18),(32,13),(44,12),(58,15),(69,22),(20,31),(73,34)]:
   c.e(x,y,12,9,hair[1]);c.l([(x+3,y+2),(x+7,y+1),(x+9,y+3)],hair[2])
  c.e(74,59,4,6,'gold2');c.dot(75,60,'gold4')
 # Collar and garment signatures.
 if who=='ivy':
  c.p([(34,93),(43,99),(52,102),(62,98),(68,92),(68,98),(61,109),(46,111),(36,103)],'cream2')
  c.l([(37,96),(45,104),(52,106),(60,103),(65,96)],'cream4',2)
  for y in range(117,149,5):c.dot(51,y,top[4]);c.dot(52,y+1,top[1])
 elif who=='maya':
  c.p([(31,96),(39,91),(48,104),(43,117)],top[4]);c.p([(66,92),(75,99),(62,116),(55,106)],top[3]);c.l([(50,109),(53,149)],top[0],2)
  c.r(65,122,14,11,top[1]);c.l([(65,123),(77,123)],top[4]);c.dot(56,128,'gold2')
 else:
  c.p([(32,96),(40,91),(49,107),(43,121)],top[3]);c.p([(65,92),(75,98),(63,120),(54,108)],top[2]);c.l([(52,111),(54,149)],top[0],2)
  c.r(64,128,14,9,top[0]);c.l([(65,128),(77,128)],top[3]);c.r(37,114,9,32,'cream1');c.r(39,114,3,32,'cream3')
 return c.im


def seat(c,x,y,w=100,h=111):
 c.p([(x+3,y+h),(x,y+12),(x+5,y+3),(x+12,y),(x+w-10,y),(x+w-3,y+5),(x+w,y+h)],'ink')
 fabric(c,(x+5,y+7,w-10,h-10),'plum1','plum0','plum2',x)
 c.p([(x+10,y+12),(x+15,y+8),(x+w-17,y+8),(x+w-11,y+13),(x+w-12,y+38),(x+12,y+38)],'cream1')
 c.r(x+15,y+11,w-32,2,'cream3');c.r(x+13,y+36,w-26,2,'cream0')
 for yy in range(y+15,y+35,4):c.l([(x+18,yy),(x+w-20,yy)],'cream2')
 c.l([(x+13,y+45),(x+14,y+h-10)],'plum3');c.l([(x+w-15,y+46),(x+w-16,y+h-9)],'plum0',2)
 for yy in range(y+48,y+h-8,12):
  for xx in range(x+24,x+w-18,18):
   c.l([(xx,yy),(xx+8,yy+5),(xx,yy+10),(xx-8,yy+5),(xx,yy)],'plum2');c.dot(xx,yy+5,'plum0')
 c.p([(x,y+h-11),(x+w,y+h-11),(x+w+6,y+h),(x-5,y+h)],'plum2');c.l([(x+2,y+h-10),(x+w-2,y+h-10)],'plum3')


def train_bg():
 c=Canvas(bg='brown1');wood(c,(0,0,320,150),40,True)
 c.r(0,0,320,18,'cream0');c.r(0,0,320,3,'cream3');c.r(0,16,320,3,'brown0');c.r(0,19,320,2,'brown3')
 c.r(13,6,292,3,'gold2');c.r(20,6,278,2,'gold4')
 window(c,(16,31,286,92),True)
 # Rain/weather lines and pale light strip reflected in the broad pane.
 c.l([(31,40),(145,40)],'blue2');c.l([(32,42),(142,42)],'blue1')
 for x in [23,306]:c.r(x,24,2,127,'brown4');c.r(x+2,25,1,125,'brown0')
 c.r(1,140,318,2,'cream0');c.r(0,142,320,58,'plum0')
 seat(c,35,99,108,101);seat(c,188,99,108,101)
 c.p([(144,180),(177,180),(181,191),(177,197),(143,196)],'gray0');c.r(146,181,28,3,'gray2');c.r(153,187,3,13,'ink')
 return c


def selfie(nora=False):
 # Portrait-format handheld photo; the empty seat and scarf stay fixed in both versions.
 c=Canvas(320,426,'brown1');wood(c,(0,0,320,245),40,True)
 c.r(0,0,320,25,'brown0');c.r(10,4,300,8,'gold1');c.r(20,7,278,3,'gold4')
 window(c,(8,36,150,150),True)
 c.r(162,27,148,166,'brown2');c.r(164,28,144,3,'brown4');grainseed=42
 for x in range(170,308,22):c.r(x,32,1,151,'brown1')
 seat(c,13,176,137,239);seat(c,169,176,137,239)
 # Scarf on the right seat is visible before and after the reveal.
 c.p([(181,357),(224,350),(269,365),(281,395),(264,402),(220,389),(183,393)],'red1');c.l([(185,360),(225,354),(269,369)],'red3',3)
 ivy=bust('ivy','travel').resize((158,228),Image.Resampling.NEAREST);c.paste(ivy,34,170)
 # One sleeve and forearm reach toward the camera; the phone remains out of frame.
 if nora:
  person=bust('nora').resize((137,198),Image.Resampling.NEAREST);c.paste(person,175,193)
  # Scarf stays in front of her lower coat rather than disappearing.
  c.p([(183,376),(204,375),(226,383),(233,399),(216,397),(196,390),(181,393)],'red1');c.l([(185,379),(203,378),(222,385)],'red3',2)
 # An angled sleeve and forearm extend toward the out-of-frame camera.
 c.p([(130,341),(146,345),(160,365),(188,415),(183,426),(158,426),(140,387),(121,361)],'red1')
 c.p([(146,365),(157,370),(183,415),(179,426),(160,426),(151,401),(137,376)],'skin2')
 c.l([(145,378),(156,383),(169,406)],'skin3',2)
 return c

def plate(c,x,y,w,h):
 c.e(x-2,y+4,w+4,h,'brown1');c.e(x,y,w,h,'cream1');c.e(x+2,y,w-4,h-3,'cream4');c.e(x+7,y+4,w-14,h-11,'cream2');c.e(x+11,y+7,w-22,h-17,'cream3');c.l([(x+16,y+h-5),(x+w-16,y+h-5)],'cream4')


def mug(c,x,y,w=43,h=47,col='blue2'):
 c.e(x-8,y+h-3,w+19,12,'brown1');c.e(x-5,y+h-5,w+13,10,'cream2');c.e(x-1,y+h-5,w+6,6,'cream3')
 background=c.im.copy();c.e(x+w-5,y+8,19,h-17,col)
 mask=Image.new('L',c.im.size);ImageDraw.Draw(mask).ellipse((x+w-1,y+12,x+w+9,y+h-14),fill=255);c.im.paste(background,(0,0),mask);c.d=ImageDraw.Draw(c.im)
 c.p([(x,y+6),(x+w,y+6),(x+w-4,y+h-4),(x+w-9,y+h),(x+7,y+h),(x+2,y+h-5)],col)
 c.p([(x+3,y+10),(x+8,y+11),(x+8,y+h-5),(x+5,y+h-8)],'blue3' if col.startswith('blue') else 'cream4')
 c.p([(x+w-7,y+11),(x+w-2,y+9),(x+w-5,y+h-5),(x+w-10,y+h-2)],'blue1' if col.startswith('blue') else 'cream1')
 c.e(x-1,y,w+2,14,'cream3');c.e(x+2,y+2,w-4,9,'brown0');c.e(x+4,y+3,w-8,6,'brown2');c.l([(x+8,y+4),(x+w-12,y+4)],'brown4')
 c.dot(x+10,y+5,'gold3');c.dot(x+w-9,y+7,'brown5')


def breakfast():
 c=Canvas(bg='cream1');wood(c,(0,0,320,200),7)
 # A draped blue linen napkin breaks up the warm tabletop.
 c.p([(211,23),(291,36),(307,177),(205,169),(191,83)],'blue1');c.l([(214,27),(286,41),(301,171)],'blue3')
 for yy in range(40,169,6):c.l([(211,yy),(293,yy+12)],'blue2')
 for xx in range(215,292,8):c.l([(xx,43),(xx-3,162)],'blue0')
 # Broad diagonal window light is a stepped area of lighter wood, not a blur.
 c.p([(0,0),(56,0),(179,200),(108,200)],'brown4');c.tex((0,0,150,200),['brown3','brown5'],300,11,'grain')
 c.p([(0,0),(43,0),(168,200),(153,200)],'brown5')
 plate(c,22,53,173,123)
 # Thick irregular slice of toast, toasted rim and fine porous crumb.
 c.p([(46,76),(50,69),(61,65),(99,65),(108,69),(113,76),(109,90),(117,130),(112,140),(57,144),(51,137),(47,95)],'brown1')
 c.p([(49,77),(55,70),(64,68),(96,68),(105,72),(109,79),(105,91),(113,130),(108,136),(59,141),(55,136),(51,94)],'brown3')
 c.p([(54,78),(60,74),(95,73),(103,78),(100,91),(108,130),(103,133),(61,136),(57,130),(57,95)],'gold3')
 c.tex((61,78,37,53),['gold2','brown4','cream3'],180,12)
 c.r(69,94,23,13,'gold4');c.p([(70,94),(88,92),(93,95),(91,105),(70,107)],'cream4');c.l([(72,95),(88,94)],'white')
 # Fried egg with irregular cooked white and lifted crispy edges.
 c.p([(126,84),(139,80),(151,85),(158,94),(170,98),(174,110),(168,123),(159,128),(149,140),(135,139),(129,131),(119,126),(115,115),(120,103),(120,93)],'gold2')
 c.p([(128,86),(139,83),(148,86),(155,96),(167,101),(171,110),(165,120),(155,125),(148,136),(136,135),(129,127),(120,123),(119,113),(124,104),(124,93)],'cream4')
 c.e(132,99,28,28,'gold1');c.e(133,98,27,27,'gold2');c.e(135,99,22,21,'gold3');c.e(138,100,13,9,'gold4');c.r(139,101,6,2,'white');c.l([(137,122),(151,122)],'gold1')
 for x,y in [(124,116),(161,112),(139,130),(128,96),(166,106)]:c.dot(x,y,'gold3')
 mug(c,221,36,53,58,'blue1')
 # Silver cutlery has solid silhouettes with hard specular pixels.
 c.p([(227,120),(232,120),(230,172),(227,181),(224,180)],'gray0');c.l([(229,122),(226,178)],'gray3',2)
 c.r(225,106,10,19,'gray2')
 for xx in [226,229,232]:c.r(xx,103,1,17,'cream4');c.r(xx+1,103,1,12,'blue0')
 c.p([(258,110),(264,110),(266,142),(261,147),(259,177),(255,181),(252,178),(255,143)],'gray2');c.l([(260,112),(263,139),(259,145),(257,177)],'cream3')
 # Glass jam jar and half-open lid in the background.
 c.e(26,12,39,11,'gray0');c.r(28,17,35,28,'red0');c.e(28,36,35,10,'red1');c.r(32,20,4,21,'red2');c.r(42,25,17,12,'cream2');c.r(43,26,15,9,'cream4');c.text('JAM',43,25,'red1')
 c.e(27,9,37,11,'gold0');c.e(28,8,35,9,'gold2');c.l([(35,10),(55,10)],'gold4')
 for x,y in [(39,171),(91,180),(116,165),(177,73),(194,157),(184,145)]:c.r(x,y,2,1,'gold3')
 return c


def desk():
 c=Canvas(bg='plum1');wood(c,(0,0,320,118),35,True)
 window(c,(183,9,122,92),True)
 # Pinboard, layered notes and tiny blue-bird sketch.
 c.r(14,13,101,68,'brown0');c.r(17,16,95,62,'brown3');c.tex((18,17,92,58),['brown2','brown4'],180,4)
 c.p([(24,25),(55,21),(59,59),(29,62)],'cream2');c.p([(60,23),(97,28),(95,61),(59,57)],'cream3');c.l([(65,48),(73,34),(80,43),(85,37),(92,51)],'blue2');c.e(68,28,5,5,'gold2')
 for y in [32,38,44]:c.l([(30,y),(49,y-1)],'cream0')
 for x,y in [(40,25),(79,29)]:c.e(x,y,3,3,'red1');c.dot(x,y,'red3')
 # Desk perspective, fascia and separate warm lamplight footprint.
 c.p([(0,115),(320,112),(320,200),(0,200)],'brown0');wood(c,(0,118,320,82),9)
 c.p([(0,130),(69,120),(129,200),(0,200)],'brown4');c.tex((2,135,95,63),['brown3','brown5'],150,11,'grain')
 c.r(0,194,320,6,'brown1');c.r(0,194,320,2,'brown4')
 # Monitor and detailed desktop UI as material, not a standalone webpage.
 c.p([(110,41),(228,43),(225,137),(108,134)],'ink');c.p([(114,45),(224,47),(221,130),(112,128)],'gray1')
 c.p([(119,50),(219,52),(216,123),(117,121)],'blue0');c.r(121,53,94,64,'blue1')
 c.r(121,53,94,7,'blue3');c.r(123,55,4,3,'cream3');c.r(130,55,29,1,'blue0')
 c.r(127,64,82,48,'cream2');c.r(128,65,80,7,'plum2');c.r(130,75,8,31,'gray3');c.r(194,75,12,31,'gray2')
 for x in [132,140,148,156,164,172,180,188,196]:c.r(x,67,3,3,'cream3')
 c.r(196,77,8,4,'cream3');c.r(196,84,8,4,'blue2');c.r(196,91,8,4,'cream3');c.r(197,99,6,5,'gold2')
 for yy,col in [(77,'blue1'),(84,'blue2'),(91,'gold2'),(98,'green2')]:c.r(132,yy,4,4,col)
 c.r(141,75,51,32,'cream3');bird(c,147,75,1);c.r(177,103,10,2,'blue1')
 c.r(119,117,97,5,'gray2');c.r(121,119,12,1,'cream2');c.r(214,126,4,2,'green3')
 c.p([(158,134),(178,135),(181,151),(153,151)],'gray0');c.e(141,148,54,7,'gray1');c.l([(146,149),(185,150)],'gray2')
 # Drawing tablet with actual bezel, buttons and a resting stylus.
 c.p([(111,155),(198,155),(218,187),(121,190)],'ink');c.p([(117,159),(193,159),(208,183),(125,186)],'gray0');c.p([(126,161),(188,162),(198,180),(132,182)],'plum1')
 for yy in [163,169,175]:c.r(119+(yy-163)//3,yy,4,2,'gray2')
 c.l([(148,165),(198,150)],'brown0',4);c.l([(149,164),(195,150)],'cream0',2);c.dot(198,149,'cream4')
 # Layered sketch sheets, pencil contours and hand-drawn small face.
 c.p([(24,143),(83,135),(104,176),(39,185)],'brown1');c.p([(23,140),(81,132),(101,173),(39,181)],'cream2');c.p([(30,143),(78,137),(94,170),(43,176)],'cream3')
 c.e(50,144,20,20,'cream0');c.e(53,146,15,16,'cream3');c.l([(54,147),(59,144),(67,148)],'blue1');c.l([(47,166),(53,163),(68,162),(80,169)],'blue1');c.r(57,153,2,1,'blue1');c.r(64,152,2,1,'blue1')
 c.l([(41,171),(84,164)],'brown2',3);c.l([(42,170),(84,163)],'gold3')
 # Adjustable brass lamp: jointed arm, shade, bulb and base.
 c.e(5,137,34,10,'brown1');c.e(7,136,30,7,'gold0');c.l([(20,137),(27,92),(35,65)],'ink',5);c.l([(19,136),(26,93),(34,66)],'gold1',2);c.e(23,88,7,7,'gold2')
 c.p([(17,61),(47,59),(57,75),(8,79)],'gold0');c.p([(19,61),(45,61),(51,71),(13,74)],'gold2');c.l([(20,62),(43,62)],'gold4');c.l([(12,77),(54,73)],'gold3',2)
 # Pen cup, rubber, cable, coffee, scattered supplies.
 c.l([(210,137),(236,145),(250,153),(274,151)],'brown0',2)
 c.e(261,125,28,8,'blue0');c.r(262,129,26,24,'blue1');c.e(262,148,26,8,'blue0');c.l([(264,131),(264,149)],'blue3')
 for x,y,col in [(266,100,'gold2'),(273,95,'red1'),(279,104,'cream2'),(285,99,'plum3')]:c.l([(x,y),(x-2,137)],'ink',3);c.l([(x,y),(x-2,134)],col)
 c.r(230,176,16,6,'red2');c.r(230,176,9,6,'cream2')
 return c


def portrait(who):
 c=Canvas(104,120,bg='blue0' if who=='nora' else ('plum1' if who=='ivy' else 'green1'))
 c.tex((0,0,104,120),['blue1' if who=='nora' else ('plum2' if who=='ivy' else 'green2')],220,11)
 c.paste(bust(who),0,-1);return c


def nora_seated():
 c=Canvas(112,150,transparent=True)
 # Three-quarter profile, knees forward; independent full-body silhouette.
 c.p([(39,55),(52,55),(63,65),(65,86),(61,97),(88,100),(95,108),(94,134),(83,138),(76,130),(77,115),(47,116),(33,107),(28,87),(29,67)],'ink')
 c.p([(39,59),(50,58),(59,67),(62,85),(58,99),(38,103),(31,94),(31,75)],'gold1')
 c.p([(36,65),(43,63),(48,73),(46,94),(38,99),(33,90)],'gold2')
 c.l([(32,73),(33,89),(37,96)],'gold3');c.l([(53,69),(57,80),(56,94)],'gold0',2)
 c.p([(41,98),(60,100),(88,103),(91,109),(87,117),(71,115),(54,111),(39,111),(33,106)],'blue0')
 c.p([(53,102),(86,106),(88,110),(70,110),(55,108)],'blue1')
 c.p([(83,110),(91,112),(90,135),(82,137),(79,133),(80,118)],'navy');c.l([(84,119),(84,132)],'blue1')
 c.p([(49,110),(60,112),(57,128),(58,137),(49,142),(43,137),(43,129)],'navy');c.l([(49,115),(48,130)],'blue0')
 c.p([(82,132),(90,132),(94,139),(104,143),(105,147),(81,147),(78,143)],'brown0');c.l([(83,135),(89,135),(94,142),(102,144)],'brown2');c.l([(80,147),(104,147)],'gray0')
 c.p([(47,134),(56,134),(59,140),(69,142),(71,147),(45,147),(42,143)],'brown0');c.l([(48,138),(55,138),(60,143),(67,144)],'brown2');c.l([(45,147),(70,147)],'gray0')
 # Slim neck and outlined head, nose points towards laptop at the right.
 c.p([(42,44),(54,43),(55,57),(61,63),(50,68),(40,57)],'skin1');c.p([(45,46),(51,47),(51,58),(55,61),(48,64),(43,56)],'skin3')
 c.p([(29,16),(36,8),(47,5),(58,9),(63,18),(61,36),(65,50),(62,67),(52,71),(43,64),(35,69),(27,56),(27,39)],'ink')
 c.p([(37,15),(48,11),(58,16),(60,28),(65,33),(62,36),(61,44),(54,51),(47,51),(39,44),(35,31)],'skin2')
 c.p([(44,16),(54,17),(56,27),(60,31),(59,40),(54,47),(48,45),(43,37)],'skin3')
 c.l([(56,27),(59,28)],'brown1');c.l([(56,31),(60,31)],'green2');c.dot(58,31,'cream3')
 c.l([(60,35),(64,34)],'skin0');c.l([(57,42),(61,41)],'skin0');c.r(53,36,4,2,'red3')
 c.p([(31,20),(36,12),(47,8),(57,12),(61,22),(56,23),(52,18),(47,24),(43,28),(41,40),(43,52),(40,65),(32,61),(29,46)],'brown0')
 c.l([(34,22),(39,16),(45,14),(51,15)],'brown2');c.l([(31,29),(31,45),(34,56),(36,61)],'brown1',2);c.l([(37,24),(35,31)],'brown2')
 c.e(40,31,6,10,'skin1');c.l([(42,33),(44,34),(43,38)],'skin3')
 # Bent right sleeve, cuff and small hand resting over the table edge.
 c.p([(52,69),(59,69),(67,79),(81,80),(84,87),(76,90),(61,87),(53,80)],'gold0')
 c.p([(54,70),(58,71),(65,82),(79,83),(79,87),(63,85),(55,78)],'gold2');c.l([(57,72),(65,81),(77,82)],'gold3')
 c.r(79,81,5,8,'cream1');c.p([(83,82),(91,82),(96,85),(96,88),(84,89)],'skin2');c.l([(85,84),(91,84),(94,86)],'skin4');c.l([(88,87),(94,88)],'skin1')
 c.p([(41,60),(46,64),(49,74),(43,78),(38,67)],'cream2');c.l([(42,62),(45,70)],'cream4')
 c.r(38,91,13,7,'gold0');c.l([(39,91),(50,91)],'gold3');c.dot(52,86,'brown0')
 return c


def nora_standing():
 c=Canvas(88,170,transparent=True)
 # Legs extend naturally from the coat; paired shoes have distinct perspective.
 c.p([(28,105),(43,106),(42,145),(38,158),(26,158),(27,141)],'ink')
 c.p([(45,106),(59,105),(62,141),(61,159),(48,159),(45,140)],'ink')
 c.p([(31,108),(40,110),(38,141),(34,155),(28,155),(30,139)],'blue0')
 c.p([(48,109),(56,108),(58,140),(57,155),(50,155),(49,138)],'navy')
 c.l([(33,114),(32,136),(30,147)],'blue1');c.l([(52,116),(54,135),(54,147)],'blue0')
 c.p([(26,153),(38,153),(38,162),(35,166),(18,166),(18,161)],'brown0');c.l([(27,156),(35,156),(34,163),(21,163)],'brown2')
 c.p([(49,153),(60,153),(63,160),(72,163),(72,167),(48,167),(47,162)],'brown0');c.l([(51,156),(58,156),(63,163),(69,164)],'brown2')
 upper=bust('nora').resize((76,110),Image.Resampling.NEAREST);c.paste(upper,5,0)
 # Narrow sleeves and visible hands beside coat.
 c.p([(12,88),(17,88),(19,109),(17,118),(13,118),(11,113)],'skin2');c.l([(13,93),(14,112)],'skin3')
 c.p([(73,88),(78,88),(79,110),(76,119),(72,116)],'skin1');c.l([(74,94),(75,111)],'skin3')
 return c


def mirror_morning():
 # Bathroom mirror photograph: tile wall and ceramic sink share a shallow downward view.
 c=Canvas(bg='cream2');c.r(0,0,320,153,'cream3')
 for yy in range(4,155,25):
  c.r(0,yy,320,1,'cream1')
  for xx in range((yy//25%2)*24,320,48):c.r(xx,yy,1,24,'cream1')
 c.r(19,10,171,143,'gray0');c.r(22,13,165,137,'gray3');c.r(25,16,159,131,'blue3');c.r(28,19,153,125,'cream2')
 c.r(31,22,147,120,'cream3');c.r(135,23,39,93,'blue3');c.r(138,26,33,86,'blue4');c.r(153,26,2,86,'cream2')
 # Ivy is reflected, phone beside her face rather than in the lens view.
 c.paste(bust('ivy','home'),46,22)
 c.p([(122,101),(130,96),(137,98),(140,108),(136,121),(126,125),(120,117)],'skin1')
 c.p([(125,103),(130,100),(136,101),(137,110),(133,120),(127,120)],'skin3')
 c.r(122,68,20,37,'ink');c.r(124,70,16,33,'blue1');c.r(126,71,2,29,'blue3');c.r(135,72,3,6,'ink');c.dot(136,73,'cream4')
 c.l([(128,101),(136,102),(138,106)],'skin4',2)
 c.r(205,15,76,5,'gray2');c.r(216,20,4,40,'gray1');c.p([(210,32),(249,32),(247,77),(212,75)],'blue3');c.l([(214,36),(214,70),(242,72)],'blue4')
 # Rear counter edge, white ceramic counter and elliptical basin with inset drain.
 c.p([(0,149),(320,145),(320,200),(0,200)],'gray2');c.p([(0,143),(320,140),(320,190),(0,194)],'cream4')
 c.l([(0,145),(320,142)],'white',2);c.l([(0,192),(320,188)],'gray1',2)
 c.e(82,151,151,39,'gray1');c.e(85,149,145,37,'blue4');c.e(90,151,135,31,'cream4');c.e(100,153,116,23,'white');c.e(151,166,13,5,'gray1');c.e(154,166,7,3,'gray3')
 # Faucet arches over the bowl with visible dark gap under the spout.
 c.r(160,125,8,32,'gray0');c.r(162,124,5,27,'gray3');c.p([(163,124),(164,116),(170,112),(182,112),(188,116),(188,128),(182,128),(182,120),(179,118),(172,118),(170,123)],'gray1')
 c.l([(167,119),(171,115),(181,115),(185,119)],'white');c.e(181,125,9,5,'gray0');c.r(182,126,6,1,'gray3')
 # Toiletries remain separate, with cast shadows toward the right.
 c.e(17,166,38,8,'gray3');c.p([(20,140),(48,140),(45,164),(24,164)],'blue1');c.e(20,138,28,7,'blue3');c.e(23,139,22,4,'blue0')
 for x,col in [(26,'red2'),(33,'green3'),(40,'blue3')]:c.l([(x,141),(x-1,116)],col,2);c.r(x-3,113,5,4,'cream4')
 c.p([(248,142),(269,141),(273,164),(247,164)],'cream2');c.r(250,143,18,19,'cream4');c.r(253,149,11,8,'green3');c.r(252,137,15,6,'blue2')
 c.r(280,138,19,25,'cream3');c.r(283,134,13,5,'cream1');c.r(284,145,11,8,'red2');c.e(245,163,56,7,'gray3')
 return c


def coffee_shop():
 c=Canvas(bg='brown1');c.r(0,0,320,135,'cream1')
 window(c,(10,15,220,113),False)
 # A pedestrian street through a large divided shop window.
 c.r(15,79,210,43,'blue2')
 for x,y,w,col in [(17,45,48,'cream0'),(72,32,51,'brown2'),(133,49,43,'gray1'),(184,28,36,'green1')]:
  c.r(x,y,w,72-y,col);c.r(x,73,w,34,'gray0')
  for wx in range(x+7,x+w-5,13):
   c.r(wx,y+10,8,14,'blue3');c.l([(wx+1,y+11),(wx+1,y+20)],'cream2')
  c.r(x+4,76,w-8,5,'red1' if col=='brown2' else 'green2');c.r(x+8,85,w-16,19,'blue1')
 c.r(116,18,5,105,'brown1');c.r(119,19,1,103,'cream0');c.r(12,74,216,4,'brown1');c.r(13,74,214,1,'cream2')
 c.l([(22,23),(21,65)],'blue4');c.l([(27,22),(25,65)],'blue3');c.l([(152,27),(149,65)],'blue4')
 wood(c,(236,0,84,139),4,True);c.r(248,18,57,45,'brown0');c.r(251,21,51,39,'green0');c.text('COFFEE',258,28,'cream3');c.text('8 - 19',262,44,'cream1')
 c.l([(54,0),(54,19)],'ink',2);c.p([(41,19),(67,19),(78,36),(31,36)],'gold0');c.p([(42,20),(65,20),(73,32),(35,32)],'gold2');c.l([(35,35),(75,35)],'gold4',2)
 # Window seat, worn edge and warm pool of light.
 c.r(0,135,320,65,'brown0');wood(c,(0,137,320,63),16);c.r(0,137,320,2,'brown5')
 c.p([(17,140),(129,140),(168,200),(2,200)],'brown4');c.tex((18,153,113,43),['brown3','brown5'],55,14,'grain')
 mug(c,70,125,39,42,'cream3')
 # Open book has a valley, page thickness and asymmetric bent corner.
 c.p([(164,140),(202,136),(208,145),(246,143),(258,180),(211,185),(171,181)],'brown1')
 c.p([(163,137),(202,133),(207,141),(246,139),(254,176),(211,180),(169,176)],'cream2')
 c.p([(165,138),(200,135),(205,142),(210,178),(172,174)],'cream4');c.p([(208,143),(243,141),(250,174),(213,177)],'cream3');c.l([(205,143),(211,176)],'cream0')
 for y in [145,151,157,163]:c.l([(173,y),(199,y-3)],'cream1');c.l([(216,y),(242,y-2)],'cream1')
 c.p([(240,141),(244,153),(250,151)],'cream1')
 plant(c,277,113,1);c.r(286,142,1,45,'brown0')
 c.r(17,177,12,23,'brown0');c.r(21,178,2,22,'brown2');c.r(288,180,16,20,'brown0');c.l([(290,180),(290,199)],'brown3')
 return c


def books(c,x,y,w,h,seed=12):
 rr=random.Random(seed);xx=x
 cols=['blue1','green2','red1','plum2','brown4','gold1','cream1']
 while xx<x+w-5:
  ww=rr.randrange(5,12);hh=rr.randrange(int(h*.65),h);cc=rr.choice(cols)
  c.r(xx,y+h-hh,ww,hh,'brown0');c.r(xx+1,y+h-hh+1,ww-2,hh-1,cc);c.r(xx+2,y+h-hh+2,1,hh-3,'cream0')
  if ww>7:
   for yy in [y+h-hh+5,y+h-6]:c.r(xx+3,yy,ww-5,1,'cream2')
   for yy in range(y+h-hh+11,y+h-12,4):c.r(xx+ww//2,yy,1,2,'cream3')
  xx+=ww+1


def bookshop():
 c=Canvas(bg='brown0');wood(c,(0,0,320,155),3,True)
 for y in [8,56,108]:
  c.r(4,y,311,42,'brown0');books(c,10,y+3,300,36,y)
  c.r(0,y+41,320,6,'brown3');c.r(0,y+41,320,1,'brown5');c.r(0,y+47,320,2,'brown0')
 for x in [1,106,210,313]:c.r(x,0,5,156,'brown2');c.r(x,1,1,155,'brown4')
 # Foreground display table and two differently angled illustrated art books.
 wood(c,(0,157,320,43),51);c.r(0,156,320,2,'brown5')
 c.p([(22,150),(94,141),(111,191),(36,199)],'brown0');c.p([(23,146),(92,137),(107,186),(36,195)],'blue0')
 c.p([(29,151),(88,144),(99,176),(40,184)],'blue2');c.p([(35,178),(49,159),(62,169),(74,151),(95,174),(41,181)],'green1');c.p([(51,158),(54,163),(48,164)],'cream2')
 c.text('LANDSCAPES',42,182,'cream2')
 c.p([(121,143),(187,150),(182,194),(116,189)],'brown0');c.p([(121,140),(188,147),(183,190),(116,185)],'cream2')
 c.p([(130,148),(178,153),(174,179),(126,175)],'red1');c.e(142,151,24,26,'cream1');c.p([(145,163),(154,150),(164,160),(160,174),(148,175)],'plum1');c.text('PORTRAITS',128,177,'brown2')
 # Tiered postcard rack, each card a tiny independent landscape or bird.
 wood(c,(220,94,87,100),7,True)
 for row in range(2):
  for col in range(3):
   x=225+col*26;y=103+row*40;c.r(x,y,22,31,'cream3');c.r(x+2,y+2,18,23,'blue2' if col!=1 else 'red2')
   if col==0:c.p([(x+2,y+23),(x+10,y+8),(x+18,y+23)],'green2');c.e(x+13,y+5,4,4,'gold3')
   elif col==1:c.e(x+5,y+9,11,12,'cream2');c.r(x+6,y+7,9,4,'brown1')
   else:c.r(x+3,y+17,16,7,'blue0');c.r(x+8,y+8,5,12,'cream1');c.r(x+7,y+7,7,2,'red1')
   c.r(x+4,y+28,13,1,'cream0')
  c.r(221,133+row*40,86,4,'brown4');c.r(223,133+row*40,82,1,'brown5')
 return c


def rainy_window():
 c=Canvas(bg='blue0');c.r(0,0,320,200,'blue1')
 # Shapes remain visible through the cold pane; window lights form subdued blocks.
 for x,y,w,col in [(0,62,53,'blue0'),(60,22,61,'gray0'),(130,70,45,'navy'),(185,13,70,'blue0'),(269,45,51,'gray0')]:
  c.r(x,y,w,162-y,col)
  for xx in range(x+7,x+w-4,11):
   for yy in range(y+9,158,16):
    c.r(xx,yy,5,7,'blue2' if (xx+yy)%3 else 'gold1');c.r(xx,yy,1,7,'blue3')
 c.r(0,155,320,45,'blue0')
 for x in range(0,320,31):c.l([(x,157),(x-8,181)],'blue2');c.l([(x+4,160),(x-4,184)],'gold0')
 c.r(155,0,12,200,'brown0');c.r(158,0,3,198,'gray1');c.r(165,0,2,199,'gray2')
 c.r(0,175,320,25,'brown0');wood(c,(0,181,320,19),19,True);c.r(0,179,320,2,'cream0')
 rr=random.Random(89)
 for _ in range(93):
  x=rr.randrange(5,315);y=rr.randrange(2,167);h=rr.randrange(3,16)
  if 150<x<170:continue
  c.l([(x,y),(x-1,y+h)],'blue3');c.e(x-2,y+h-1,4,5,'blue0');c.dot(x-1,y+h,'blue4');c.dot(x+1,y+h+3,'navy')
 for x,y in [(35,18),(75,58),(136,33),(190,74),(250,19),(289,90)]:
  c.l([(x,y),(x-2,y+34),(x-1,y+55)],'blue2');c.l([(x+1,y+3),(x-1,y+31)],'blue3')
 # The sill is intentionally clear, with no cup.
 c.r(23,186,67,8,'plum0');c.r(25,184,63,6,'cream1');c.r(26,185,61,1,'cream3')
 return c


def neighborhood_cat():
 c=Canvas(bg='cream0');c.r(0,0,320,139,'cream1')
 for row in range(7):
  yy=row*20;c.r(0,yy,320,2,'gray1')
  for xx in range(-20 if row%2 else 0,320,49):
   c.r(xx,yy+1,2,19,'gray1');c.l([(xx+3,yy+3),(xx+45,yy+3)],'cream2')
   if row%2:c.l([(xx+7,yy+13),(xx+17,yy+13)],'cream0')
 c.r(0,140,320,60,'gray1');c.r(0,141,320,2,'cream1')
 for x in [12,89,172,262]:c.l([(x,143),(x-17,199)],'gray0')
 c.l([(0,170),(320,167)],'gray0');c.tex((0,144,320,56),['gray2','cream0','gray0'],220,71)
 # Raised terracotta pot and a large, leafy plant provide scale.
 c.e(236,163,36,11,'gray0');c.e(238,160,32,10,'cream2');c.e(241,161,26,6,'brown2')
 for x,y in [(245,163),(250,162),(255,164),(260,162)]:c.e(x,y,3,2,'gold1')
 c.e(276,161,35,11,'gray0');c.e(278,158,31,10,'cream2');c.e(281,160,25,5,'blue2');c.l([(285,161),(294,161)],'cream4')
 c.e(74,171,135,18,'gray0');c.e(86,163,104,15,'brown1')
 # Cat rounded haunches, chest, small forepaws, curved tail.
 c.p([(104,144),(109,123),(123,113),(147,111),(165,124),(173,148),(172,173),(157,180),(117,179),(103,171)],'brown2')
 c.p([(109,143),(116,126),(128,120),(147,120),(160,132),(165,151),(164,171),(151,175),(119,174),(109,167)],'brown4')
 c.p([(125,136),(143,134),(151,147),(147,172),(130,177),(118,169)],'cream2')
 c.p([(166,157),(179,153),(187,143),(187,132),(183,126),(187,122),(194,125),(197,136),(194,151),(183,165),(168,169)],'brown3')
 c.l([(174,160),(186,149),(190,140),(189,130)],'brown5',3)
 c.e(113,169,22,11,'brown5');c.e(144,169,23,11,'brown4')
 for x in [119,125,150,156]:c.l([(x,175),(x+1,179)],'brown2')
 # Ears have stepped silhouettes; face is slightly tilted and fully furred.
 c.p([(111,113),(108,86),(117,77),(132,94),(147,93),(165,76),(171,81),(168,112),(174,125),(169,139),(153,150),(130,150),(116,141),(108,126)],'brown2')
 c.p([(114,115),(113,91),(118,85),(131,100),(147,100),(164,84),(166,91),(163,116),(168,126),(164,136),(151,144),(132,144),(119,136),(114,125)],'brown5')
 c.p([(117,91),(126,103),(116,107)],'red2');c.p([(160,92),(162,109),(151,104)],'red1')
 c.p([(125,126),(139,124),(152,125),(159,133),(150,141),(132,141),(122,134)],'cream2')
 c.p([(120,115),(126,111),(135,114),(134,120),(127,123),(121,120)],'green1');c.p([(147,114),(155,110),(163,113),(161,119),(153,121),(147,119)],'green1')
 c.e(123,113,10,7,'green3');c.e(150,112,10,7,'green3');c.r(127,113,2,7,'ink');c.r(154,112,2,7,'ink');c.dot(125,114,'cream4');c.dot(152,113,'cream4')
 c.p([(136,127),(145,127),(141,132)],'red1');c.l([(141,131),(140,135),(135,137)],'brown2');c.l([(140,135),(145,137)],'brown2')
 for pts in [[(135,134),(119,130),(105,129)],[(134,137),(117,138),(102,142)],[(147,133),(162,129),(178,127)],[(148,136),(164,137),(180,142)]]:c.l(pts,'cream4')
 for pts in [[(135,99),(136,110)],[(143,99),(142,108)],[(116,120),(123,123)],[(163,120),(157,123)],[(112,149),(122,153)],[(159,147),(166,150)],[(114,160),(122,163)],[(183,150),(188,153)]]:c.l(pts,'brown2',2)
 c.l([(3,155),(9,145),(12,154),(15,143),(18,154)],'green2',2)
 return c


def night_walk():
 # A single vanishing point at (164,91) controls both street edges and pavement.
 c=Canvas(bg='navy');c.r(0,0,320,200,'navy');c.r(0,82,320,118,'blue0')
 c.tex((0,0,320,62),['blue1','blue2'],40,29)
 vx,vy=164,91
 # Far skyline remains low and recedes into the blue night instead of blocking the road.
 c.p([(0,80),(41,75),(68,82),(93,76),(116,84),(135,82),(150,88),(178,88),(202,83),(225,85),(250,77),(281,79),(320,72),(320,112),(0,112)],'blue1')
 c.p([(vx,vy),(320,159),(320,200),(0,200),(0,159)],'gray0')
 c.p([(vx,vy),(261,200),(70,200)],'blue0')
 c.p([(vx,vy),(70,200),(0,200),(0,162)],'gray1');c.p([(vx,vy),(320,159),(320,200),(261,200)],'gray1')
 for x in [0,31,62,96,127,291,320]:c.l([(vx,vy),(x,199)],'gray0')
 for depth in [.13,.24,.4,.61,.88]:
  yy=int(vy+(199-vy)*depth);left=int(vx+(0-vx)*depth);right=int(vx+(320-vx)*depth)
  c.l([(left,yy),(right,yy)],'gray0');c.l([(int(vx+(70-vx)*depth),yy),(int(vx+(261-vx)*depth),yy)],'blue1')
 for depth in [.18,.36,.62,.91]:
  yy=int(vy+(199-vy)*depth);c.r(vx-1,yy,2+int(depth*3),1+int(depth*2),'cream0')
 # Each facade narrows toward the shared point, with different heights, doors and roofs.
 c.p([(0,20),(92,54),(114,103),(0,140)],'blue0');c.p([(0,20),(11,13),(94,48),(92,54)],'blue1')
 c.p([(320,12),(235,49),(212,103),(320,139)],'blue0');c.p([(320,12),(309,7),(232,44),(235,49)],'blue1')
 for x,y,w,h in [(10,40,24,35),(45,55,18,29),(76,68,13,21),(247,61,17,26),(281,43,23,35)]:
  c.r(x,y,w,h,'ink');c.r(x+2,y+2,w-4,h-4,'gold1');c.r(x+4,y+3,w-8,h-7,'gold2');c.r(x+w//2,y+2,1,h-4,'brown1');c.r(x+2,y+h//2,w-4,1,'brown1')
 c.p([(11,90),(31,94),(32,129),(11,135)],'ink');c.p([(14,94),(28,97),(28,128),(14,131)],'brown2');c.r(25,112,2,2,'gold3')
 # Asymmetric tree silhouettes and a distinct foreground lamp with light on the pavement.
 tree(c,-28,63,84,night=True);tree(c,278,80,65,night=True)
 c.e(29,175,79,19,'gold0');c.e(42,178,50,11,'gold1');c.e(51,180,27,6,'gold2')
 c.r(61,53,4,132,'ink');c.r(62,55,1,128,'gray2');c.e(57,182,13,4,'ink')
 c.p([(56,51),(65,43),(74,51),(70,54),(59,54)],'ink');c.r(59,53,11,11,'gold3');c.r(61,54,7,8,'gold4');c.r(56,64,17,2,'gray0')
 c.r(206,83,2,34,'gray1');c.r(203,80,8,4,'gold3');c.r(136,86,1,16,'gray1');c.r(134,84,5,2,'gold2')
 return c


def birthday_cake():
 c=Canvas(bg='plum0');c.r(0,0,320,130,'plum1')
 # Small birthday bunting casts warm shadows on the wall.
 c.l([(0,10),(80,29),(164,35),(244,25),(320,5)],'gold0')
 for x,y,col in [(23,16,'red1'),(65,26,'gold1'),(112,32,'green2'),(158,35,'plum3'),(204,30,'blue2'),(251,24,'red2'),(294,12,'gold2')]:
  c.p([(x-9,y),(x+10,y+1),(x,y+17)],col);c.l([(x-6,y+2),(x+6,y+3)],'cream1')
 wood(c,(0,132,320,68),19,True);c.r(0,132,320,2,'brown4')
 plate(c,75,143,174,39)
 # Layer cake cylindrical perspective, cream drips and piped frosting.
 c.e(94,101,137,49,'brown1');c.r(94,122,137,33,'red1');c.e(94,134,137,38,'red1')
 c.e(96,127,133,36,'cream1');c.r(96,138,133,11,'cream1');c.e(96,121,133,37,'red2');c.r(97,123,131,10,'red2')
 c.e(95,101,135,48,'cream2');c.e(96,98,133,45,'cream3');c.e(103,104,119,32,'cream4')
 for x,y,h in [(99,123,16),(116,134,12),(136,139,15),(162,141,10),(185,138,16),(208,130,11),(223,120,12)]:
  c.r(x,y,5,h,'cream3');c.e(x,y+h-3,5,5,'cream3')
 for x,y in [(111,111),(128,104),(155,102),(184,105),(211,115),(204,132),(174,138),(143,138),(118,130)]:
  c.e(x-4,y-3,10,7,'cream1');c.e(x-3,y-5,8,8,'cream4');c.dot(x,y-4,'white')
 # Strawberries, seeds and green crowns.
 for x,y in [(121,115),(195,117)]:
  c.p([(x-5,y-3),(x+6,y-3),(x+8,y+2),(x+2,y+11),(x-4,y+7),(x-7,y+2)],'red0')
  c.p([(x-4,y-2),(x+5,y-2),(x+5,y+3),(x+1,y+8),(x-4,y+4)],'red2')
  c.l([(x-7,y-3),(x,y-1),(x+8,y-4)],'green2');c.l([(x-2,y-7),(x,y-1),(x+3,y-6)],'green3')
  for dx,dy in [(-2,1),(2,2),(0,5)]:c.dot(x+dx,y+dy,'gold3')
 for x,y,col in [(146,84,'blue2'),(166,79,'plum3'),(184,88,'red2')]:
  c.r(x,y,5,39,col);c.r(x+1,y,1,38,'cream3');c.r(x+2,y-4,1,5,'brown0')
  c.p([(x+2,y-17),(x+5,y-11),(x+5,y-7),(x+3,y-4),(x,y-5),(x-1,y-9)],'gold2');c.p([(x+2,y-13),(x+3,y-9),(x+2,y-5),(x+1,y-7)],'gold4')
 # Paper cups and a small birthday card.
 for x,y,col in [(36,119,'plum3'),(269,126,'green3')]:
  c.p([(x,y),(x+26,y),(x+22,y+37),(x+5,y+37)],col);c.e(x,y-3,27,8,'cream3');c.e(x+3,y-2,21,4,'brown1');c.l([(x+4,y+7),(x+7,y+30)],'cream2')
 c.p([(230,176),(280,171),(285,190),(235,194)],'cream3');c.text('FOR IVY',237,178,'red1')
 return c


def weekend_lake():
 c=Canvas(bg='blue3');c.r(0,0,320,87,'blue3');c.r(0,72,320,29,'blue2')
 # Angular cloud clusters, distant hills and multiple depths of the shore.
 for x,y,w in [(42,19,64),(211,28,55),(135,10,40)]:
  c.p([(x,y+8),(x+8,y+3),(x+22,y+3),(x+26,y),(x+39,y+1),(x+w-9,y+7),(x+w,y+7),(x+w,y+10),(x,y+10)],'blue4')
 c.p([(0,86),(34,67),(65,77),(112,54),(142,66),(176,61),(220,80),(257,62),(290,74),(320,65),(320,109),(0,109)],'green3')
 c.p([(0,96),(31,85),(62,92),(96,80),(124,84),(158,79),(190,91),(224,83),(265,89),(298,81),(320,93),(320,116),(0,116)],'green2')
 c.r(0,108,320,60,'blue2');c.r(0,112,320,1,'blue4')
 rr=random.Random(41)
 for _ in range(90):
  x=rr.randrange(0,320);y=rr.randrange(115,166);c.r(x,y,rr.randrange(3,21),1,rr.choice(['blue1','blue3','blue4']))
 c.p([(0,153),(54,160),(103,174),(161,181),(218,169),(275,156),(320,151),(320,200),(0,200)],'green1')
 c.p([(0,161),(47,169),(106,187),(174,190),(243,172),(320,163),(320,200),(0,200)],'green3')
 c.tex((0,179,320,21),['green2','green4','gold2'],250,9,'weave')
 tree(c,-12,30,137);tree(c,256,22,149)
 # Wooden bench facing the lake, bolts and cast shadow.
 c.p([(125,179),(185,178),(206,190),(141,193)],'green2')
 for y in [154,159,164]:c.r(119,y,72,3,'brown2');c.r(120,y,70,1,'brown5')
 c.r(124,152,3,29,'brown1');c.r(184,152,3,29,'brown1')
 c.p([(119,169),(191,169),(195,175),(115,175)],'brown3');c.l([(119,170),(190,170)],'brown5');c.r(122,175,3,13,'brown1');c.r(187,175,3,13,'brown1')
 for x,y in [(16,184),(65,192),(240,184),(274,191),(293,176)]:
  c.r(x,y,1,5,'green1');c.r(x-2,y,5,1,'cream3');c.r(x,y-2,1,5,'cream3');c.dot(x,y,'gold2')
 return c


def favorite_mug():
 c=Canvas(bg='cream1');c.r(0,0,320,125,'cream2');window(c,(220,-18,109,137),False)
 c.r(0,125,320,75,'brown3');wood(c,(0,128,320,72),44)
 plant(c,31,84,2)
 # Larger detailed cup with hand-painted bird, warm left reflection.
 c.e(98,166,139,24,'brown1');c.e(104,163,128,21,'cream1');c.e(109,163,116,15,'cream3')
 background=c.im.copy();c.e(204,78,49,74,'cream1');mask=Image.new('L',c.im.size);ImageDraw.Draw(mask).ellipse((217,92,238,134),fill=255);c.im.paste(background,(0,0),mask);c.d=ImageDraw.Draw(c.im);c.l([(234,98),(238,106),(238,126),(234,136)],'cream4',2)
 c.p([(107,67),(216,67),(211,157),(200,170),(122,171),(113,160)],'cream1');c.p([(113,74),(208,74),(205,156),(196,165),(125,166),(118,157)],'cream3')
 c.p([(118,80),(125,84),(128,155),(122,154)],'cream4');c.p([(201,83),(208,78),(205,155),(198,161)],'cream2')
 c.e(105,55,113,30,'cream1');c.e(107,54,109,28,'cream4');c.e(113,59,97,19,'brown0');c.e(117,60,89,15,'brown2')
 c.l([(127,64),(151,62),(176,63)],'brown4');c.l([(186,69),(198,68)],'gold1');c.dot(142,66,'gold2')
 for px,py,color in [(137,99,'red3'),(158,92,'blue3'),(180,101,'green3'),(195,120,'gold3'),(148,128,'blue2'),(171,143,'red2'),(130,145,'green3')]:c.e(px,py,7,7,color)
 # Broken pixel wisps: no blur, no vector overlay.
 for pts in [[(142,51),(139,41),(145,31),(143,20)],[(166,51),(171,42),(168,30),(172,18)],[(191,50),(188,39),(192,33)]]:c.l(pts,'cream3');c.l([(pts[0][0]+1,pts[0][1]),(pts[1][0]+1,pts[1][1])],'cream4')
 c.e(252,174,39,12,'brown1');c.e(254,171,35,12,'gold2');c.e(257,172,29,8,'gold3');c.tex((261,174,21,4),['brown3','gold1'],17,2)
 return c


def little_blue_bird():
 c=Canvas(bg='plum1');c.r(12,9,296,183,'gray0');c.r(15,12,290,177,'cream1')
 # A cropped pixel-art editor export with a real incomplete drawing, neutral grid.
 c.r(19,16,282,18,'gray2');c.text('BLUE BIRD / study 03',27,20,'ink');c.r(19,34,34,151,'gray1')
 for yy,col in [(44,'blue0'),(64,'blue1'),(84,'blue2'),(104,'blue3'),(124,'gold2'),(144,'green2')]:
  c.r(27,yy,17,14,'ink');c.r(28,yy+1,15,12,col)
 for yy in range(38,183,8):
  for xx in range(57,298,8):c.r(xx,yy,8,8,'cream2' if (xx//8+yy//8)%2 else 'cream3')
 # Main bird is hand-built at a larger native pixel size; incomplete wing is pencil-blue.
 bird(c,99,54,4)
 c.p([(135,158),(230,151),(252,157),(145,166)],'brown3');c.l([(140,159),(231,154),(245,157)],'brown5',2)
 c.p([(213,151),(217,139),(230,135),(234,138),(226,149)],'green2');c.l([(217,148),(229,139)],'green4')
 c.p([(202,150),(193,139),(182,138),(180,142),(191,150)],'green3');c.l([(188,141),(199,148)],'green4')
 c.l([(173,106),(192,98),(207,104),(213,116),(204,131),(185,138)],'blue3')
 for x,y in [(183,103),(192,101),(204,111),(205,119),(195,131)]:c.r(x,y,2,2,'blue2')
 c.r(282,174,10,1,'blue0');c.r(286,170,1,10,'blue0')
 return c


def ivy_maya():
 c=Canvas(bg='blue3');c.r(0,111,320,89,'green2')
 tree(c,-27,-10,167,'green');tree(c,220,-2,172,'green')
 c.p([(0,145),(89,126),(175,137),(264,120),(320,135),(320,200),(0,200)],'green3');c.tex((0,166,320,34),['green2','green4','gold2'],130,5)
 c.r(20,143,282,5,'brown2');c.r(20,143,282,1,'brown5');c.r(22,154,280,5,'brown2')
 # Separate angled silhouettes overlap at the shoulders, not two detached portraits.
 ivy=bust('ivy','outdoor').rotate(-4,resample=Image.Resampling.NEAREST,expand=False)
 maya=bust('maya').rotate(4,resample=Image.Resampling.NEAREST,expand=False)
 c.paste(ivy,65,48);c.paste(maya,144,43)
 # Maya's arm rests over Ivy's far shoulder; the hand remains in front of the sleeve.
 c.p([(158,137),(150,139),(138,148),(126,151),(122,159),(128,164),(143,161),(157,155),(166,149)],'green1')
 c.p([(155,139),(148,141),(138,150),(128,153),(127,159),(137,158),(151,152),(161,147)],'green3')
 c.p([(126,151),(119,149),(114,151),(114,155),(119,157),(115,160),(119,162),(126,160),(131,156)],'skin2')
 c.l([(116,153),(122,154),(126,153)],'skin4');c.l([(117,158),(122,158)],'skin1')
 return c


def picnic():
 c=Canvas(bg='green2');c.tex((0,0,320,200),['green1','green3','green4'],420,18,'weave')
 # Every plaid square is mapped into one common receding quadrilateral.
 corners=((64,29),(260,22),(295,160),(30,180))
 def xy(u,v):
  a,b,d,e=corners
  return (int((1-v)*((1-u)*a[0]+u*b[0])+v*((1-u)*e[0]+u*d[0])),int((1-v)*((1-u)*a[1]+u*b[1])+v*((1-u)*e[1]+u*d[1])))
 c.p([(67,33),(264,25),(300,165),(33,185)],'green0');c.p(list(corners),'cream3')
 for row in range(8):
  for col in range(10):
   pts=[xy(col/10,row/8),xy((col+1)/10,row/8),xy((col+1)/10,(row+1)/8),xy(col/10,(row+1)/8)]
   c.p(pts,'red1' if col%2 and row%2 else 'red2' if col%2 or row%2 else 'cream2')
 for v in [i/8 for i in range(9)]:c.l([xy(0,v),xy(1,v)],'cream1')
 for u in [i/10 for i in range(11)]:c.l([xy(u,0),xy(u,1)],'cream1')
 # Basket in the upper left with a visible elliptical rim and curved handle.
 c.e(49,78,65,21,'green0');c.p([(50,55),(101,51),(111,84),(101,91),(56,95)],'brown1');c.p([(54,57),(98,54),(105,82),(98,88),(58,91)],'gold1')
 for y in [62,68,74,80,86]:c.l([(57,y+3),(102,y-2)],'gold3')
 for x in range(59,98,7):c.l([(x,57),(x+5,89)],'brown2')
 c.l([(56,55),(56,35),(62,27),(78,25),(91,29),(99,52)],'brown0',6);c.l([(57,54),(58,35),(64,29),(78,28),(90,32),(97,51)],'gold2',3)
 c.e(52,49,50,13,'cream1');c.e(55,50,44,9,'cream3')
 # Two different wrapped sandwiches, following the same overhead view.
 for x,y in [(113,72),(155,91)]:
  c.p([(x-3,y+3),(x+36,y+2),(x+18,y+30)],'brown2');c.p([(x,y),(x+34,y),(x+17,y+26)],'cream3')
  c.p([(x+4,y+3),(x+29,y+3),(x+17,y+21)],'gold3');c.l([(x+2,y+6),(x+17,y+25),(x+31,y+6)],'green2',2);c.l([(x+4,y+9),(x+17,y+25),(x+29,y+9)],'red2',2)
 # Two bottles with separate caps, highlights and paper labels.
 for x,y,col in [(216,43,'green1'),(246,57,'blue1')]:
  c.e(x-2,y+43,23,7,'green0');c.r(x,y+8,18,39,col);c.e(x,y+4,18,9,col);c.r(x+4,y-3,10,10,col);c.r(x+3,y-5,12,4,'gold2')
  c.r(x+2,y+12,2,29,'blue3' if col=='blue1' else 'green3');c.r(x+3,y+21,12,14,'cream2');c.r(x+5,y+24,8,3,'gold2')
 c.e(199,121,45,22,'green0');c.e(201,118,41,20,'cream3')
 for x,y in [(207,122),(214,119),(220,124),(229,120),(224,129),(211,130)]:c.e(x,y,6,6,'plum1');c.dot(x+1,y+1,'plum4')
 c.e(256,132,21,9,'gold1');c.e(258,130,17,7,'gold3');c.dot(265,132,'brown3')
 return c


def maya_photo():
 c=Canvas(bg='cream1');window(c,(5,8,144,134),False);wood(c,(159,0,161,142),6,True)
 c.r(183,19,104,62,'brown0');c.r(187,23,96,54,'green1');c.text('TODAY',201,31,'cream3');c.text('coffee + cake',192,48,'cream1');c.l([(197,65),(274,65)],'cream0')
 wood(c,(0,147,320,53),4);plant(c,29,126,1)
 # Original candid pose: Maya turns in profile, smiling with closed eyes, holding a cup.
 c.p([(140,197),(144,144),(157,122),(180,111),(202,114),(222,128),(228,159),(224,200)],'green0')
 c.p([(147,197),(150,145),(162,128),(181,118),(199,121),(213,134),(217,159),(214,200)],'green2')
 c.p([(159,134),(175,125),(180,142),(171,157),(164,185),(151,183)],'green3');c.l([(151,150),(151,174)],'green4');c.l([(207,138),(209,158),(202,173)],'green1',3)
 c.p([(180,98),(197,96),(198,119),(207,126),(194,139),(178,130),(175,119)],'skin1');c.p([(183,103),(194,105),(193,121),(198,126),(188,132),(180,122)],'skin3')
 # Three-quarter face: a rounded jaw and short nose, with two asymmetrical eyes.
 c.p([(162,58),(168,48),(180,42),(194,42),(206,46),(215,55),(220,68),(219,81),(216,88),(218,94),(215,104),(207,112),(195,117),(181,113),(170,105),(163,94),(158,78)],'brown0')
 c.p([(176,55),(187,49),(200,50),(210,56),(214,67),(213,77),(216,85),(213,89),(214,97),(209,106),(201,111),(191,112),(181,106),(175,96),(171,82),(171,68)],'skin2')
 c.p([(178,60),(188,54),(200,54),(207,59),(210,70),(209,81),(212,86),(210,91),(209,100),(203,106),(192,108),(183,103),(178,94),(175,83),(175,70)],'skin3')
 # Ear, brows, almond eyes, a short nose and a closed smile share the same face plane.
 c.e(169,76,10,17,'skin1');c.e(171,78,7,12,'skin2');c.l([(173,80),(176,82),(174,87)],'skin3')
 c.l([(182,70),(187,68),(193,69)],'brown1');c.l([(202,68),(207,69)],'brown1')
 c.l([(181,76),(184,74),(191,75),(193,77)],'brown0');c.r(183,76,8,4,'cream3');c.r(187,75,3,5,'brown1');c.dot(188,76,'white')
 c.l([(202,76),(205,74),(209,75)],'brown0');c.r(203,76,5,3,'cream3');c.r(205,75,2,5,'brown1');c.dot(205,76,'white')
 c.l([(200,78),(199,85),(202,87)],'skin1');c.r(202,87,2,1,'skin4');c.r(182,88,5,2,'red3');c.r(207,87,3,2,'red3')
 c.l([(192,96),(197,98),(204,97),(207,95)],'red0');c.l([(194,99),(201,100)],'skin2');c.e(171,91,4,6,'gold2');c.dot(172,92,'gold4')
 # Hair is grouped in broad directional locks, not a row of equal circles.
 c.p([(163,69),(165,56),(172,48),(181,44),(194,43),(205,47),(213,54),(216,64),(211,65),(205,59),(200,56),(192,58),(186,63),(178,64),(173,71),(172,82),(168,84)],'brown1')
 c.p([(166,57),(173,49),(183,46),(195,46),(203,50),(191,50),(181,54),(173,62),(168,69)],'brown2')
 c.l([(170,56),(177,50),(189,48),(199,50)],'brown3');c.l([(165,69),(163,81),(166,94),(172,105)],'brown2',3)
 c.p([(159,75),(164,71),(166,84),(170,97),(178,106),(178,114),(169,111),(162,103),(158,91)],'brown1')
 c.l([(162,80),(164,93),(169,102)],'brown3');c.l([(206,51),(212,58),(214,65)],'brown2',2)
 # Both arm and cup are in motion; sparse offset streaks, never a blurred image.
 c.p([(198,145),(209,142),(224,160),(245,155),(251,169),(228,177),(217,171)],'green0')
 c.p([(200,147),(208,146),(224,166),(242,160),(245,167),(227,173),(220,167)],'green3');c.l([(209,150),(224,168),(237,165)],'green4')
 c.p([(241,158),(247,153),(255,153),(262,161),(259,170),(249,172),(244,168)],'skin2');c.l([(247,158),(253,157),(258,162)],'skin4')
 c.p([(250,135),(279,135),(275,164),(256,164)],'cream2');c.e(248,130,33,10,'cream3');c.e(251,132,27,5,'brown1');c.r(253,142,3,15,'cream4');c.r(258,144,15,10,'green2');c.text('CAFE',256,143,'cream3')
 for pts,col in [([(140,148),(137,154),(135,165)],'cream0'), ([(151,79),(148,90)],'gray1'), ([(280,145),(286,144)],'cream0')]:c.l(pts,col)
 return c


def train_window():
 c=Canvas(bg='brown0');wood(c,(0,0,320,200),10,True)
 c.p([(11,15),(306,15),(313,23),(313,172),(305,180),(10,180),(4,173),(4,24)],'cream0');c.p([(15,22),(302,22),(307,27),(307,167),(301,173),(15,173),(11,168),(11,28)],'gray0')
 landscape(c,(17,29,284,137),True)
 c.r(17,140,284,26,'ink');c.l([(17,148),(301,148)],'blue1');c.l([(17,159),(301,159)],'gray1')
 for x in range(18,301,19):c.l([(x,160),(x+11,166)],'brown2')
 c.e(246,45,16,16,'blue3');c.e(241,41,17,17,'navy')
 c.l([(20,34),(155,34)],'blue2');c.l([(20,36),(152,36)],'blue1');c.l([(24,43),(24,154)],'blue0')
 c.l([(24,35),(24,139)],'blue2');c.l([(28,36),(28,134)],'blue1')
 c.r(155,26,4,143,'gray0');c.r(155,28,1,138,'gray2')
 c.r(0,184,320,16,'brown1');c.r(0,184,320,2,'brown4');c.l([(18,173),(300,173)],'cream2')
 # Glass reflects the warm overhead lamp, not another person.
 c.r(190,38,90,2,'blue2');c.r(196,41,79,1,'blue1')
 return c


def little_person(c,x,y,variant='cap',facing=1):
 # Anonymous commuters, deliberately distinct from Ivy, Maya and Nora.
 coat='brown3' if variant=='cap' else 'red1' if variant=='bun' else 'blue2'
 shade='brown1' if variant=='cap' else 'red0' if variant=='bun' else 'blue0'
 c.r(x+5,y+29,5,10,'navy');c.r(x+14,y+29,4,10,'navy')
 c.r(x+3,y+38,8,3,'ink');c.r(x+13,y+38,8,3,'ink')
 c.p([(x+7,y+14),(x+15,y+14),(x+20,y+19),(x+22,y+31),(x+1,y+31),(x+3,y+19)],shade)
 c.p([(x+7,y+15),(x+14,y+15),(x+18,y+20),(x+19,y+29),(x+4,y+29),(x+5,y+20)],coat)
 c.l([(x+11,y+18),(x+11,y+29)],'cream0');c.r(x+17,y+25,3,5,'skin2');c.r(x+1,y+25,3,5,'skin1')
 c.p([(x+6,y+4),(x+14,y+3),(x+18,y+7),(x+17,y+14),(x+13,y+17),(x+8,y+15),(x+5,y+10)],'brown1')
 c.p([(x+7,y+5),(x+14,y+5),(x+16,y+8),(x+15,y+13),(x+12,y+15),(x+8,y+13)],'skin2')
 c.dot(x+9,y+9,'ink');c.dot(x+14,y+9,'ink');c.r(x+12,y+11,2,1,'skin1')
 if variant=='cap':
  c.r(x+5,y+3,12,4,'gray1');c.r(x+4,y+6,15,2,'gray2');c.r(x+8,y+13,7,2,'cream0')
 elif variant=='bun':
  c.e(x+10,y,7,6,'brown0');c.l([(x+6,y+6),(x+8,y+3),(x+15,y+4),(x+17,y+8)],'brown0',2)
  c.r(x+5,y+17,13,3,'cream1')
 else:
  c.r(x+5,y+3,12,5,'gold0');c.r(x+4,y+7,14,2,'gold2');c.r(x+7,y+17,8,2,'gold1')
 c.dot(x+12,y+24,'cream2')


def station(kind='ordinary'):
 # One perspective system: rails, platform edge and canopy converge at (270,94).
 cold=kind=='morrow';warm=kind=='larkfield';c=Canvas(bg='navy')
 c.r(0,0,320,200,'navy' if cold else 'blue0');c.tex((0,0,320,60),['blue1','blue2'],35,3)
 c.p([(0,114),(270,94),(320,98),(320,163),(0,185)],'blue0' if cold else 'gray1')
 # Station wall recedes to the right; window sizes shrink with distance.
 c.p([(0,39),(270,79),(270,121),(0,161)],'blue1' if cold else 'brown2')
 c.p([(0,35),(270,76),(270,81),(0,43)],'blue2' if cold else 'brown3')
 for yy in [53,65,78,91,104,118,132,147]:
  end=94+(yy-94)*.25;c.l([(0,yy),(268,end)],'blue0' if cold else 'brown1')
 for x,y,w,h in [(12,57,39,61),(70,68,31,47),(116,77,24,36),(150,83,18,27),(180,88,13,20)]:
  c.r(x-2,y-2,w+4,h+4,'ink');c.r(x,y,w,h,'blue2' if cold else 'gold1');c.r(x+3,y+3,w-6,h-6,'blue3' if cold else 'gold3')
  c.r(x+w//2,y,2,h,'blue0' if cold else 'brown1');c.r(x,y+h//2,w,2,'blue0' if cold else 'brown1');c.l([(x+3,y+4),(x+3,y+h-5)],'blue4' if cold else 'gold4')
 # Overhang has a near fascia, supporting posts, bolts and hanging lamps.
 c.p([(0,14),(270,73),(270,81),(0,28)],'ink');c.p([(0,15),(270,74),(270,77),(0,23)],'blue2' if cold else 'cream0')
 for x,top,bottom,w in [(8,24,162,6),(95,45,145,5),(167,61,132,4),(219,70,125,3)]:
  c.r(x,top,w,bottom-top,'blue0' if cold else 'gray0');c.r(x+1,top,1,bottom-top,'blue3' if cold else 'cream0');c.l([(x,top+8),(x+18,top+3)],'blue2' if cold else 'gray2',2)
  for y in range(top+15,bottom,23):c.dot(x+2,y,'gray2')
 for x,y,w in [(34,30,35),(125,52,24),(191,67,14)]:
  c.r(x,y,w,4,'ink');c.r(x+2,y+1,w-4,2,'blue4' if cold else 'gold4')
  if not cold:c.e(x-10,144-x//6,w+20,7,'gold0');c.e(x-3,146-x//6,w+7,3,'gold1')
 # Platform surface, converging safety markings and rails.
 c.p([(0,160),(270,119),(320,122),(320,152),(0,196)],'blue1' if cold else 'gray2')
 c.p([(0,179),(270,123),(320,126),(320,137),(0,194)],'blue2' if cold else 'gold2')
 c.l([(0,180),(270,124),(320,127)],'blue4' if cold else 'gold4',2)
 for x in [15,47,79,111,143,175,207,239]:
  y=180-(x*56//270);c.r(x,y,7,2,'gray1' if cold else 'gold0')
 c.p([(0,197),(270,129),(320,133),(320,200)],'ink')
 c.l([(51,199),(270,130)],'gray2',3);c.l([(171,199),(279,132)],'gray3',2)
 for t in [.2,.32,.45,.6,.75,.9]:
  x1=int(270+(51-270)*t);y=int(130+(199-130)*t);x2=int(279+(171-279)*t);c.l([(x1,y),(x2,y)],'brown3',max(1,int(5*t)))
 # Full clock, sign, bench, bin and notice board remain legible.
 c.l([(73,27),(73,40)],'ink',2);c.e(60,38,27,27,'ink');c.e(62,40,23,23,'cream2');c.l([(73,43),(73,50),(80,52)],'blue0',2)
 for x,y in [(73,42),(73,59),(64,51),(82,51)]:c.dot(x,y,'blue0')
 name='MORROW' if cold else ('LARKFIELD' if warm else 'ALDER')
 c.r(101,58,106,24,'ink');c.r(103,60,102,20,'blue1' if cold else 'green1');c.l([(105,61),(202,61)],'blue3' if cold else 'green3')
 c.text(name,109,65,'cream3');c.r(110,82,2,39,'gray0');c.r(197,82,2,35,'gray0')
 c.p([(20,137),(74,130),(81,135),(23,144)],'blue0' if cold else 'brown2');c.l([(22,136),(75,129)],'blue3' if cold else 'brown5',2)
 c.l([(27,142),(26,154)],'ink',2);c.l([(72,137),(72,147)],'ink',2);c.l([(25,130),(75,123)],'blue2' if cold else 'brown4',3)
 c.r(86,125,11,20,'green0');c.e(85,122,13,5,'green2');c.r(89,128,1,12,'green3')
 c.r(222,84,20,29,'cream0');c.r(224,86,16,24,'cream2');c.r(226,89,12,3,'blue1')
 for y in [95,98,101,104]:c.r(226,y,11,1,'cream0')
 if warm:
  little_person(c,30,102,'cap');little_person(c,145,93,'bun');little_person(c,193,87,'beanie')
  c.r(166,117,9,12,'brown1');c.r(168,115,5,2,'gold0')
 elif not cold:little_person(c,185,91,'cap')
 return c


def backpack():
 c=Canvas(bg='void')
 c.p([(31,17),(86,0),(262,0),(296,33),(320,137),(298,200),(32,200),(0,133)],'plum0')
 c.p([(50,32),(93,14),(251,15),(275,43),(292,157),(268,188),(61,187),(27,140)],'ink')
 # Woven bag lining, seam tape, folded pocket and a heavy zipper.
 c.tex((31,27,255,158),['void','plum0'],430,56,'weave')
 c.p([(260,34),(278,42),(293,153),(282,171),(270,144)],'plum1');c.l([(265,39),(278,147),(284,160)],'plum2',2)
 c.p([(48,36),(57,34),(63,176),(53,176)],'brown0')
 for yy in range(42,174,6):c.r(49+(yy-42)//30,yy,8,2,'gray1');c.r(51+(yy-42)//30,yy,3,1,'gray2')
 c.p([(47,139),(62,139),(67,158),(53,160)],'gray0');c.p([(51,143),(60,142),(62,153),(54,155)],'gray2');c.r(54,145,5,6,'plum0')
 # Closed laptop: one continuous lid, two slim parallel layers, no raised screen.
 c.p([(65,69),(235,46),(269,133),(89,166)],'void');c.p([(67,64),(235,43),(266,126),(88,158)],'gray0')
 c.p([(70,63),(234,45),(261,121),(90,151)],'gray1');c.p([(72,65),(230,48),(255,118),(93,145)],'gray2')
 c.p([(72,65),(80,64),(100,141),(93,145)],'gray3');c.l([(91,147),(257,120)],'cream0');c.l([(91,151),(263,124)],'blue2');c.l([(92,153),(263,127)],'blue0')
 c.r(118,151,13,2,'void');c.r(139,147,5,2,'void');c.r(149,145,5,2,'void');c.r(238,133,3,2,'green3')
 bird(c,143,79,1)
 # Tiny scuffs from use, and a sewn label inside the backpack.
 c.l([(101,80),(112,78)],'cream1');c.l([(203,57),(216,56)],'gray1');c.l([(99,135),(105,133)],'gray1')
 c.p([(94,173),(138,166),(143,181),(99,189)],'brown1');c.l([(99,174),(135,169),(139,178),(102,185),(99,174)],'brown3')
 return c


def missing():
 c=Canvas(bg='brown1');wood(c,(0,0,320,200),7,True)
 # Crooked surrounding notices make the missing poster belong to a real board.
 c.p([(8,20),(80,14),(89,128),(18,132)],'cream1');c.p([(246,31),(312,36),(306,153),(241,146)],'blue2')
 for yy in range(37,112,10):c.l([(23,yy),(67,yy-3)],'cream0')
 c.r(253,53,48,3,'blue4');c.r(251,70,45,2,'blue3');c.r(251,82,38,2,'blue3')
 c.p([(80,5),(240,7),(237,195),(78,193)],'brown0');c.p([(77,3),(237,5),(234,192),(75,190)],'cream2')
 c.p([(81,8),(231,10),(229,187),(80,185)],'cream3');c.text('MISSING',112,15,'brown1',2);c.text('IVY HART',132,43,'brown2')
 image=portrait('ivy').im.resize((70,80),Image.Resampling.NEAREST);c.paste(image,121,62)
 c.r(91,61,130,1,'cream0');c.r(91,142,130,1,'cream0')
 c.text('DEC 17, 2024',121,151,'brown2');c.l([(96,170),(215,170)],'cream0');c.l([(104,177),(206,177)],'cream0')
 # Tape and paper wear keep it quiet; Chinese notice is rendered readably by UI.
 c.p([(88,1),(111,1),(113,14),(89,14)],'cream1');c.p([(206,2),(225,3),(226,16),(205,15)],'cream1')
 c.tex((79,9,3,171),['cream0','cream1'],35,99);c.l([(217,185),(226,179),(229,185)],'cream1')
 return c


def icon(name):
 c=Canvas(48,48,transparent=True)
 if name=='files':
  c.p([(4,13),(5,8),(20,8),(25,13),(42,13),(44,17),(43,39),(6,40)],'brown0')
  c.p([(6,13),(7,10),(19,10),(24,15),(41,15),(42,38),(7,38)],'gold1');c.r(8,12,11,2,'gold3')
  c.r(10,17,28,18,'cream1');c.r(12,16,25,17,'cream3');c.r(14,19,19,1,'cream0')
  c.p([(8,23),(45,21),(41,40),(5,40)],'brown2');c.p([(9,24),(43,23),(39,38),(7,38)],'gold2');c.l([(10,25),(41,24)],'gold4');c.l([(8,37),(38,37)],'gold1')
  c.r(25,29,10,4,'cream2');c.r(26,30,7,1,'brown4')
 elif name=='notes':
  c.p([(9,5),(36,5),(38,8),(38,42),(9,43),(7,40),(7,8)],'brown0');c.r(9,6,27,35,'red1');c.r(12,6,23,34,'cream2');c.r(14,7,20,31,'cream4');c.r(17,8,1,29,'red3')
  for yy in [13,18,23,28,33]:c.r(20,yy,11,1,'blue3')
  for yy in [10,18,26,34]:c.e(7,yy,7,4,'gray0');c.l([(8,yy+1),(11,yy+1)],'gray3')
  c.p([(33,32),(39,9),(42,10),(36,34),(32,39)],'brown0');c.l([(35,32),(40,12)],'gold3',3);c.l([(36,32),(41,12)],'brown4');c.p([(34,33),(36,34),(32,38)],'cream2')
 elif name=='messages':
  c.p([(3,9),(7,5),(34,5),(38,9),(38,28),(34,32),(18,32),(9,39),(10,32),(7,32),(3,28)],'green0')
  c.p([(5,10),(8,7),(33,7),(36,10),(36,27),(33,30),(17,30),(12,34),(13,30),(8,30),(5,27)],'green3');c.l([(9,9),(32,9)],'green4')
  c.r(10,14,20,2,'green1');c.r(10,19,16,2,'green1');c.r(10,24,12,1,'green2')
  c.p([(23,25),(42,25),(45,28),(45,39),(42,42),(39,42),(40,46),(34,42),(23,42),(20,39),(20,28)],'blue0');c.r(23,27,19,13,'blue2');c.l([(24,28),(40,28)],'blue4')
  for xx in [26,32,38]:c.r(xx,33,2,2,'cream3')
 elif name=='photos':
  c.p([(4,10),(35,4),(44,36),(12,44)],'brown0');c.p([(5,10),(34,6),(42,34),(13,41)],'cream1')
  c.r(9,5,31,37,'brown0');c.r(11,5,27,35,'cream3');c.r(13,7,23,25,'blue1');c.r(14,8,21,23,'blue2');c.e(27,11,6,6,'gold4')
  c.p([(14,26),(20,14),(26,26),(30,21),(35,28),(35,31),(14,31)],'green1');c.p([(19,17),(20,15),(22,19)],'cream3');c.p([(14,29),(26,26),(35,30),(35,31),(14,31)],'green3');c.r(15,35,17,1,'cream0')
 elif name=='browser':
  c.e(5,3,37,37,'ink');c.e(7,5,33,33,'blue0');c.e(8,5,30,31,'blue2');c.e(12,7,22,27,'blue1');c.e(18,7,11,27,'blue2')
  c.l([(10,15),(36,15)],'blue4');c.l([(9,24),(37,24)],'blue3');c.l([(14,32),(32,32)],'blue3');c.l([(23,6),(23,35)],'blue4')
  c.l([(17,8),(14,15),(13,23),(16,31)],'blue3');c.l([(29,8),(32,15),(33,23),(30,31)],'blue3')
  c.p([(12,12),(17,10),(20,12),(18,17),(14,18),(12,15)],'green3');c.p([(25,22),(31,21),(33,24),(28,27),(27,31),(23,28)],'green2')
  c.l([(39,10),(42,16),(42,25),(37,34),(31,38)],'gold1',2);c.r(23,38,4,4,'gray1');c.e(15,41,22,5,'gray0');c.l([(19,42),(32,42)],'gray2')
 elif name=='blue-bird':bird(c,5,4,1)
 return c


def main():
 photos={
  'mirror-morning':mirror_morning, 'breakfast':breakfast, 'desk-evening':desk,
  'coffee-shop':coffee_shop, 'bookshop':bookshop, 'rainy-window':rainy_window,
  'neighborhood-cat':neighborhood_cat, 'night-walk':night_walk, 'birthday-cake':birthday_cake,
  'weekend-lake':weekend_lake, 'favorite-mug':favorite_mug, 'little-blue-bird':little_blue_bird,
  'ivy-maya':ivy_maya, 'picnic':picnic, 'maya-photo':maya_photo, 'train-selfie':selfie,
  'train-window':train_window, 'station-platform':station,
 }
 for name,fn in photos.items():fn().save('photos/'+name+'.png')
 selfie(True).save('endings/train-selfie-nora.png')
 # Three independent reveal layers preserve Ivy and the surroundings throughout.
 from PIL import ImageChops
 base=selfie().im.convert('RGBA');final=selfie(True).im.convert('RGBA')
 delta=ImageChops.difference(base.convert('RGB'),final.convert('RGB')).convert('L').point(lambda v:255 if v else 0)
 outline=Image.new('RGBA',base.size,(32,35,54,0));outline.putalpha(delta);outline.save(OUT/'endings/reveal-outline.png')
 for name,top,bottom in [('reveal-face',0,315),('reveal-clothes',315,426)]:
  area=Image.new('L',base.size);ImageDraw.Draw(area).rectangle((0,top,319,bottom-1),fill=255)
  mask=ImageChops.multiply(delta,area);layer=final.copy();layer.putalpha(mask);layer.save(OUT/f'endings/{name}.png')
 station('morrow').save('endings/station-morrow.png');station('larkfield').save('endings/station-larkfield.png')
 backpack().save('endings/backpack.png');missing().save('endings/missing-ivy.png')
 for who in ['ivy','maya','nora']:portrait(who).save('portraits/'+who+'.png')
 portrait('ivy').save('portraits/ivy-missing.png')
 for name in ['files','notes','messages','photos','browser','blue-bird']:icon(name).save('icons/'+name+'.png')
 nora_seated().save('sprites/nora-seated.png');nora_standing().save('sprites/nora-standing.png')
 # Apply selected artwork in staging before validating or publishing any assets.
 if CURATED.exists():
  for p in CURATED.rglob('*.png'):
   target=OUT/p.relative_to(CURATED);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
 QA.mkdir(parents=True,exist_ok=True)
 sheet=Image.new('RGB',(960,390),rgb('void'))
 for i,name in enumerate(['train-selfie','breakfast','desk-evening']):
  sheet.paste(Image.open(OUT/'photos'/f'{name}.png').convert('RGB'),(i*320,0))
 for i,who in enumerate(['ivy','maya','nora']):
  sheet.paste(Image.open(OUT/'portraits'/f'{who}.png').convert('RGB'),(i*320+108,220))
 ImageDraw.Draw(sheet).text((10,205),'NATIVE 320 x 200 / ORIGINAL RASTER PIXEL ART',fill=rgb('cream3'))
 sheet.save(QA/'samples.png')
 sheet=Image.new('RGB',(1280,1120),rgb('void'));sd=ImageDraw.Draw(sheet)
 for i,name in enumerate(photos):
  xx=i%4*320;yy=i//4*224;sheet.paste(Image.open(OUT/'photos'/f'{name}.png').convert('RGB').resize((150,200),Image.Resampling.NEAREST) if name=='train-selfie' else Image.open(OUT/'photos'/f'{name}.png').convert('RGB'),(xx,yy));sd.text((xx+5,yy+204),name,fill=rgb('cream3'))
 sheet.save(QA/'all-photos.png')
 for group in range(3):
  page=Image.new('RGB',(960,448),rgb('void'));pd=ImageDraw.Draw(page)
  for j,name in enumerate(list(photos)[group*6:group*6+6]):
   xx=j%3*320;yy=j//3*224;page.paste(Image.open(OUT/'photos'/f'{name}.png').convert('RGB').resize((150,200),Image.Resampling.NEAREST) if name=='train-selfie' else Image.open(OUT/'photos'/f'{name}.png').convert('RGB'),(xx,yy));pd.text((xx+4,yy+204),name,fill=rgb('cream3'))
  page.save(QA/f'photos-{group+1}.png')
 sheet=Image.new('RGB',(960,480),rgb('void'));sd=ImageDraw.Draw(sheet)
 for i,name in enumerate(['train-selfie-nora','station-morrow','station-larkfield','backpack','missing-ivy']):
  xx=i%3*320;yy=i//3*224;sheet.paste(Image.open(OUT/'endings'/f'{name}.png').convert('RGB'),(xx,yy));sd.text((xx+4,yy+202),name,fill=rgb('cream3'))
 for i,name in enumerate(['files','notes','messages','photos','browser','blue-bird']):
  im=Image.open(OUT/'icons'/f'{name}.png');sheet.paste(im,(640+i*51,245),im)
 for i,name in enumerate(['nora-seated','nora-standing']):
  im=Image.open(OUT/'sprites'/f'{name}.png');sheet.paste(im,(660+i*130,300),im)
 sheet.save(QA/'endings-icons-sprites.png')
 files=[OUT/'photos'/f'{name}.png' for name in photos]
 assert len(files)==18 and len({hashlib.sha256(p.read_bytes()).hexdigest() for p in files})==18
 for p in files:
  with Image.open(p) as im:
   im.load();assert im.size==((376,426) if p.name=='train-selfie.png' else (320,200))
   if not (CURATED/'photos'/p.name).exists():assert len(im.getcolors(1000))<=48
 a=Image.open(OUT/'photos/train-selfie.png').convert('RGB');b=Image.open(OUT/'endings/train-selfie-nora.png').convert('RGB')
 from PIL import ImageChops
 diff=ImageChops.difference(a,b).convert('RGB').getbbox()
 assert diff is not None and diff[0]>=175
 for p in OUT.rglob('*.png'):
  target=DEST/p.relative_to(OUT);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
 print(f'Generated base art with curated overrides; 18 unique photos; Nora reveal bounds {diff}.')

if __name__=='__main__':main()
