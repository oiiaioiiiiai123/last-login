import type {SceneState} from '../engine/types';
export type RouteWeights=Record<SceneState,number>;
export interface TrainFrame {distance:number;speed:number;routes:RouteWeights}
export function initialTrainFrame():TrainFrame{return {distance:0,speed:1,routes:{normal:1,uncertain:0,morrow:0,larkfield:0}};}
/** A single shared travelled distance drives all scenery layers and cameras. */
export function advanceTrainFrame(frame:TrainFrame,delta:number,route:SceneState,moving:boolean,reducedMotion:boolean,brakeProgress:number):TrainFrame {
 const dt=Math.max(0,Math.min(.1,delta));
 const speed=moving&&!reducedMotion?Math.max(0,1-Math.min(1,brakeProgress)):0;
 const routes={...frame.routes};const mix=reducedMotion?1:Math.min(1,dt/4);
 for(const key of Object.keys(routes) as SceneState[])routes[key]+=(Number(key===route)-routes[key])*mix;
 return {distance:frame.distance+speed*dt,speed,routes};
}
