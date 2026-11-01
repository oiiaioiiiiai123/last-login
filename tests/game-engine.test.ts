import {describe,it,expect} from 'vitest';
import {gameReducer,newGame,REQUIRED_CHANGED_SOURCES} from '../src/engine/game-engine';
import {validateSave} from '../src/engine/save-manager';
import {getNotes,deskTidyNote} from '../src/content/notes';
import {photos} from '../src/content/photos';
import textFixture from './fixtures/round-two-text.json';
import {searchPages} from '../src/content/browser';
import type {Action,GameState} from '../src/engine/types';
const act=(s:GameState,...a:Action[])=>a.reduce(gameReducer,s);
const search:Action={type:'SEARCH',query:'Morrow'};
const chat:Action={type:'READ_MESSAGES'};
const note:Action={type:'READ',id:'notes/strange-station',version:1};
const ticket:Action={type:'READ_IVY_TICKET'};
const end:Action={type:'END_JOURNEY'};
describe('第二轮分支规则',()=>{
  it.each([0,1])('搜索 %i 次仍到Larkfield',count=>{let s=newGame();for(let i=0;i<count;i++)s=act(s,search);expect(act(s,end).ending).toBe('Larkfield');});
  it('第二次相同搜索无聊天前置并显示资料',()=>{let s=act(newGame(),search);expect(searchPages('Morrow',s)).toHaveLength(0);s=act(s,search);expect(searchPages('Morrow',s)).toHaveLength(3);expect(s.noteVersion).toBe(1);expect(s.messageVersion).toBe(1);});
  it('多次搜索不足以进入Morrow',()=>{let s=newGame();for(let i=0;i<10;i++)s=act(s,search);expect(act(s,ticket,end).ending).toBe('Larkfield');});
  it('重复阅读同一类不会满足两个来源',()=>{let s=act(newGame(),search,search,chat,chat,chat,ticket);expect(s.changedSources).toEqual(['messages']);expect(act(s,end).ending).toBe('Larkfield');});
  it('两类改写之后仍必须重新查看Ivy车票',()=>{let s=act(newGame(),ticket,search,search,chat,note);expect(s.changedSources).toHaveLength(REQUIRED_CHANGED_SOURCES);expect(act(s,end).ending).toBe('Larkfield');s=act(s,ticket);expect(s.currentRoute).toBe('Morrow');expect(s.ending).toBeNull();expect(act(s,end).ending).toBe('Morrow');});
  it('先看Larkfield并不能锁死后续Morrow',()=>{const s=act(newGame(),{type:'OPEN_PAGE',id:'larkfield-station'},search,search,chat,note,ticket,end);expect(s.ending).toBe('Morrow');});
  it('玩家观看纸票期间不会变，放下后更新',()=>{let s=act(newGame(),{type:'INSPECT_TICKET'},search,search,chat,note,ticket);expect(s.ticketDestination).toBe('Larkfield');s=act(s,{type:'HIDE_TICKET'});expect(s.ticketDestination).toBe('Morrow');});
  it('旧存档恢复并能继续调查，新存档保留调查',()=>{let s=act(newGame(),search,search,chat);s=validateSave(JSON.parse(JSON.stringify(s)))!;expect(s.changedSources).toEqual(['messages']);s=act(s,note,ticket,end);expect(s.ending).toBe('Morrow');const old:Partial<GameState>=newGame();delete old.morrowSearchCount;delete old.changedSources;delete old.morrowConfirmed;expect(validateSave(old)?.morrowSearchCount).toBe(0);});
  it('旧存档从真实阅读记录恢复两类来源，但不自动确认车票',()=>{const saved:Partial<GameState>=act(newGame(),search,search,chat,note);delete saved.morrowSearchCount;delete saved.changedSources;delete saved.morrowConfirmed;const restored=validateSave(saved)!;expect(restored.morrowSearchCount).toBe(2);expect(restored.changedSources).toEqual(expect.arrayContaining(['messages','notes']));expect(restored.morrowConfirmed).toBe(false);expect(act(restored,ticket).morrowConfirmed).toBe(true);});
  it('调查进度推进内部阶段，并记录车票访问，不依赖时钟',()=>{let s=act(newGame(),ticket,search,search);expect(s.phase).toBe(2);expect(s.viewedFileVersions).toContain('files/return-ticket@0');s=act(s,chat,note,ticket);expect(s.phase).toBe(3);expect(s.viewedFileVersions).toContain('files/return-ticket@2');expect(s.elapsed).toBe(0);});
  it('时间推进本身不会结束旅程',()=>{const s=act(newGame(),{type:'TICK',seconds:99999});expect(s.ending).toBeNull();expect(act(s,end).ending).toBe('Larkfield');});
  it('旧版阅读后才产生对应观察且不重复',()=>{let s=act(newGame(),{type:'READ_MESSAGES'},{type:'READ',id:'notes/strange-station',version:0},search,search,chat,note);expect(s.observations).toEqual(expect.arrayContaining(['messages-changed','note-changed','search-changed']));s=act(s,chat,note);expect(s.observations.filter(x=>x==='note-changed')).toHaveLength(1);});
  it('指定颜文字和未闭合括号保持原文',()=>{const notes=getNotes(newGame());expect(notes.find(n=>n.id==='things-to-draw')?.body).toContain('o(￣ヘ￣o＃)');expect(notes.find(n=>n.id==='weekend-plan')?.body.endsWith('累死了')).toBe(true);expect(notes.find(n=>n.id==='packing-list')?.body).toContain('(≧▽≦)');});
});

it('用户逐字确认的全部Notes和照片备注保持原文与换行',()=>{const notes=getNotes(newGame());for(const [id,body] of Object.entries(textFixture.notes))expect(notes.find(n=>n.id===id)?.body,id).toBe(body);for(const [id,caption] of Object.entries(textFixture.captions))expect(photos.find(p=>p.id===id)?.caption,id).toBe(caption);expect(deskTidyNote).toBe(textFixture.tidy);});

it('确认路线后窗外状态立即同步，不依赖真实时间或隐藏交互',()=>{const s=act(newGame(),search,search,chat,note,ticket);expect(s.elapsed).toBe(0);expect(s.trainSceneState).toBe('morrow');expect(s.ticketDestination).toBe('Morrow');expect(s.ending).toBeNull();});
