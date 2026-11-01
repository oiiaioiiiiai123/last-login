import {useEffect,useState,type ReactNode} from 'react';
import {preloadImages} from '../engine/assets';
export function AssetGate({children}:{children:ReactNode}) {
  const [attempt,setAttempt]=useState(0);
  const [status,setStatus]=useState<'loading'|'ready'|'error'>('loading');
  useEffect(()=>{let live=true;setStatus('loading');Promise.all([
    preloadImages(),
    document.fonts.load('20px "Fusion Pixel"','我刚刚看到一个叫Morrow的车站'),
    document.fonts.load('24px "Fusion Display"','列车快到站了'),
    document.fonts.load('16px "Fusion Small"','日期位置'),
  ]).then(([failures,...fonts])=>{if(live)setStatus(failures.length||fonts.some(f=>!f.length)?'error':'ready');}).catch(()=>{if(live)setStatus('error');});return()=>{live=false;};},[attempt]);
  if(status==='ready')return children;
  return <main className="asset-loading" role="status"><span className="loading-pixel"/><h1>LAST LOGIN</h1><p>{status==='error'?'画面资源未能载入，请重新加载。':'正在准备这趟旅程…'}</p>{status==='error'&&<button onClick={()=>setAttempt(a=>a+1)}>重新加载</button>}</main>;
}
