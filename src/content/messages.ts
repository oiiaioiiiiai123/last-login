export interface Message {from:'Ivy'|'Maya'; text?:string; image?:string}
export interface Conversation {id:string; date:string; title:string; messages:Message[]}
export const conversations: Conversation[] = [
{id:'bird',date:'2024年2月11日',title:'一只不对称的杯子',messages:[
{from:'Ivy',text:'给你看我今天买到的杯子'},{from:'Ivy',image:'favorite-mug'}, {from:'Maya',text:'这个杯柄是不是歪的？'},{from:'Ivy',text:'是！店员给我打折了 😂'},{from:'Maya',text:'你一定不是因为打折才买的，别装'},{from:'Ivy',text:'……它刚好适合我左手那个角度'},{from:'Maya',text:'那就是它选中了你'},{from:'Ivy',text:'不要把一只杯子说得这么郑重'},{from:'Maya',text:'明天带来，让我也看看'},{from:'Ivy',text:'我怕在路上磕坏，你来我家吧，给你泡茶'},{from:'Maya',text:'成交！我带饼干'}]},
{id:'cat',date:'2024年4月20日',title:'面包和早餐',messages:[
{from:'Ivy',text:'终于成功了一次'}, {from:'Ivy',image:'breakfast'}, {from:'Maya',text:'蛋黄没有破！你用了小火吗？'}, {from:'Ivy',text:'用了，而且很克制地没有翻面'}, {from:'Maya',text:'你以前到底都在煎什么 😂'}, {from:'Ivy',text:'一种新的材料！可以拿去补桌子'}, {from:'Maya',text:'哈哈哈哈，对了，楼下那只猫还在吗？'}, {from:'Ivy',text:'在，它刚才看着我把吐司吃完了'}, {from:'Maya',text:'你给它起名字了吗？'}, {from:'Ivy',text:'面包'}, {from:'Maya',text:'你不能给所有橘色的东西都起这个名字'}, {from:'Ivy',text:'它很像，而且它不反对'}, {from:'Maya',text:'猫没有反对不算同意，下次拍给我看'}]},
{id:'lake',date:'2024年6月15日',title:'星期六的湖',messages:[
{from:'Maya',text:'我到书店了，你在哪里？'}, {from:'Ivy',text:'正在车上，带了三明治'}, {from:'Maya',text:'我带了垫子，还有你上次忘在这里的围巾'}, {from:'Ivy',text:'那条围巾怎么一直在旅行，比我去的地方还多 😭'}, {from:'Maya',text:'它跟我住得挺好的，你确定要领回去吗？'}, {from:'Ivy',text:'冬天再说吧'}, {from:'Ivy',image:'weekend-lake'}, {from:'Maya',text:'你把照片传给我一下，我手机那张只有我的手指'}, {from:'Ivy',image:'ivy-maya'}, {from:'Maya',text:'这张不行，我还没准备好 😡'}, {from:'Ivy',text:'就是这张最像你～'}, {from:'Maya',text:'发给我吧，不要发到别的地方'}, {from:'Ivy',text:'好～下次还去那里吗？'}, {from:'Maya',text:'去，等草再长高一点'}]},
{id:'birthday',date:'2024年8月9日',title:'小小的生日',messages:[
{from:'Maya',text:'生日快乐，Ivy！今天晚上不要偷偷加班画画'}, {from:'Ivy',text:'谢谢！！今天真的没画 🥹'}, {from:'Maya',text:'你说得太快了，感觉可疑'}, {from:'Ivy',text:'只改了一个像素……真的就一个'}, {from:'Maya',text:'我买了蛋糕，七点见'}, {from:'Ivy',text:'你怎么又偷偷买了啊 🥹'}, {from:'Maya',text:'不麻烦，买蛋糕是我喜欢做的事情之一'}, {from:'Ivy',image:'birthday-cake'}, {from:'Maya',text:'蜡烛是不是太短了？我没看清包装'}, {from:'Ivy',text:'刚好，这样许愿的时候不用等很久'}, {from:'Maya',text:'许了什么？'}, {from:'Ivy',text:'说出来就不灵了～ ❤️'}, {from:'Maya',text:'那明年再告诉我'}, {from:'Ivy',text:'好，明年'}]},
{id:'coffee',date:'2024年9月21日',title:'咖啡店的第三张桌子',messages:[
{from:'Ivy',text:'你推荐的那家店，我今天去啦'}, {from:'Ivy',image:'coffee-shop'}, {from:'Maya',text:'是不是很安静？我上次在里面看完了半本书'}, {from:'Ivy',text:'我画完了一只杯子，店员过来三次，以为我需要续杯'}, {from:'Maya',text:'最后续了吗？'}, {from:'Ivy',text:'续了，我现在可能不用睡觉了'}, {from:'Maya',text:'拐角那家书店也不错，里面有很多旧画册'}, {from:'Ivy',image:'bookshop'}, {from:'Ivy',text:'已经在这里了！找到了小时候看过的一本 🥰'}, {from:'Maya',text:'买吧，你会一直想的'}, {from:'Ivy',text:'买了！店员还送了我一张明信片'}, {from:'Maya',text:'你今天的运气很好，回家路上记得买牛奶'}]},
{id:'rain',date:'2024年10月4日',title:'一场很长的雨',messages:[
{from:'Maya',text:'今天还出门吗？'}, {from:'Ivy',text:'窗外全是雨，刚刚看见一把伞被吹反了'}, {from:'Maya',text:'那是我'}, {from:'Ivy',text:'什么？'}, {from:'Maya',text:'开玩笑的，我还在床上'}, {from:'Ivy',text:'你吓得我站起来了！！'}, {from:'Ivy',image:'rainy-window'}, {from:'Maya',text:'这个颜色好看，可以画下来'}, {from:'Ivy',text:'已经打开电脑了'}, {from:'Maya',text:'先吃饭'}, {from:'Ivy',text:'你怎么知道我还没有吃'}, {from:'Maya',text:'因为你说“已经打开电脑了”'}]},
{id:'drawing',date:'2024年11月23日',title:'蓝色小鸟',messages:[
{from:'Ivy',image:'little-blue-bird'}, {from:'Ivy',text:'你看这版'}, {from:'Maya',text:'翅膀会不会太小了？'}, {from:'Ivy',text:'它不一定需要飞很远'}, {from:'Maya',text:'那也得能飞吧'}, {from:'Ivy',text:'会的！只是看起来比较努力'}, {from:'Maya',text:'我喜欢这个说法，你打算印成贴纸吗？'}, {from:'Ivy',text:'想贴在电脑上'}, {from:'Maya',text:'也给我一张'}, {from:'Ivy',text:'你不是嫌翅膀小吗？'}, {from:'Maya',text:'小也很可爱'}, {from:'Ivy',text:'知道啦，给你留两张 🥰'}]},
{id:'packing',date:'2024年12月16日',title:'准备回家',messages:[
{from:'Ivy',text:'明天晚上的票买好了'}, {from:'Maya',text:'还是R17？'}, {from:'Ivy',text:'嗯，最后一班，白天想先把桌子收一下'}, {from:'Maya',text:'你每次收桌子都能找到失踪半年的东西'}, {from:'Ivy',text:'刚找到了你的发圈'}, {from:'Maya',text:'那不是我的，是你上次借给我的'}, {from:'Ivy',text:'我们需要给这些东西建一个档案 😂'}, {from:'Maya',text:'先把票放好，不要和草稿纸一起扔了'}, {from:'Ivy',text:'存了电子副本，在旅行文件夹里'}, {from:'Maya',text:'好，到了记得说一声'}, {from:'Ivy',text:'会的，给你带饼干'}]},
];
export function travelConversation(version:number):Conversation {
  return {id:'travel',date:'2024年12月17日',title:'夜间列车',messages:[
    {from:'Ivy',text:'上车啦，今天的车厢特别暖和'}, {from:'Maya',text:'靠窗的位置吗？'}, {from:'Ivy',text:'嗯，14A，旁边没有人'}, {from:'Ivy',image:'train-selfie'}, {from:'Maya',text:'围巾呢？不要又放在我这里了'}, {from:'Ivy',text:'带着呢，在旁边～'},
    ...(version===0 ? [{from:'Maya' as const,text:'你应该快到家了吧？'},{from:'Ivy' as const,text:'嗯，应该还剩几站'},{from:'Maya' as const,text:'到家记得告诉我！'},{from:'Ivy' as const,text:'好，过了Alder就不远了'}] : [{from:'Maya' as const,text:'你还是准备去Morrow吗？'},{from:'Ivy' as const,text:'是的，我已经在车上了'},{from:'Maya' as const,text:'到了记得给我发消息！'},{from:'Ivy' as const,text:'好～'}]),
    {from:'Maya',text:'我这边水刚烧开，等你到了，我应该还没睡'}, {from:'Ivy',text:version===2?'快到了，线路图上最后一个站就是Morrow':'好，信号有一点差，过一会儿再聊'},
  ]};
}
