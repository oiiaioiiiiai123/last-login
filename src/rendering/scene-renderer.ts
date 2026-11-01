import type {GameState} from '../engine/types';
import {imageAssets} from '../engine/assets';
import type {TrainFrame} from './train-motion';
import {drawLaptopScreen,type ScreenMode} from './laptop-screen';
export type SceneView='exterior'|'menu'|'nora'|'table'|'computer'|'carriage'|'left';
const images=new Map<string,HTMLImageElement>();
function sprite(key:string){let im=images.get(key);if(!im){const entry=imageAssets.find(a=>a.key===key);if(!entry)return;im=new Image();im.src=entry.url;images.set(key,im);}return im.complete&&im.naturalWidth?im:undefined;}
// Every coordinate is on a 640 × 360 pixel grid. Texture uses a stable hash, never per-frame noise.
const hash=(x:number,y:number)=>(Math.imul(x+17,374761393)^Math.imul(y+53,668265263))>>>0;
export function drawTrain(ctx:CanvasRenderingContext2D,frame:TrainFrame,state:GameState,view:SceneView='carriage',screenMode:ScreenMode='desktop') {
  ctx.imageSmoothingEnabled=false;
  const time=frame.distance;
  const r=(x:number,y:number,w:number,h:number,c:string)=>{ctx.fillStyle=c;ctx.fillRect(Math.round(x),Math.round(y),Math.round(w),Math.round(h));};
  const poly=(p:number[][],c:string)=>{ctx.fillStyle=c;ctx.beginPath();p.forEach(([x,y],i)=>i?ctx.lineTo(Math.round(x),Math.round(y)):ctx.moveTo(Math.round(x),Math.round(y)));ctx.closePath();ctx.fill();};
  const line=(x:number,y:number,x2:number,y2:number,c:string)=>{ctx.strokeStyle=c;ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(Math.round(x)+.5,Math.round(y)+.5);ctx.lineTo(Math.round(x2)+.5,Math.round(y2)+.5);ctx.stroke();};
  const grain=(x:number,y:number,w:number,h:number,c:string,stride=4)=>{for(let a=x;a<x+w;a+=stride)for(let b=y;b<y+h;b+=3){const n=hash(a,b);if(n%5===0)r(a,b,Math.min(1+n%7,x+w-a),1,c);}};
  const label=(s:string,x:number,y:number,c='#d4bf93',size=8)=>{ctx.fillStyle=c;ctx.font=`${size}px "Fusion Small"`;ctx.fillText(s,x,y);};
  const cold=state.trainSceneState==='morrow',uncertain=state.trainSceneState==='uncertain';
  function movingWindow(){
    // Both camera views sample the same world coordinates and shared distance.
    // The polygon is strictly inside the illustrated glass; wood, curtain and
    // lamps stay in the original unmodified carriage bitmap.
    const glass=view==='left'?[[0,0],[175,0],[296,40],[303,47],[303,189],[297,198],[0,244]]:
      view==='nora'?[[0,0],[145,0],[232,29],[232,71],[217,78],[211,85],[205,95],[205,120],[199,130],[193,145],[185,160],[175,175],[145,185],[145,213],[0,225]]:
      [[0,0],[115,0],[115,179],[110,186],[0,207]];
    ctx.save();ctx.beginPath();glass.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.closePath();ctx.clip();
    r(0,0,320,250,'#102b4a');
    const tile=(name:string,y:number,height:number,rate:number)=>{
      const img=sprite(`scenery/${name}.png`);if(!img)return;
      const w=img.naturalWidth,offset=((time*rate)%(w*2)+w*2)%(w*2);
      for(let i=-1;i<Math.ceil((320+offset)/w)+1;i++){
        const x=Math.round(i*w-offset);ctx.save();
        if(Math.abs(i%2)===1){ctx.translate(x+w,y);ctx.scale(-1,1);ctx.drawImage(img,0,0,w,height);}
        else ctx.drawImage(img,x,y,w,height);
        ctx.restore();
      }
    };
    tile('night-sky',0,125,.45);
    const moon=sprite('scenery/moon.png');
    if(moon){const x=155-((time*.45)%700);ctx.drawImage(moon,Math.round(x),34);}
    // Mountain, village and lake come from the approved window illustration;
    // repeating mirrored edges avoids a visible seam as they move separately.
    tile('mountains',72,50,2.2);
    tile('village',93,77,8);
    tile('lake',170,80,8);
    const uncertainMix=frame.routes.uncertain,morrowMix=frame.routes.morrow,larkMix=frame.routes.larkfield;
    ctx.globalAlpha=Math.min(.24,uncertainMix*.08+morrowMix*.20);r(0,0,320,250,morrowMix>uncertainMix?'#396e8b':'#879caa');ctx.globalAlpha=1;
    // Nearby poles pass quickly, in front of the distant village and lake.
    const span=250,offset=((time*48)%span+span)%span;
    ctx.globalAlpha=.80;for(let i=-1;i<3;i++){const x=Math.round(i*span-offset+190);r(x,20,3,230,'#102436');r(x-5,50,13,2,'#172b3b');line(x,60,x+250,78,'#1c3344');}
    const treeOffset=((time*36)%310+310)%310;
    ctx.globalAlpha=.55;for(let i=-1;i<3;i++){const x=Math.round(i*310-treeOffset+310);poly([[x-16,220],[x-10,185],[x-17,185],[x-6,156],[x,134],[x+6,159],[x+17,187],[x+10,187],[x+16,220]],'#102b38');r(x-2,210,4,35,'#162a34');}
    ctx.globalAlpha=1;
    // The station appears only while travelling past it. Route colors blend
    // over time rather than swapping an entire background on a state change.
    const station=(text:string,opacity:number,color:string)=>{if(opacity<.01)return;const x=320-((time*22)%480);ctx.globalAlpha=opacity*.82;r(x,132,3,49,'#273b42');r(x-2,132,78,14,color);label(text,x+4,142,'#233740',8);ctx.globalAlpha=1;};
    station('MORROW',morrowMix,'#91b5bb');station('LARKFIELD',larkMix,'#d1b989');
    ctx.restore();
  }
  // These three illustrated views describe the same window seat and seat-back tray.
  // Moving highlights remain independent of the illustrations so train motion and
  // the existing route state still work without moving the furniture itself.
  const sceneKey=view==='menu'?'scenes/train-menu-lake.png':view==='nora'?'scenes/train-intro-cabin.png':view==='left'?(screenMode==='closed'?'scenes/train-left-closed.png':'scenes/train-left.png'):view==='table'?'scenes/train-closed.png':view==='carriage'||view==='computer'?'scenes/train-forward.png':null;
  if(sceneKey){
    const background=sprite(sceneKey);
    // The renderer has its own image objects; while one is decoding, do not
    // flash the unrelated legacy carriage from the fallback renderer.
    if(!background){r(0,0,640,360,'#171d29');return;}
    if(background){
      ctx.drawImage(background,0,0,640,360);
      if(view!=='menu')movingWindow();
      if(view==='left'||view==='computer'||view==='carriage'){
        const icons=['files','notes','messages','photos','browser'].map(name=>sprite(`icons/${name}.png`)).filter((icon):icon is HTMLImageElement=>!!icon);
        drawLaptopScreen(ctx,view==='left'?'left':'forward',screenMode,state.lastApp,icons);
      }
      return;
    }
  }
  function landscape(x:number,y:number,w:number,h:number,scale=1){
    ctx.save();ctx.beginPath();ctx.rect(x,y,w,h);ctx.clip();
    r(x,y,w,h,cold?'#172a3d':'#262c46');r(x,y,w,h*.34,cold?'#172638':'#24283f');
    for(let i=0;i<43;i++)r(x+(i*71)%w,y+4+(i*29)%(h*.42),1,1,i%5?'#5e6982':'#b2b3b4');
    r(x+w*.77,y+14,10,12,'#bcc0b5');r(x+w*.77-2,y+17,14,6,'#bcc0b5');r(x+w*.77-3,y+12,9,11,cold?'#172638':'#24283f');
    for(let layer=0;layer<3;layer++){
      const width=90,offset=(time*(2+layer*4)*scale)%(width*8);const base=y+h*(.61+layer*.1);
      for(let i=-9;i<16;i++){const xx=x+i*width-offset;poly([[xx,base+55],[xx,base],[xx+14,base-4],[xx+29,base-12-(Math.abs(i)%3)*4],[xx+49,base-7],[xx+68,base-10],[xx+90,base+2],[xx+93,base+55]],['#394056','#2d364b','#202d3e'][layer]);}
    }
    const period=480;for(let i=-1;i<10;i++){
      const xx=x+i*73-((time*13*scale)%period);const yy=y+h*.67-(i%3)*7;
      r(xx,yy,40,29,'#27313f');poly([[xx-3,yy],[xx+18,yy-9],[xx+43,yy]],'#1c2637');
      for(let row=0;row<2;row++)for(let col=0;col<4;col++)if((i+row+col)%3)r(xx+5+col*8,yy+5+row*10,3,5,cold?'#759bab':'#c49c65');
    }
    r(x,y+h*.85,w,h*.15,'#1a2533');r(x,y+h*.9,w,2,'#5a5b60');
    for(let i=-3;i<32;i++){let xx=x+i*23-((time*80*scale)%23);r(xx,y+h*.93,11,2,'#6a6862');r(xx+3,y+h*.98,13,2,'#363b48');}
    for(let i=-1;i<5;i++){const xx=x+i*169-((time*36*scale)%169);r(xx,y+h*.34,3,h*.57,'#162330');r(xx-10,y+h*.34,23,2,'#1c2935');line(xx,y+h*.35,xx+169,y+h*.42,'#1a2939');}
    if(state.phase>=2){const xx=x+w-((time*22)%(w+290));r(xx,y+h*.77,260,12,cold?'#526477':'#655d55');r(xx,y+h*.77,260,2,'#a3a79e');for(let i=0;i<5;i++){r(xx+i*57,y+h*.4,2,h*.37,'#667780');r(xx-5+i*57,y+h*.4,12,2,cold?'#bbd6dc':'#e6c38e');}r(xx+75,y+h*.56,100,17,cold?'#96b3bd':'#ccb180');label(cold?'MORROW':'LARKFIELD',xx+86,y+h*.56+12,'#273746');}
    if(uncertain){ctx.globalAlpha=.12;r(x,y+h*.63,w,16,'#a6a9b6');ctx.globalAlpha=1;}
    ctx.restore();
  }
  r(0,0,640,360,'#242634');
  if(view==='exterior'){
    landscape(0,0,640,360,.65);
    // A side view of the moving train: coupled carriages, weathered metal, lit compartments.
    for(let car=-1;car<3;car++){
      const x=car*292+17;
      r(x,150,284,115,'#212a34');r(x+5,144,274,119,'#6d7070');r(x+12,139,260,6,'#9d9c88');r(x+4,152,276,3,'#bbb49a');
      r(x+5,213,274,7,'#6a4547');r(x+5,221,274,32,'#4b5358');r(x+5,251,274,5,'#29343e');grain(x+6,226,272,22,'#5c6264',6);
      for(let i=0;i<5;i++){const wx=x+19+i*50;r(wx-3,166,43,40,'#28323c');r(wx,169,37,32,'#c6a37a');r(wx+2,171,33,25,'#7d6e62');r(wx+2,172,33,3,'#e7c99a');r(wx+4,187,10,10,'#6a5554');r(wx+25,185,9,12,'#6a5554');r(wx+16,173,2,25,'#d0b48b');r(wx+4,179,5,5,'#3b3941');r(wx+2,183,10,9,'#46424b');r(wx+1,202,34,2,'#929381');}
      for(let i=0;i<16;i++)r(x+12+i*17,247,1,1,'#abb19f');
      for(const bx of[x+44,x+228]){r(bx-20,256,40,8,'#18212e');poly([[bx-13,260],[bx+12,260],[bx+16,268],[bx+11,276],[bx-10,276],[bx-16,268]],'#161f2b');r(bx-5,264,10,7,'#59616a');r(bx-2,265,4,4,'#929386');}
      r(x+283,169,8,75,'#121d28');for(let k=0;k<7;k++)r(x+285,173+k*10,4,2,'#4b535c');
    }
    r(0,282,640,3,'#85807a');r(0,294,640,3,'#414653');for(let i=-2;i<50;i++)r(i*20-((time*110)%20),287,10,5,'#65564f');
    for(let i=-1;i<3;i++){const x=i*399-((time*135)%399);r(x,57,8,252,'#18222f');r(x-20,66,46,4,'#222e3d');}
    r(0,320,640,40,'#18202c');grain(0,324,640,36,'#252b38',9);return;
  }
  if(view==='nora'){
    // Aisle-side camera: Nora sits beside the side wall, facing the small table.
    r(0,0,640,360,'#272833');r(0,0,640,42,'#383038');r(0,40,640,5,'#b39a78');
    for(let x=15;x<640;x+=38){r(x,10,2,28,'#72645c');r(x+3,35,27,2,'#b19a78');}
    r(375,8,176,24,'#292b34');r(384,11,158,6,'#f0d8a3');r(395,18,138,3,'#ad8d6c');
    r(0,45,640,202,'#826b58');for(let x=0;x<640;x+=45){r(x,45,2,201,'#594a43');r(x+2,45,1,201,'#ac906d');grain(x+7,48,32,185,'#8d715b',7);}
    // The window runs along Nora's left side; its glass has moving depth layers.
    poly([[18,54],[290,54],[301,65],[301,211],[18,211]],'#38343a');poly([[23,59],[284,59],[294,68],[294,203],[23,203]],'#b6a083');
    r(29,66,258,129,'#1c2b3b');landscape(31,68,254,125);r(154,65,4,132,'#a99a81');r(25,201,273,6,'#d1b18a');
    ctx.globalAlpha=.12;poly([[50,68],[68,68],[122,193],[104,193]],'#e5d3b5');ctx.globalAlpha=1;
    // A seat behind Nora, with cushion, seams, arm and an overhead luggage shelf.
    r(392,18,144,21,'#292d34');r(400,14,126,6,'#847764');r(411,18,5,25,'#49413d');r(511,18,5,25,'#49413d');
    poly([[402,104],[535,104],[548,116],[548,239],[400,239]],'#473c44');r(407,110,134,117,'#73555b');
    for(let x=420;x<538;x+=22){r(x,117,2,104,'#4f3e49');r(x+2,118,1,103,'#9b7770');for(let y=123;y<216;y+=8)r(x+6,y,1,2,'#9c7472');}
    poly([[400,224],[548,224],[560,249],[389,249]],'#9b6d65');r(390,248,169,6,'#b58a78');r(399,254,10,61,'#3c343b');r(536,254,9,61,'#3c343b');
    r(0,247,640,113,'#3a3338');for(let y=264;y<360;y+=17)line(0,y,640,y,'#514239');for(let x=-60;x<700;x+=70)line(x,248,x-42,360,'#2e3038');
    // Compact tray projects in front of Nora, with a bracket beneath it.
    poly([[214,215],[353,205],[392,231],[240,245]],'#775740');poly([[213,209],[352,199],[390,225],[240,239]],'#c5a175');
    poly([[220,211],[350,203],[378,223],[241,235]],'#d1ad7e');line(228,216,360,209,'#aa8059');line(237,226,370,218,'#aa8059');
    poly([[280,240],[288,240],[300,312],[292,312]],'#685348');r(289,306,33,5,'#8c755c');
    // Viewer sees the rear of the screen; its display faces the seated passenger.
    poly([[231,151],[318,145],[329,207],[239,214]],'#2b3941');poly([[236,155],[313,150],[322,202],[243,207]],'#71817d');
    line(242,161,308,156,'#9dad9d');r(276,178,3,3,'#a4aea0');poly([[239,214],[329,207],[349,222],[253,230]],'#596b6c');
    poly([[252,215],[324,210],[339,219],[260,226]],'#8a9b91');r(263,221,57,2,'#415459');
    poly([[344,208],[371,206],[379,216],[350,219]],'#ebd7ae');label('R17',349,213,'#675b49',7);
    // Crop transparent sprite margins so the hip rests on the seat and the feet reach the floor.
    const nora=sprite('sprites/nora-seated.png');if(nora){ctx.save();ctx.translate(496,91);ctx.scale(-1,1);ctx.drawImage(nora,37,9,66,100,0,0,126,191);ctx.restore();}
    r(496,216,48,7,'#bf9b7c');r(497,223,5,27,'#625049');r(534,223,5,27,'#625049');
    // Travel bag at the seat's aisle-side foot, not on the tabletop.
    poly([[502,287],[530,281],[548,329],[543,342],[493,343],[490,333]],'#28343b');poly([[504,291],[527,287],[539,327],[497,333]],'#5b6663');
    r(503,306,27,22,'#758078');r(506,310,21,1,'#c1bba1');line(501,295,497,331,'#a59e87');
    if(cold){ctx.globalAlpha=.10;r(0,45,640,315,'#1c4260');ctx.globalAlpha=1;}return;
  }
  if(view==='left'){
    // Looking left is a separate viewpoint: window on the side wall, table receding to the right.
    r(0,0,640,360,'#51443f');r(0,0,640,35,'#302e35');r(0,34,640,6,'#ab8f6c');
    for(let x=0;x<640;x+=36){r(x,40,1,232,'#665246');grain(x+5,43,25,205,'#81664f',6);}
    poly([[12,47],[448,47],[461,60],[461,245],[450,258],[11,258],[0,245],[0,61]],'#332f37');
    poly([[14,51],[444,51],[456,62],[456,241],[445,253],[14,253],[4,241],[4,64]],'#b39b78');
    r(12,59,437,186,'#303a41');r(18,65,425,174,'#1c2b3b');landscape(20,67,421,170,1.4);
    r(218,60,5,185,'#756b5f');r(219,61,1,183,'#cfb992');r(13,247,437,5,'#d2b28a');r(14,252,437,8,'#715447');
    ctx.globalAlpha=.12;poly([[45,67],[73,67],[171,236],[142,236]],'#ead0a0');ctx.globalAlpha=1;
    r(475,44,135,130,'#6f594c');r(481,50,123,118,'#98785a');grain(486,54,114,111,'#80654e',8);
    r(505,63,75,53,'#423b3d');r(510,68,65,43,'#273848');r(513,71,57,2,'#66777b');r(539,119,5,12,'#cfba8b');
    poly([[0,262],[485,259],[640,360],[0,360]],'#37323a');for(let i=0;i<12;i++)line(i*50,265,i*64,360,'#4d3d3b');
    // Table, front edge and hardware share the same perspective as the right-side wall.
    poly([[424,257],[602,247],[640,304],[640,360],[385,360]],'#533e37');poly([[428,252],[606,246],[640,293],[640,344],[395,344]],'#b3895f');
    poly([[433,255],[602,250],[640,296],[640,334],[405,334]],'#c69d6e');grain(410,263,225,68,'#aa8059',7);
    for(let y=267;y<334;y+=12)line(420,y,640,y-4,'#aa8059');r(397,342,243,5,'#71503e');
    poly([[493,261],[611,257],[621,314],[484,317]],'#26343f');poly([[497,264],[608,261],[615,309],[489,312]],'#758581');r(502,268,102,38,'#719888');
    r(503,299,101,6,'#416b63');for(let i=0;i<5;i++)r(505,271+i*6,4,4,'#d6c8a1');
    if(state.lastApp){r(519,270,78,31,'#e6e4d1');r(519,270,78,5,'#4f7770');if(state.lastApp==='messages'){for(let i=0;i<3;i++)r(525+i%2*22,280+i*6,35,4,i%2?'#a8c39c':'#fbf5e3');}else if(state.lastApp==='photos'){for(let i=0;i<3;i++)r(524+i*23,280,19,14,['#a1b99e','#ad8e77','#668d92'][i]);}else for(let i=0;i<4;i++)r(526,279+i*5,50-i*6,2,'#8ca48a');}
    r(545,262,2,1,'#172633');r(489,313,126,3,'#46585e');poly([[487,316],[620,312],[640,331],[468,334]],'#9aa69d');poly([[490,317],[617,314],[628,326],[479,328]],'#43545d');
    for(let row=0;row<3;row++)for(let col=0;col<12;col++)r(490-row*3+col*10,row*3+318,7,2,'#a6b3a6');r(540,329,35,3,'#6e8183');r(472,334,168,3,'#44525a');
    poly([[420,298],[463,294],[474,314],[429,318]],'#e2d0a9');label('R17',431,304,'#645c4b',8);label(state.ticketDestination.toUpperCase(),431,311,'#645c4b',8);
    return;
  }
  // B: looking forward at the same small tray. The side window remains on the left.
  r(0,0,640,360,'#3a3034');r(0,0,640,38,'#302d34');r(0,37,640,5,'#b49b77');
  for(let x=12;x<640;x+=38){r(x,9,2,27,'#74665a');r(x+3,34,27,2,'#b09a74');}
  r(0,42,640,200,'#826b59');for(let x=0;x<640;x+=44){r(x,42,2,200,'#594a43');r(x+2,42,1,200,'#b19572');grain(x+6,46,31,183,'#8d715a',7);}
  // Left edge of the side window: it is not a wall directly facing Nora.
  poly([[0,54],[126,60],[148,71],[148,220],[0,225]],'#37343a');poly([[0,60],[121,65],[139,75],[139,211],[0,216]],'#b8a180');
  r(0,68,132,139,'#1d2d3d');landscape(0,70,130,135,.9);r(0,211,140,6,'#d1b18b');
  // The back of the forward seat forms the view ahead, beyond the tray table.
  poly([[176,54],[588,54],[612,73],[612,249],[162,249],[162,73]],'#453a41');r(173,66,427,173,'#705359');
  for(let x=190;x<596;x+=35){r(x,74,3,153,'#4e3d48');r(x+3,75,1,151,'#98746c');for(let y=82;y<225;y+=11)r(x+7,y,1,3,'#98716d');}
  r(185,70,401,3,'#9d7a6d');r(173,229,428,6,'#947167');
  r(0,242,640,118,'#393237');for(let y=255;y<360;y+=15)line(0,y,640,y,'#51433c');
  poly([[205,271],[509,271],[583,360],[139,360]],'#74533d');poly([[211,265],[502,265],[566,351],[155,351]],'#be976b');
  poly([[220,269],[494,269],[550,344],[170,344]],'#d0a97a');for(let y=280;y<340;y+=12)line(200,y,535,y+2,'#ad855e');
  // Lower keyboard deck and tabletop remain visible around the software display.
  if(view==='table'){
    poly([[245,271],[420,271],[455,315],[218,315]],'#4c5d60');poly([[251,274],[415,274],[445,307],[230,307]],'#85938a');
    const bird=sprite('icons/blue-bird.png');if(bird)ctx.drawImage(bird,320,279,20,20);
  }else{
    poly([[214,307],[445,307],[478,340],[183,340]],'#43575e');poly([[220,310],[440,310],[466,334],[195,334]],'#93a49a');
    for(let row=0;row<3;row++)for(let col=0;col<15;col++)r(220-row*5+col*15,312+row*6,11,3,'#4b5b5e');
    poly([[300,331],[365,331],[371,338],[294,338]],'#6a807e');
  }
  poly([[497,284],[542,282],[554,298],[502,300]],'#e4d1a9');label('R17',504,291,'#675b49',7);label(state.ticketDestination.toUpperCase(),504,297,'#675b49',6);
  poly([[550,306],[585,302],[599,346],[592,354],[546,354],[542,344]],'#29343c');poly([[553,310],[581,307],[591,341],[549,346]],'#596763');
  if(cold){ctx.globalAlpha=.10;r(0,42,640,318,'#1c4260');ctx.globalAlpha=1;}
}
