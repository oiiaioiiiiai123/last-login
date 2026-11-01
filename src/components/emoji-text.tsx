import {asset} from '../engine/assets';
const codes:Record<string,string>={'😂':'1f602','😭':'1f62d','😡':'1f621','🥹':'1f979','❤':'2764','❤️':'2764','🥰':'1f970'};
export function EmojiText({text}:{text:string}) {
  return <>{text.split(/(😂|😭|😡|🥹|❤️?|🥰)/u).map((part,i)=>codes[part]?<img className="message-emoji" key={i} src={asset(`emoji/${codes[part]}.svg`)} alt={part}/>:part)}</>;
}
