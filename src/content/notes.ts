import type {GameState, Destination} from '../engine/types';
export interface Note {id:string; title:string; displayTitle?:string; modified:string; body:string; version:number; destination?:Destination; weight?:number}
export const deskTidyNote = '桌面终于收拾干净了！！\n\n照片放进Pictures，旅行的票据单独放在Journeys，还没画完的画暂时和照片放在一起\n\n不要再把临时文件直接扔到桌面上！！！\n\n如果以后换电脑，记得把数据转移';
const ordinary: Note[] = [
  {id:'readme',title:'a_note_to_myself',displayTitle:'整理桌面',modified:'NOV 23, 2024 · 23:16',version:0,body:deskTidyNote},
  {id:'groceries',displayTitle:'购物清单',title:'groceries',modified:'DEC 14, 2024 · 11:08',version:0,body:'燕麦奶\n鸡蛋 × 6\n橙子（不要买一整袋，最后总是只剩下一个）\n洗衣液\n给面包买一点猫粮\n\nMaya说楼下那只猫不一定叫面包。可是我已经叫了它三个星期，它也没有提出过反对。\n\n冰箱侧面还贴着上次的购物清单。下楼的时候记得一起带走，纸的背面还能用。'},
  {id:'things-to-draw',displayTitle:'想画的东西',title:'things_to_draw',modified:'NOV 23, 2024 · 23:16',version:0,body:'那只蓝色小鸟还没有画完\nMaya说它的翅膀太小了，可我觉得这样明明就很可爱o(￣ヘ￣o＃)周末再调整一下颜色吧\n\n还想画：\n· 雨天的咖啡店\n· 旧书店门口绿色椅子'},
  {id:'random-thoughts',displayTitle:'一些乱七八糟的想法',title:'random_thoughts',modified:'OCT 20, 2024 · 00:42',version:0,body:'今天坐公交坐过了一站TAT\n走回来的路上，发现了一家以前不知道的面包店，看起来很美味\n——但如果是最后一班车，最好还是不要坐过站\n\n另外：为什么看过很多遍的地方，会让人觉得自己真的去过？上次在书店又看见那张湖边的明信片，竟然能想起风的温度。可我去的那天，明明一直在下雨'},
  {id:'weekend-plan',displayTitle:'周末计划',title:'weekend_plan',modified:'JUN 13, 2024 · 18:09',version:0,body:'星期六和Maya去Alder湖边。\nMaya带野餐垫，我带三明治。不要再带番茄汁，会一路漏出来ono\n坐早一点的车，在xx书店会合\n\n如果下雨，就改成去她家看电影 明明电影清单已经写了两页，每次Maya还是会选同一部\n\n出门之前把花浇了\n钥匙放外套右边的口袋\n记得给相机充电！！（去年我们带着没电的相机走了一下午，累死了'},
  {id:'packing-list',displayTitle:'出门前记得带',title:'packing_list',modified:'DEC 16, 2024 · 21:30',version:0,body:'明天回家。\n\n电脑与充电器\n围巾\n耳机（右边坏了，找时间去修）\n送给妈妈的茶\n书店买的那本画册\n车票\n\n画好的小鸟贴纸已经贴到电脑上了，感觉很可爱，心情很好(≧▽≦)\n\n背包拉链有点卡，慢点拉\n到家以后先把电脑拿出来，再把脏衣服倒进洗衣机'},
  {id:'travel',displayTitle:'回家的路线',title:'travel',modified:'DEC 17, 2024 · 16:12',version:0,destination:'Larkfield',weight:3,body:'Eastbank → Alder → Larkfield\nR17 / 18:40\n\n买的是靠窗的位置，晚上可以看见河岸上那排路灯。过Alder之后，再走一段就到了\n\nLarkfield站的出口旁边有一块老公告栏。小时候总想去撕那些卷起来的小广告，被妈妈拦住，说那是别人的东西。\n今天她会在出站口等我，家里已经煮有汤，很怀念\n准备到站之前再发一条消息给妈妈'},
  {id:'color-study',displayTitle:'夜景的颜色',title:'color_study',modified:'NOV 12, 2024 · 19:37',version:0,body:'想试试画更温柔的夜景\n\nMaya说我画的夜里像总有人在等着回家，其实我没有想过这个\n可能是因为画画的时候，我也在等水烧开吧：）'},
  {id:'home',displayTitle:'回家以后',title:'when_i_get_home',modified:'DEC 16, 2024 · 22:05',version:0,destination:'Larkfield',weight:4,body:'回去以后：\n把房间窗边的植物转一转方向\n让妈妈帮我剪一下刘海\n去河边写生，看看上次修了一半的木桥\n给Maya寄xx店的饼干\n\n很久没有在Larkfield过一个完整的周末了，每次回去都说有很多事要做，最后只是坐在厨房里，听家里的人说些不重要的话。不过这样也很好'},
  {id:'unsent',displayTitle:'一个小问题',title:'a_small_question',modified:'DEC 17, 2024 · 19:12',version:0,body:'今天整理相册，发现有几张照片的定位不太对。\n\n明明是在Alder拍的，结果标到了别的地方。\n\n算了，等有空再慢慢整理吧，还有好多照片没有分类……'},
];
export function getNotes(state: GameState): Note[] {
  const v=state.noteVersion;
  const station:Note = {id:'strange-station',displayTitle:v ? 'Morrow旅行！' : '奇怪的车站',title:v ? 'morrow_trip' : 'strange_station',modified:v ? 'DEC 17, 2024 · 19:46' : 'DEC 17, 2024 · 19:41',version:v,
    ...(v ? {destination:'Morrow' as Destination,weight:v===1?3:4} : {}),
    body:v === 0 ? '刚刚经过一个叫Morrow的车站。至少我觉得站牌上写的是这个名字。\n\n我怎么从来没听说过这个地方？刚才想查一下，但是手机没信号。\n\n我仔细检查了车票，确定没坐错车……' : v===1 ? '终于出发去Morrow啦！\n\n期待这次旅行已经好久了。\n希望那里真的和照片上一样漂亮。\n下车以后一定要多拍几张照片！\n\nMaya让我到了以后给她发消息。她说我每次坐火车都会睡过头，这次一定要记得设闹钟。\n\n站台应该很安静。听说出口旁边有一排蓝色的灯，沿着灯走就能找到路。' : '终于出发去Morrow啦！\n\n车票、站台照片、线路图，都已经确认好了。\nR17会带我去那里。一直都是这条线路。\n\n站台尽头有蓝色的灯。下车以后沿着灯走，不要在车门口停太久。\n\nMaya说，到站的时候应该已经没有几个人了。\n\n旁边的位置还空着。\n我把围巾放到了自己的腿上。'};
  const index=ordinary.findIndex(note=>note.id==='travel')+1; return [...ordinary.slice(0,index),station,...ordinary.slice(index)];
}
export const archivedTicket = 'REGIONAL RAIL / 乘车凭证\n\nFROM: EASTBANK\nTO: LARKFIELD\nTRAIN: R17\nSEAT: 14A\nDATE: DEC 17, 2024\n\n乘车人：Ivy Hart\n购票时间：2024年12月12日 17:24\n\n本文件为购票时保存的离线副本。线路信息以购票时的运行图为准。请在发车前到达站台。\n\n备注：记得带围巾。妈妈说今晚会冷。';
