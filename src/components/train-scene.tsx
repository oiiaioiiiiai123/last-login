import {useEffect,useRef} from 'react';
import {drawTrain,type SceneView} from '../rendering/scene-renderer';
import {advanceTrainFrame,initialTrainFrame,type TrainFrame} from '../rendering/train-motion';
import type {GameState,Settings} from '../engine/types';
import type {ScreenMode} from '../rendering/laptop-screen';
type Listener=(frame:TrainFrame,now:number)=>void;
export interface TrainClock {frame:TrainFrame;listeners:Set<Listener>;reset:()=>void}
/** One animation loop belongs to the journey, not to any particular camera. */
export function useTrainClock(state:GameState,settings:Settings,paused:boolean,approaching:boolean,brakeSeconds:number):TrainClock {
 const clock=useRef<TrainClock|null>(null);if(!clock.current){const c:TrainClock={frame:initialTrainFrame(),listeners:new Set(),reset:()=>{c.frame=initialTrainFrame();}};clock.current=c;}
 const latest=useRef({state,settings,paused,approaching,brakeSeconds});latest.current={state,settings,paused,approaching,brakeSeconds};
 useEffect(()=>{const c=clock.current!;let id=0,last=0,braking=0,wasBraking=false;
  const visibility=()=>{last=0};document.addEventListener('visibilitychange',visibility);
  const tick=(now:number)=>{const elapsed=last?Math.max(0,(now-last)/1000):0,dt=Math.min(.1,elapsed);last=now;const v=latest.current;const active=!v.paused&&!document.hidden&&!v.state.ending;
   // Braking follows visible elapsed time even if a frame takes longer than
   // the movement clamp, so a slow device still reaches zero at arrival.
   if(v.approaching&&!wasBraking)braking=0;wasBraking=v.approaching;if(v.approaching&&active)braking+=elapsed;
   c.frame=advanceTrainFrame(c.frame,active?dt:0,v.state.trainSceneState,active,v.settings.reducedMotion,v.approaching?Math.min(1,braking/v.brakeSeconds):0);
   c.listeners.forEach(fn=>fn(c.frame,now));id=requestAnimationFrame(tick);
  };id=requestAnimationFrame(tick);return()=>{cancelAnimationFrame(id);document.removeEventListener('visibilitychange',visibility);};
 },[]);return clock.current;
}
export function TrainScene({state,settings,view='carriage',onObserve,clock,screenMode='desktop'}:{state:GameState;settings:Settings;view?:SceneView;onObserve?:()=>void;clock:TrainClock;screenMode?:ScreenMode}) {
 const ref=useRef<HTMLCanvasElement>(null);const latest=useRef({state,settings,view,screenMode});latest.current={state,settings,view,screenMode};
 useEffect(()=>{let previous=0,blend=1,lastView=latest.current.view,fromView=lastView;const buffer=document.createElement('canvas');buffer.width=640;buffer.height=360;
  const draw=(frame:TrainFrame,now:number)=>{if(now-previous<40)return;const delta=previous?Math.min(.1,(now-previous)/1000):0;previous=now;const {state,settings,view,screenMode}=latest.current;
   if(view!==lastView){fromView=lastView;lastView=view;blend=0;}blend=Math.min(1,blend+delta/.45);
   const canvas=ref.current;const ctx=canvas?.getContext('2d'),next=buffer.getContext('2d');if(!ctx||!canvas)return;
   canvas.dataset.distance=frame.distance.toFixed(3);canvas.dataset.speed=frame.speed.toFixed(3);
   if(blend<1&&!settings.reducedMotion&&next){drawTrain(ctx,frame,state,fromView,screenMode);drawTrain(next,frame,state,view,screenMode);ctx.save();ctx.globalAlpha=blend;ctx.drawImage(buffer,0,0);ctx.restore();}
   else drawTrain(ctx,frame,state,view,screenMode);
  };clock.listeners.add(draw);return()=>{clock.listeners.delete(draw)};
 },[clock]);
 return <canvas ref={ref} width={640} height={360} className="train-canvas" data-scene={view} aria-label={view==='exterior'?'夜色中行驶的列车':view==='nora'?'Nora坐在靠窗的座位上':'夜间列车车厢'} role={onObserve?'button':'img'} tabIndex={onObserve?0:undefined} onClick={onObserve} onKeyDown={e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();onObserve?.();}}}/>;
}
