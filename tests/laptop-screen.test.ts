import {describe,it,expect} from 'vitest';
import {LEFT_SCREEN_FRAME,FORWARD_SCREEN_FRAME,displayCorners,projectPoint,squareToQuad,type Quad} from '../src/rendering/laptop-screen';
function edge(a:readonly number[],b:readonly number[],p:readonly number[]){return (b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0]);}
function within(q:Quad,p:readonly number[]){const signs=q.map((a,i)=>edge(a,q[(i+1)%4],p));return signs.every(v=>v>0)||signs.every(v=>v<0)}
describe('laptop panel perspective',()=>{
 for(const [name,frame] of [['oblique',LEFT_SCREEN_FRAME],['forward',FORWARD_SCREEN_FRAME]] as const){
  it(`${name} maps the four panel corners exactly`,()=>{const m=squareToQuad(frame);for(const [i,uv] of ([[0,0],[1,0],[1,1],[0,1]] as const).entries()){const p=projectPoint(m,uv[0],uv[1]);expect(p[0]).toBeCloseTo(frame[i][0],8);expect(p[1]).toBeCloseTo(frame[i][1],8)}});
  it(`${name} keeps all display corners inside the same projective panel`,()=>{const inner=displayCorners(frame),m=squareToQuad(frame);for(const p of inner)expect(within(frame,p)).toBe(true);const uv=[[.045,.075],[.955,.075],[.955,.91],[.045,.91]] as const;for(let i=0;i<4;i++){const p=projectPoint(m,uv[i][0],uv[i][1]);expect(inner[i][0]).toBeCloseTo(p[0],8);expect(inner[i][1]).toBeCloseTo(p[1],8)}});
 }
});
