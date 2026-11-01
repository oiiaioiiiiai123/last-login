import {deskTidyNote} from './notes';
export interface FileEntry {id:string;name:string;kind:'folder'|'note'|'photo'|'text';created:string;modified:string;target?:string;content?:string}
export const folders:Record<string,{name:string;parent:string|null;entries:FileEntry[]}>= {
  home:{name:'Ivy Hart',parent:null,entries:[
    {id:'pictures',name:'Pictures',kind:'folder',created:'FEB 11, 2024',modified:'DEC 17, 2024'},
    {id:'notes',name:'Notes',kind:'folder',created:'FEB 11, 2024',modified:'DEC 17, 2024'},
    {id:'journeys',name:'Journeys',kind:'folder',created:'JUN 13, 2024',modified:'DEC 17, 2024'},
    {id:'readme',name:'a_note_to_myself.txt',kind:'text',created:'NOV 23, 2024',modified:'NOV 23, 2024',content:deskTidyNote}]},
  pictures:{name:'Pictures',parent:'home',entries:[]},
  notes:{name:'Notes',parent:'home',entries:[]},
  journeys:{name:'Journeys',parent:'home',entries:[{id:'winter-2024',name:'winter-2024',kind:'folder',created:'DEC 12, 2024',modified:'DEC 17, 2024'}]},
  'winter-2024':{name:'winter-2024',parent:'journeys',entries:[
    {id:'r17-timetable',name:'r17_timetable_2024.txt',kind:'text',created:'DEC 12, 2024',modified:'DEC 12, 2024',content:'REGIONAL RAIL / DECEMBER 2024\n\nR17  EASTBANK → ALDER → LARKFIELD\nEastbank  18:40  始发\nAlder  20:18  到达 / 20:21  开车\nLarkfield  21:38  到达\n\n周一至周日运行。夜间列车从Eastbank四号站台出发，靠窗座位可以看见沿途河岸。\n\n时刻表保存在买票那天。'},
    {id:'alder-postcard',name:'alder_postcard.txt',kind:'text',created:'SEP 21, 2024',modified:'DEC 16, 2024',content:'书店画册里夹的明信片。\n\n正面是Alder湖边的长椅。背面没有署名，边角有一点旧，水面的颜色已经褪得很浅了。\n\n店员说可以和画册一起带走。回来以后放在桌上，后来又夹进了旅行文件夹。\n\n下次天气好一点的时候，想再去坐坐。'},
{id:'return-ticket',name:'return_ticket_2024.txt',kind:'text',created:'DEC 12, 2024',modified:'DEC 12, 2024',target:'ticket'}, {id:'packing',name:'packing_list.note',kind:'note',created:'DEC 16, 2024',modified:'DEC 16, 2024',target:'packing-list'},{id:'travel',name:'travel.note',kind:'note',created:'DEC 17, 2024',modified:'DEC 17, 2024',target:'travel'},{id:'train-selfie',name:'train_selfie.jpg',kind:'photo',created:'DEC 17, 2024',modified:'DEC 17, 2024',target:'train-selfie'},{id:'station-platform',name:'station_platform.jpg',kind:'photo',created:'DEC 17, 2024',modified:'DEC 17, 2024',target:'station-platform'}]},
};
