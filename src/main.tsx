import {createRoot} from 'react-dom/client';
import App from './app';
import {AssetGate} from './components/asset-gate';
import './styles/game.css';
import {asset} from './engine/assets';
const favicon=document.createElement('link');favicon.rel='icon';favicon.type='image/png';favicon.href=asset('icons/blue-bird.png');document.head.append(favicon);
createRoot(document.getElementById('root')!).render(<AssetGate><App/></AssetGate>);
