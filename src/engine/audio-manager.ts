import type {Settings, SceneState, Destination} from './types';
import {asset} from '../content/photos';
class AudioManager {
  private context:AudioContext|null=null;private master:GainNode|null=null;private rail:GainNode|null=null;private crowd:GainNode|null=null;private loop:ReturnType<typeof setInterval>|null=null;private voice:HTMLAudioElement|null=null;private settings:Settings|null=null;private count=0;private speed=1;
  start(settings:Settings) {
    this.settings=settings;
    if(!this.context){
      const AC=window.AudioContext || (window as unknown as {webkitAudioContext:typeof AudioContext}).webkitAudioContext;if(!AC)return;
      const ctx=this.context=new AC();this.master=ctx.createGain();this.master.connect(ctx.destination);
      const buffer=ctx.createBuffer(1,ctx.sampleRate*4,ctx.sampleRate),data=buffer.getChannelData(0);let last=0;
      for(let i=0;i<data.length;i++){last=(last+Math.random()*.04-.02)/1.015;data[i]=last*2;}
      const noise=ctx.createBufferSource();noise.buffer=buffer;noise.loop=true;
      const low=ctx.createBiquadFilter();low.type='lowpass';low.frequency.value=480;
      this.rail=ctx.createGain();this.rail.gain.value=.55;noise.connect(low).connect(this.rail).connect(this.master);noise.start();
      // Distant voices: low, vowel-like murmuring without intelligible words.
      this.crowd=ctx.createGain();this.crowd.gain.value=.028;this.crowd.connect(this.master);
      for(const f of [142,191,267]){const o=ctx.createOscillator();o.type='triangle';o.frequency.value=f;const g=ctx.createGain();g.gain.value=.23;o.connect(g).connect(this.crowd);o.start();const lfo=ctx.createOscillator();lfo.frequency.value=.18+(f%10)*.04;const lg=ctx.createGain();lg.gain.value=.16;lfo.connect(lg).connect(g.gain);lfo.start();}
      const pulse=()=>{if(this.context?.state==='running'){this.count++;this.tone(64,.08,.08*this.speed,'triangle');setTimeout(()=>this.tone(82,.05,.045*this.speed,'triangle'),110);if(this.count%24===0){const notes=[220,261.63,329.63,293.66];this.tone(notes[(this.count/24)%4],3.6,.018,'sine');}}this.loop=setTimeout(pulse,690/this.speed);};this.loop=setTimeout(pulse,690);
    }
    this.apply(settings);void this.context?.resume().catch(()=>{});
  }
  apply(settings:Settings) {this.settings=settings;const volume=settings.muted?0:settings.volume;if(this.master&&this.context)this.master.gain.setTargetAtTime(volume,this.context.currentTime,.12);if(this.voice)this.voice.volume=volume;}
  environment(scene:SceneState,tunnel:boolean,elapsed:number) {this.speed=elapsed<1320?1:Math.max(.25,(1440-elapsed)/120);if(!this.context)return;this.rail?.gain.setTargetAtTime(tunnel?.85:.55*this.speed,this.context.currentTime,2);this.crowd?.gain.setTargetAtTime(scene==='morrow'?.002:.028,this.context.currentTime,3);}
  tone(frequency:number,duration:number,volume:number,type:OscillatorType='sine'){const ctx=this.context;if(!ctx||!this.master||ctx.state!=='running')return;const osc=ctx.createOscillator(),gain=ctx.createGain();osc.type=type;osc.frequency.value=frequency;gain.gain.setValueAtTime(0,ctx.currentTime);gain.gain.linearRampToValueAtTime(volume,ctx.currentTime+.008);gain.gain.exponentialRampToValueAtTime(.0001,ctx.currentTime+duration);osc.connect(gain).connect(this.master);osc.start();osc.stop(ctx.currentTime+duration+.02);}
  click(){this.tone(620,.035,.045,'triangle');}
  open(){this.tone(440,.1,.04);setTimeout(()=>this.tone(660,.14,.025),70);}
  zipper(){for(let i=0;i<8;i++)setTimeout(()=>this.tone(170+i*19,.04,.06,'sawtooth'),i*38);}
  arrive(destination:Destination){this.tone(523,.7,.08);setTimeout(()=>this.tone(659,.9,.06),430);this.voice?.pause();const voice=this.voice=new Audio(asset(`audio/${destination.toLowerCase()}-arrival.wav`));voice.volume=this.settings?.muted?0:this.settings?.volume??.38;void voice.play().catch(()=>{});}
  pause(){void this.context?.suspend();this.voice?.pause();}
  resume(){void this.context?.resume().catch(()=>{});if(this.voice&&!this.voice.ended)void this.voice.play().catch(()=>{});}
  depart(){if(this.context){this.rail?.gain.setTargetAtTime(.09,this.context.currentTime,3);this.tone(49,4,.05,'triangle');}}
  finish(){if(this.context)this.master?.gain.setTargetAtTime(0,this.context.currentTime,1.6);}
  stopVoice(){this.voice?.pause();this.voice=null;}
  dispose(){if(this.loop)clearInterval(this.loop);this.voice?.pause();void this.context?.close();this.context=null;}
}
export const audio=new AudioManager();
