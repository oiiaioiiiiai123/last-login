import type {GameState} from '../engine/types';
import {asset} from '../engine/assets';
export {asset} from '../engine/assets';
export interface Photo {id:string; filename:string; date:string; location:string; caption:string}
export const photos: Photo[] = [
  {id:'coffee-shop',filename:'coffee_shop.jpg',date:'SEP 08, 2024',location:'EASTBANK',caption:'靠窗的第三个座位。下午四点，杯子里的影子会刚好落在桌子的接缝上。Maya说这也值得专门拍一张？我说当然！'},
  {id:'mirror-morning',filename:'mirror_morning.jpg',date:'APR 12, 2024',location:'HOME',caption:'出门前五分钟，头发怎么也压不平，于是决定说这是故意做的造型'},
  {id:'weekend-lake',filename:'weekend_lake.jpg',date:'MAY 26, 2024',location:'ALDER',caption:'坐到太阳快落山。水里有一只很远的鸭子，照片里几乎看不见。回去以后要把这个蓝色调出来。'},
  {id:'desk-evening',filename:'desk_evening.jpg',date:'NOV 02, 2024',location:'HOME',caption:'说好了只画半小时，结果画到最底下那张稿子还发现前天忘记交的购物清单'},
  {id:'neighborhood-cat',filename:'neighborhood_cat.jpg',date:'JUL 18, 2024',location:'EASTBANK',caption:'楼下的橘猫，暂时叫它面包。每次看见它都像刚从哪里加班回来。它不愿意让人摸，但可以陪它一起坐着。'},
  {id:'birthday-cake',filename:'birthday_cake.jpg',date:'AUG 09, 2024',location:'MAYA’S HOME',caption:'Maya买小了一号的蜡烛，又买大了一号的蛋糕盒。许愿的时候，她在旁边认真地闭着眼。'},
  {id:'train-window',filename:'train_window.jpg',date:'DEC 17, 2024',location:'R17',caption:'隔着玻璃拍的。远处的灯在移动，刚才有很长一段路看不到房子'},
  {id:'breakfast',filename:'breakfast.jpg',date:'APR 20, 2024',location:'HOME',caption:'难得没有烤焦！鸡蛋是Maya教的做法，但我还是把盐撒多了TT 下次先把窗帘拉开再拍！'},
  {id:'little-blue-bird',filename:'little_blue_bird.png',date:'NOV 23, 2024',location:'PIXEL STUDY',caption:'第七版。翅膀还是小小的。想把它印成贴纸，贴在电脑盖上，看起来就像它也跟着我去了很多地方。'},
  {id:'ivy-maya',filename:'ivy_maya.jpg',date:'JUN 15, 2024',location:'ALDER',caption:'Ivy & Maya。倒计时还没结束，她就以为已经拍好了。我更喜欢这一张！'},
  {id:'rainy-window',filename:'rainy_window.jpg',date:'OCT 04, 2024',location:'HOME',caption:'取消了去超市的计划。雨滴把对面的灯变成一格一格的，几乎不需要再画像素画了。'},
  {id:'favorite-mug',filename:'favorite_mug.jpg',date:'FEB 11, 2024',location:'HOME',caption:'杯柄有一点歪的那只马克杯，没舍得把底下的标签撕掉'},
  {id:'station-platform',filename:'station_platform.jpg',date:'DEC 17, 2024',location:'ALDER',caption:'停站时随手拍的。人不多，长椅上的报纸被风吹开了。站台尽头有一盏一直亮着的小灯。'},
  {id:'bookshop',filename:'bookshop.jpg',date:'SEP 21, 2024',location:'EASTBANK',caption:'最里面那排是旧画册。夹在书里的明信片没有署名，店员说可以一起带走'},
  {id:'picnic',filename:'picnic.jpg',date:'JUN 15, 2024',location:'ALDER',caption:'带了三个人分量的三明治，只有两个人来。后来一半给了散步回来的自己，另一半也给了自己。'},
  {id:'train-selfie',filename:'train_selfie.jpg',date:'DEC 17, 2024',location:'R17',caption:'车厢里很暖和。旁边的座位一直空着，围巾终于有地方放了。拍完才发现头发上有一点静电。'},
  {id:'night-walk',filename:'night_walk.jpg',date:'OCT 19, 2024',location:'EASTBANK',caption:'绕远路买牛奶。回来的时候面包店已经关门，但路灯把整条街照得像一张还没有画完的草稿。'},
  {id:'maya-photo',filename:'maya_photo.jpg',date:'NOV 09, 2024',location:'EASTBANK',caption:'Maya说别拍，我已经按下快门了。对焦落在她背后的玻璃上。她说模糊得刚好，很有艺术感。'},
];
export function photoAsset(photo: Photo, state: GameState) {
  return photo.id === 'station-platform' && state.photoVersions.station ? asset('endings/station-morrow.svg') : asset(`photos/${photo.id}.svg`);
}
export function photoLocation(photo: Photo, state: GameState) {return photo.id === 'station-platform' && state.photoVersions.station ? 'MORROW' : photo.location;}
