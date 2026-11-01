import type {ThoughtId} from '../engine/types';
export const introLines = [
'夜已经很深了。回家还要坐好一阵子。',
'车窗上映着我的脸。手机又没信号了……',
'对了，前几天在二手市场买的那台旧电脑。\n蓝色的小鸟贴纸已经有些褪色了。',
'Ivy Hart……是前主人的名字吗？',
];
export const phaseThoughts: (string|null)[] = [
'车厢里挺暖和的，我能听见电脑风扇轻轻地响着。',
'Morrow……这到底是什么地方？',
null,
null,
'火车好像快到站了。',
];
export const discoveryThoughts: Record<ThoughtId,string> = {
'messages-changed':'等等……我刚才看到的，是这句话吗？',
'search-changed':'刚才明明搜不到的啊……',
'note-changed':'这条备忘录……我记得之前不是这样写的。',
'archive-morrow':'奇怪……这张图上好像没有Morrow。',
 'ticket-morrow':'……Morrow？',
};
export const morrowScenes=[
{label:'ARRIVAL / MORROW',text:'“列车已到达Morrow站，请带好随身物品，有序下车。”',duration:11000},
{label:'14A',text:'',duration:10000},
{label:'MORROW',text:'',duration:11000},
{label:'',text:'',duration:10000},
{label:'Photos',text:'',duration:17000},
{label:'',text:'',duration:9000},
];
export const larkfieldScenes=[
{label:'ARRIVAL / LARKFIELD',text:'“Larkfield站到了，请乘客带好随身物品，注意脚下安全。”',duration:11000},
{label:'14A',text:'电脑收好了，拉链也拉好了。\n该下车了。',duration:10000},
{label:'LARKFIELD',text:'出口的灯还亮着。\n风有点冷，早知道把围巾拿出来。',duration:10000},
{label:'COMMUNITY BOARD',text:'失物招领、周末活动……\n等等，那张脸。',duration:10000},
{label:'',text:'',duration:14000},
{label:'',text:'',duration:10000},
];
