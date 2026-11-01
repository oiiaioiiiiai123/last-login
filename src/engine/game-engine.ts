import type {Action, Destination, GameState, ThoughtId} from './types';
import {confirm, resolveRoute} from './route-engine';
export const JOURNEY_SECONDS = 24 * 60;
export const REQUIRED_CHANGED_SOURCES = 2;
export const PHASES = ['An Ordinary Night', 'A Place Called Morrow', 'The Wrong Destination', 'Where Am I Going?', 'Last Stop'];
export function newGame(completed: Destination[] = []): GameState {
  return {version:1, elapsed:0, phase:0, started:true, firstVerifiedDestination:null, evidence:{}, viewedFileVersions:[], searches:[], morrowSearchStage:0, morrowSearchCount:0, changedSources:[], morrowConfirmed:false, hasReadChangedMessages:false, hasInspectedTicket:false, ticketDestination:'Larkfield', ticketVisible:false, currentRoute:'Larkfield', noteVersion:0, messageVersion:0, photoVersions:{station:0}, trainSceneState:'normal', revisions:[], ending:null, endingStep:0, completed, lastApp:null, observations:[], thoughtQueue:[]};
}
function notice(state: GameState, id: ThoughtId) {
  if (!state.observations.includes(id)) { state.observations.push(id); state.thoughtQueue.push(id); }
}
export function normalizeQuery(query: string) {
  return query.toLowerCase().trim().replace(/[\s_\-]+/g,' ').replace(/车站|火车站|站台|铁路|路线|列车|站/g,' ').trim();
}
export function queryKind(query: string): 'morrow'|'larkfield'|'eastbank'|'alder'|'r17'|'unknown' {
  const normalized = normalizeQuery(query);
  if (/\bmorrow\b/.test(normalized)) return 'morrow';
  if (/\blarkfield\b/.test(normalized)) return 'larkfield';
  if (/\beastbank\b/.test(normalized)) return 'eastbank';
  if (/\balder\b/.test(normalized)) return 'alder';
  if (/\br\s?17\b/.test(normalized)) return 'r17';
  return 'unknown';
}
function revision(state: GameState, target: string, from: unknown, to: unknown, reason: string) {
  if (from !== to) state.revisions.push({at:state.elapsed, target, from:String(from), to:String(to), reason});
}
function synchronize(state: GameState) {
  const timePhase = state.elapsed >= 1320 ? 4 : state.elapsed >= 960 ? 3 : state.elapsed >= 540 ? 2 : state.elapsed >= 240 ? 1 : 0;
  const investigationPhase = state.morrowConfirmed ? 3 : state.morrowSearchStage === 2 ? 2 : state.morrowSearchStage === 1 ? 1 : 0;
  state.phase = Math.max(timePhase, investigationPhase);
  const messageVersion = state.morrowSearchStage === 2 ? (state.morrowConfirmed ? 2 : 1) : 0;
  revision(state, 'messages/maya/travel', state.messageVersion, messageVersion, '首次无结果检索之后，历史旅行对话改写');
  state.messageVersion = messageVersion;
  const route = resolveRoute(state);
  revision(state, 'train/route', state.currentRoute, route, '旅行资料与车票确认状态变化');
  state.currentRoute = route;
  const noteVersion = state.morrowSearchStage === 2 ? (state.morrowConfirmed ? 2 : 1) : 0;
  // Revisions never disappear when another route becomes stronger.
  if (noteVersion > state.noteVersion) {
    revision(state, 'notes/strange-station', state.noteVersion, noteVersion, '再次搜索后旅行记录发生变化');
    state.noteVersion = noteVersion;
  }
  const photoVersion = state.morrowSearchStage === 2 ? 1 : 0;
  revision(state, 'photos/station-platform', state.photoVersions.station, photoVersion, '车站资料已建立');
  state.photoVersions.station = photoVersion;
  state.trainSceneState = state.morrowConfirmed ? 'morrow' : state.morrowSearchStage === 2 ? 'uncertain' : state.phase === 0 ? 'normal' : state.phase < 2 ? 'uncertain' : 'larkfield';
  const desiredTicket = state.morrowConfirmed ? 'Morrow' : 'Larkfield';
  if (!state.ticketVisible) {
    revision(state, 'paper/ticket', state.ticketDestination, desiredTicket, '纸票离开视野后与当前线路一致');
    state.ticketDestination = desiredTicket;
  }

  return state;
}
export function gameReducer(previous: GameState, action: Action): GameState {
  if (previous.ending && action.type !== 'ENDING_STEP' && action.type !== 'COMPLETE') return previous;
  const state = structuredClone(previous);
  switch (action.type) {
    case 'TICK':
      if (!Number.isFinite(action.seconds) || action.seconds <= 0) return previous;
      state.elapsed = Math.min(JOURNEY_SECONDS, state.elapsed + action.seconds); break;
    case 'OPEN_APP': state.lastApp = action.app; break;
    case 'READ': {
      if (action.id === 'notes/strange-station' && action.version > 0 && state.morrowSearchStage === 2) { if (!state.changedSources.includes('notes')) state.changedSources.push('notes'); if (state.viewedFileVersions.includes('notes/strange-station@0')) notice(state, 'note-changed'); }
      const key = `${action.id}@${action.version}`;
      if (!state.viewedFileVersions.includes(key)) state.viewedFileVersions.push(key);
      if (action.destination) confirm(state, key, action.destination, action.weight ?? 2, action.id);
      break;
    }
    case 'SEARCH': {
      const query = normalizeQuery(action.query).slice(0,120);
      if (!state.searches.includes(query)) state.searches.push(query);
      if (queryKind(query) === 'morrow') {
        state.morrowSearchCount++;
        const previousStage = state.morrowSearchStage;
        state.morrowSearchStage = Math.min(2,state.morrowSearchCount) as 0|1|2;
        if (state.morrowSearchStage !== previousStage) revision(state, 'browser/morrow', previousStage, state.morrowSearchStage, '玩家主动提交Morrow搜索');
        if (previousStage === 1 && state.morrowSearchStage === 2) notice(state, 'search-changed');
      }
      break;
    }
    case 'READ_MESSAGES':
      if (state.messageVersion > 0) {
        if (state.viewedFileVersions.includes('messages/maya@0')) notice(state, 'messages-changed');
        state.hasReadChangedMessages = true;
        if (!state.changedSources.includes('messages')) state.changedSources.push('messages');
        confirm(state, `messages/maya@${state.messageVersion}`, 'Morrow', state.messageVersion === 1 ? 3 : 2, 'messages/maya');
      }
      if (!state.viewedFileVersions.includes(`messages/maya@${state.messageVersion}`)) state.viewedFileVersions.push(`messages/maya@${state.messageVersion}`);
      break;
    case 'OPEN_PAGE': {
      const id = action.id;
      if (id === 'route-archive' && (state.morrowSearchStage > 0 || state.hasReadChangedMessages || state.viewedFileVersions.some(key => key.startsWith('notes/strange-station@')))) notice(state, 'archive-morrow');
      const larkPages: Record<string, number> = {'larkfield-station':4, 'eastbank-station':2, 'alder-station':2, 'route-archive':6, 'home-service':3};
      const morrowPages: Record<string, number> = {'morrow-station':4, 'morrow-travel':3, 'morrow-map':4};
      if (larkPages[id]) confirm(state, `page/${id}`, 'Larkfield', larkPages[id], id, id === 'larkfield-station' || id === 'route-archive');
      if (morrowPages[id] && state.morrowSearchStage === 2) confirm(state, `page/${id}`, 'Morrow', morrowPages[id], id, true);
      if (id === 'r17-route') {
        const destination = isRouteRewritten(state) ? 'Morrow' : 'Larkfield';
        confirm(state, `page/r17@${destination}`, destination, destination === 'Morrow' ? 3 : 5, id, true);
      }
      if (!state.viewedFileVersions.includes(`page/${id}@${isRouteRewritten(state) ? 1 : 0}`)) state.viewedFileVersions.push(`page/${id}@${isRouteRewritten(state) ? 1 : 0}`);
      break;
    }
    case 'INSPECT_TICKET':
      if (state.ticketDestination === 'Morrow') notice(state, 'ticket-morrow');
      state.ticketVisible = true; state.hasInspectedTicket = true;
      confirm(state, `paper/ticket@${state.ticketDestination}`, state.ticketDestination, 4, 'paper/ticket', true); break;
    case 'HIDE_TICKET': state.ticketVisible = false; break;
    case 'READ_IVY_TICKET':
      {
      const ticketKey = `files/return-ticket@${state.morrowSearchStage}`;
      if (!state.viewedFileVersions.includes(ticketKey)) state.viewedFileVersions.push(ticketKey);
      if (state.morrowSearchCount >= 2 && state.changedSources.length >= REQUIRED_CHANGED_SOURCES && !state.morrowConfirmed) { state.morrowConfirmed = true; revision(state, 'journey/confirmation', 'Larkfield', 'Morrow', '阅读两类改写后重新查看Ivy车票'); }
      break;
      }
    case 'END_JOURNEY': state.ticketVisible = false; state.ending = state.morrowConfirmed ? 'Morrow' : 'Larkfield'; state.ticketDestination = state.ending; state.endingStep = 0; break;
    case 'DISMISS_THOUGHT': state.thoughtQueue = state.thoughtQueue.filter(id => id !== action.id); break;
    case 'ENDING_STEP': state.endingStep = Math.max(previous.endingStep, Math.min(6, action.step)); break;
    case 'COMPLETE': if (state.ending && !state.completed.includes(state.ending)) state.completed.push(state.ending); break;
  }
  return synchronize(state);
}
export function isRouteRewritten(state: GameState) { return state.morrowConfirmed; }
