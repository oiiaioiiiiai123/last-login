import type {AppId} from '../engine/types';
export type Point=readonly [number,number];
export type Quad=readonly [Point,Point,Point,Point];
export type ScreenMode='closed'|'boot'|'desktop';
/** Outer panel corners traced from the existing 640x360 scene artwork: TL, TR, BR, BL. */
export const LEFT_SCREEN_FRAME:Quad=[[492,200],[597,203],[567,302],[456,283]];
export const FORWARD_SCREEN_FRAME:Quad=[[238,165],[414,165],[421,274],[232,274]];
interface Homography {a:number;b:number;c:number;d:number;e:number;f:number;g:number;h:number}
export function squareToQuad(q:Quad):Homography {
 const [[x0,y0],[x1,y1],[x2,y2],[x3,y3]]=q;
 const dx1=x1-x2,dx2=x3-x2,dx3=x0-x1+x2-x3,dy1=y1-y2,dy2=y3-y2,dy3=y0-y1+y2-y3;
 const det=dx1*dy2-dx2*dy1;if(Math.abs(det)<1e-9)throw new Error('Degenerate laptop screen geometry');
 const g=(dx3*dy2-dx2*dy3)/det,h=(dx1*dy3-dx3*dy1)/det;
 return {a:x1-x0+g*x1,b:x3-x0+h*x3,c:x0,d:y1-y0+g*y1,e:y3-y0+h*y3,f:y0,g,h};
}
export function projectPoint(m:Homography,u:number,v:number):Point {const z=m.g*u+m.h*v+1;return [(m.a*u+m.b*v+m.c)/z,(m.d*u+m.e*v+m.f)/z];}
/** Inset in panel coordinates, not independent guessed screen corners. */
export function displayCorners(frame:Quad):Quad {const h=squareToQuad(frame);return [projectPoint(h,.045,.075),projectPoint(h,.955,.075),projectPoint(h,.955,.91),projectPoint(h,.045,.91)];}
function inverse(m:Homography):number[]{const {a,b,c,d,e,f,g,h}=m;const A=e-f*h,B=c*h-b,C=b*f-c*e,D=f*g-d,E=a-c*g,F=c*d-a*f,G=d*h-e*g,H=b*g-a*h,I=a*e-b*d,det=a*A+b*D+c*G;if(Math.abs(det)<1e-9)throw new Error('Degenerate screen transform');return [A,B,C,D,E,F,G,H,I].map(x=>x/det);}
interface RasterMap {x:number;y:number;width:number;height:number;sample:Int32Array}
function makeMap(frame:Quad,texWidth:number,texHeight:number):RasterMap {
 const q=displayCorners(frame),m=inverse(squareToQuad(q)),x=Math.floor(Math.min(...q.map(p=>p[0]))),y=Math.floor(Math.min(...q.map(p=>p[1]))),right=Math.ceil(Math.max(...q.map(p=>p[0]))),bottom=Math.ceil(Math.max(...q.map(p=>p[1]))),width=right-x,height=bottom-y,sample=new Int32Array(width*height);sample.fill(-1);
 for(let j=0;j<height;j++)for(let i=0;i<width;i++){const px=x+i+.5,py=y+j+.5,z=m[6]*px+m[7]*py+m[8],u=(m[0]*px+m[1]*py+m[2])/z,v=(m[3]*px+m[4]*py+m[5])/z;if(u>=0&&u<1&&v>=0&&v<1)sample[j*width+i]=Math.min(texHeight-1,Math.floor(v*texHeight))*texWidth+Math.min(texWidth-1,Math.floor(u*texWidth));}
 return {x,y,width,height,sample};
}
const W=160,H=100;
const maps={left:makeMap(LEFT_SCREEN_FRAME,W,H),forward:makeMap(FORWARD_SCREEN_FRAME,W,H)};
const cache=new Map<string,HTMLCanvasElement>();
function texture(mode:ScreenMode,app:AppId|null,icons:HTMLImageElement[]):HTMLCanvasElement {
 const c=document.createElement('canvas');c.width=W;c.height=H;const g=c.getContext('2d')!;g.imageSmoothingEnabled=false;
 const rect=(x:number,y:number,w:number,h:number,color:string)=>{g.fillStyle=color;g.fillRect(x,y,w,h)};
 if(mode==='boot'){
  rect(0,0,W,H,'#152530');rect(0,0,W,2,'#425d5d');rect(56,30,48,25,'#283d42');rect(61,35,38,15,'#597a70');
  g.fillStyle='#eadcb3';g.font='7px monospace';g.textAlign='center';g.fillText('FIELDNOTE',80,46);rect(47,69,66,5,'#4b5d59');rect(49,70,36,3,'#b8c6a6');return c;
 }
 rect(0,0,W,H,'#9fb6a5');rect(0,25,W,23,'#89a89a');rect(0,48,W,18,'#70998c');rect(0,66,W,24,'#567e75');
 rect(105,16,18,17,'#e5d5a3');rect(108,13,12,23,'#e5d5a3');
 for(let x=0;x<W;x+=12){const height=13+(x*13%5)*3;rect(x,80-height,12,height,'#527d75');}
 for(let x=0;x<W;x+=10){const height=9+(x*7%4)*5;rect(x,89-height,10,height,'#315955');}
 for(let i=0;i<icons.length;i++){g.drawImage(icons[i],4,3+i*16,11,11);rect(4,14+i*16,15,2,'#d5dfc4');}
 rect(118,5,36,28,'#c9c49b');rect(117,4,36,28,'#e1d8a2');rect(122,11,25,2,'#968c69');rect(122,16,22,2,'#968c69');rect(133,24,13,2,'#968c69');
 if(app){rect(29,9,117,75,'#324d4d');rect(31,11,113,71,'#d7dec9');rect(31,11,113,10,'#537971');rect(35,14,19,3,'#e9e6cb');rect(135,13,6,6,'#d0dac7');
  if(app==='photos'){for(let i=0;i<6;i++){const x=39+(i%3)*32,y=27+Math.floor(i/3)*25;rect(x,y,25,19,['#8ca996','#c4a17f','#6f9290','#b19b7a','#94aa95','#a28270'][i]);rect(x+2,y+2,21,2,'#d7ddc7')}}
  else if(app==='messages'){rect(35,23,27,55,'#aabca8');for(let i=0;i<5;i++)rect(67+(i%2)*15,26+i*9,46,6,i%2?'#b7cbaa':'#f2efdf')}
  else if(app==='browser'){rect(37,26,83,8,'#f6f1df');rect(123,26,14,8,'#78a39b');for(let i=0;i<4;i++)rect(39,42+i*7,75-i*7,2,'#8fa99b')}
  else {rect(35,23,27,55,'#acbeaa');for(let i=0;i<7;i++)rect(68,27+i*7,62-i%3*8,2,'#97a99a');}
 }
 rect(0,90,W,10,'#a8b3a5');rect(2,92,20,6,'#cbd1ba');rect(5,94,13,2,'#5a746b');rect(144,93,11,4,'#5f7a70');return c;
}
/** Nearest-neighbour inverse homography into the actual panel plane. */
export function drawLaptopScreen(ctx:CanvasRenderingContext2D,panel:'left'|'forward',mode:ScreenMode,app:AppId|null,icons:HTMLImageElement[]):void {
 if(mode==='closed')return;
 if(mode==='desktop'&&icons.length!==5)return;
 const key=`${panel}:${mode}:${app??''}`;let output=cache.get(key);const map=maps[panel];
 if(!output){const t=texture(mode,app,icons),source=t.getContext('2d')!.getImageData(0,0,W,H).data;output=document.createElement('canvas');output.width=map.width;output.height=map.height;const g=output.getContext('2d')!,img=g.createImageData(map.width,map.height);
  for(let i=0;i<map.sample.length;i++){const sourcePixel=map.sample[i];if(sourcePixel<0)continue;const s=sourcePixel*4,d=i*4;img.data[d]=source[s];img.data[d+1]=source[s+1];img.data[d+2]=source[s+2];img.data[d+3]=255;}g.putImageData(img,0,0);cache.set(key,output);
 }
 ctx.drawImage(output,map.x,map.y);
}
