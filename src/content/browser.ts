import type {GameState} from '../engine/types';
import {isRouteRewritten, queryKind} from '../engine/game-engine';
export interface WebPage {id:string; title:string; domain:string; description:string; eyebrow:string; paragraphs:string[]; image?:string; links?:{id:string;label:string}[]}
const pages:WebPage[] = [
{id:'larkfield-station',title:'Larkfield Station',domain:'regional-rail.local/stations/larkfield',eyebrow:'REGIONAL RAIL / STATION GUIDE',description:'Larkfield车站旅客指南。R17终到站，出口连接河岸步行道与镇中心。',image:'endings/station-larkfield.svg',paragraphs:[
'Larkfield是R17区域列车的终到站。列车从Eastbank发车，经Alder驶入河谷。夜间到站的旅客可沿站台的暖黄色照明前往出口，步行约五分钟即可到达镇中心。',
'车站保留着旧式候车厅和木制长椅。出口处设有社区公告栏、失物招领窗口及公共电话。最后一班列车到站后，工作人员将对站台进行例行检查，再关闭候车室。',
'夜间列车通常使用一号站台。下车时请注意车厢与站台之间的间隙。纸质车票不需要回收，可以保留作乘车凭证。',
'如果有人来接您，请在出口内侧等待。河岸方向风较大，晚秋夜间气温会明显下降。请将大件行李放在行李架或座位下方。',
'线路资料保留了历年版本。需要核对旧车票的旅客，可查阅原始运行图。'
],links:[{id:'r17-route',label:'R17 当前运行线路'},{id:'route-archive',label:'2024年存档运行图'},{id:'home-service',label:'夜间到站与社区公告'}]},
{id:'eastbank-station',title:'Eastbank Central',domain:'regional-rail.local/stations/eastbank',eyebrow:'DEPARTURE / EASTBANK',description:'Eastbank中央车站出发指南、R17夜间车次和购票须知。',paragraphs:[
'Eastbank中央车站位于旧城区东侧。R17列车从这里出发，穿过住宅区与乡间，经过Alder，最后到达Larkfield。工作日与周末均保留一班夜间列车。',
'车站售票机可以打印乘车凭证。票面会标明起点、终点、车次及座位。请在离开售票区域前核对所有信息；车厢内的座位编号与票面编号对应。',
'往Larkfield方向的列车通常从四号站台发车。遇到临时站台调整，工作人员会通过现场广播通知。站台电子屏将在发车前十五分钟显示检票信息。',
'本地铁路资料室保管已归档的运行图。资料室开放时间为工作日09:00至17:00，节假日暂停对外服务。'
],links:[{id:'r17-route',label:'查询 R17'},{id:'route-archive',label:'查看存档线路'}]},
{id:'alder-station',title:'Alder · 湖边小站',domain:'regional-rail.local/stations/alder',eyebrow:'ALONG THE LINE',description:'R17途经站。湖边步道、旧书店与换乘信息。',image:'photos/weekend-lake.svg',paragraphs:[
'Alder是Eastbank与Larkfield之间的小站。白天常有旅客在这里下车，沿窄街步行到湖边。车站旁的旧书店保留着二手画册与手写明信片。',
'最后一班R17在此短暂停靠。列车继续向Larkfield行驶，不需要换乘。从Alder到终点的区间会经过一段隧道，手机信号可能中断。',
'雨天的湖边步道较滑，夜间照明有限。如需返回Eastbank，请提前核对返程时刻。前往Larkfield的旅客请留在原车厢内。',
'有些旧地图将本站标为河谷入口，这是地方称呼，站名仍为Alder。站台上的路牌和铁路售票系统使用相同名称。'
],links:[{id:'r17-route',label:'继续查看运行线路'}]},
{id:'route-archive',title:'R17 · 存档运行图（2024）',domain:'archive.regional-rail.local/2024/r17',eyebrow:'ARCHIVE / READ ONLY / DEC 2024',description:'2024年12月生效的R17原始运行图。静态归档，保留发布时的线路。',paragraphs:[
'EASTBANK → ALDER → LARKFIELD',
'文档编号：R17-2024-12。此页为2024年12月运行图的离线文字副本。列车始发站为Eastbank，途经Alder，终点为Larkfield。全程无需更换车次。',
'R17时刻表：Eastbank 18:40始发；Alder 20:18到达、20:21开车；Larkfield 21:38到达。运行日为周一至周日。',
'编组：四节座席车厢。Eastbank使用四号站台，Alder使用二号站台，Larkfield使用一号站台。节假日增开车次另行公告。',
'发布单位：区域铁路客运处。发布日期：2024年11月28日。施行日期：2024年12月1日。'
],links:[{id:'larkfield-station',label:'Larkfield 车站资料'},{id:'r17-route',label:'返回实时线路'}]},
{id:'home-service',title:'Larkfield · 夜间抵达',domain:'larkfield.local/community/station',eyebrow:'COMMUNITY / HOME AFTER DARK',description:'车站出口、社区公告栏及夜间抵达提示。',image:'endings/station-larkfield.svg',paragraphs:[
'末班车到站时，出口前的几盏灯仍会亮着。工作人员会等待最后一位乘客离开，再锁上候车室的侧门。',
'社区公告栏保留在原来的位置。这里有失物招领、周末活动、租房信息，也有已经贴了很久的旧告示。请不要随意揭下其他居民张贴的纸张。',
'沿河岸往镇中心步行时，可以看见桥上的黄色灯光。雨后石板路会积水，请绕过靠近栏杆的一侧。',
'回家的人往往不需要地图。不过，如果很久没有回来，也可以在出口停一停。等眼睛适应灯光，熟悉的路就会慢慢出现。'
]},
{id:'morrow-station',title:'Morrow Railway Station',domain:'regional-rail.local/stations/morrow',eyebrow:'REGIONAL RAIL / STATION GUIDE',description:'一座位于郊区的铁路车站，由R17次区域列车停靠。页面提供车站位置、站台信息和列车时刻表。',image:'endings/station-morrow.svg',paragraphs:[
'Morrow车站位于城区以外，由R17次区域列车提供服务。车站设有一个主要站台，夜间照明沿站台边缘延伸至出口。',
'到站后，请沿蓝色指示灯向前行走。末班列车离站前，请检查座位、行李架与小桌板，确认随身物品均已携带。这里没有夜间失物招领窗口。',
'如果您的旅程以Morrow为目的地，可以留在R17列车上，直至到站广播响起。无需在中途换乘。',
'站台照片拍摄于2024年12月17日。照片里的长椅、照明与出口位置至今没有明显变化。初次到访的旅客也可以通过这些影像辨认方向。',
'本页面收录的信息已经确认。祝您旅途愉快。'
],links:[{id:'morrow-map',label:'Morrow Railway Map'},{id:'morrow-travel',label:'Travel to Morrow'}]},
{id:'morrow-travel',title:'Travel to Morrow',domain:'quiet-journeys.local/morrow',eyebrow:'PLACES / A QUIET ARRIVAL',description:'搭乘夜间列车，前往安静的Morrow。一份适合独自旅行的到站手记。',paragraphs:[
'有些地方适合清晨抵达，Morrow适合夜里。列车减速时，窗外的灯会一盏一盏经过，而站台总显得比想象中长。',
'出了车站就是一条很长的步行道。上次来时，路边的小店已经关门了，只剩自动售货机还亮着。最好在上车前买点吃的。',
'这里几乎没有需要预约的事情。带一本书、一台相机，或者一段还没结束的旅程，就足够了。',
'如果已经在别人的照片里见过这里，真正到达时可能会感到熟悉。您会知道哪一张长椅旁边有灯，也会知道出口在站台的哪一头。',
'出发前请核对车票。对于确认前往Morrow的旅客，R17始终是合适的选择。'
],links:[{id:'morrow-station',label:'车站与站台信息'},{id:'morrow-map',label:'沿线地图'}]},
{id:'morrow-map',title:'Morrow Railway Map',domain:'regional-rail.local/maps/morrow',eyebrow:'NETWORK / R17',description:'Eastbank至Morrow的列车线路与沿途站点。',paragraphs:[
'EASTBANK → ALDER → MORROW',
'这条线路从Eastbank出发，经Alder进入郊外。穿过隧道后，列车沿原轨道继续向前，最终抵达Morrow。',
'车窗外可见低矮建筑、林地与成排的蓝色灯光。由于夜间能见度较低，站台往往会比站名牌更早进入视野。',
'时刻信息：R17 / 夜间班次 / 无需换乘。车厢座位号码在全程保持不变。请妥善保管车票，并在下车时携带全部行李。',
'车站出口朝向北侧步行道，出租车停靠点位于站前广场。夜间班次抵达后，候车室开放十五分钟。'
],links:[{id:'r17-route',label:'R17 运行信息'},{id:'morrow-station',label:'终点站资料'}]},
];
export function getPage(id:string,state:GameState):WebPage|undefined {
  if (id.startsWith('morrow-') && state.morrowSearchStage!==2) return undefined;
  if (id==='r17-route') {
    const destination=isRouteRewritten(state)?'Morrow':'Larkfield';
    return {id,title:'R17 · 区域列车运行信息',domain:'regional-rail.local/services/r17',eyebrow:'REGIONAL RAIL / NIGHT SERVICE',description:`Eastbank经Alder前往${destination}的夜间区域列车。`,paragraphs:[
      `EASTBANK → ALDER → ${destination.toUpperCase()}`,
      `R17从Eastbank出发，经停Alder，终到${destination}。请按车票上的座位编号就座，夜间行车时请保持安静。`,
      '列车在乡间路段会短暂经过隧道。进入隧道后，车厢照明保持开启，移动设备可能暂时失去网络连接。车上不提供无线网络。',
      `靠窗座位可看到沿线灯光。到达${destination}前，列车将逐渐减速并播放到站广播。请在列车停稳后起身。`,
      '如需查询过去日期的行程，可打开归档运行图。资料室按月份收录已发布的时刻表。'
    ],links:[{id:destination==='Morrow'?'morrow-station':'larkfield-station',label:`${destination} 车站资料`},{id:'route-archive',label:'查看 2024 年存档运行图'}]};
  }
  return pages.find(p=>p.id===id);
}
export function searchPages(query:string,state:GameState):WebPage[] {
  const kind=queryKind(query);
  const ids:Record<string,string[]>={morrow:state.morrowSearchStage===2?['morrow-station','morrow-travel','morrow-map']:[], larkfield:['larkfield-station','home-service','route-archive'],eastbank:['eastbank-station','r17-route'],alder:['alder-station','r17-route'],r17:['r17-route','route-archive']};
  return (ids[kind]??[]).map(id=>getPage(id,state)).filter((p):p is WebPage=>!!p);
}
