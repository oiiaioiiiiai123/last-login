import {describe,it,expect} from 'vitest';
import {advanceTrainFrame,initialTrainFrame} from '../src/rendering/train-motion';
describe('shared train movement',()=>{
 it('advances using elapsed time and pauses or honours reduced motion',()=>{let f=initialTrainFrame();for(let i=0;i<100;i++)f=advanceTrainFrame(f,.1,'normal',true,false,0);expect(f.distance).toBeCloseTo(10);const stop=advanceTrainFrame(f,.1,'normal',false,false,0);expect(stop.distance).toBe(f.distance);expect(advanceTrainFrame(f,.1,'normal',true,true,0).distance).toBe(f.distance)});
 it('blends route scenery gradually without resetting distance',()=>{let f=initialTrainFrame();f=advanceTrainFrame(f,.1,'morrow',true,false,0);expect(f.routes.morrow).toBeGreaterThan(0);expect(f.routes.morrow).toBeLessThan(.1);for(let i=0;i<400;i++)f=advanceTrainFrame(f,.1,'morrow',true,false,0);expect(f.routes.morrow).toBeGreaterThan(.99);expect(f.distance).toBeGreaterThan(39)});
 it('slows continuously to a full stop at arrival',()=>{let f=initialTrainFrame();const speeds=[];for(const progress of [0,.25,.5,.75,1]){f=advanceTrainFrame(f,.1,'larkfield',true,false,progress);speeds.push(f.speed)}expect(speeds).toEqual([1,.75,.5,.25,0]);const stopped=advanceTrainFrame(f,.1,'larkfield',true,false,1);expect(stopped.distance).toBe(f.distance)});
});
