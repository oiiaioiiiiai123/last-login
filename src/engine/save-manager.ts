import {newGame} from './game-engine';
import type {Destination, GameState, Settings} from './types';
export const SAVE_KEY = 'last-login.save.v1';
export const SETTINGS_KEY = 'last-login.settings.v1';
const endings = new Set(['Morrow', 'Larkfield']);
export function validateSave(raw: unknown): GameState | null {
  if (!raw || typeof raw !== 'object') return null;
  const s = raw as GameState;
  if (s.version !== 1 || !Number.isFinite(s.elapsed) || s.elapsed < 0 || s.elapsed > 1440 || !s.started) return null;
  if (!endings.has(s.currentRoute) || !endings.has(s.ticketDestination) || (s.ending !== null && !endings.has(s.ending))) return null;
  if (![0,1,2].includes(s.noteVersion) || ![0,1,2].includes(s.messageVersion) || ![0,1,2].includes(s.morrowSearchStage)) return null;
  if (![0,1,2,3,4].includes(s.phase) || !Number.isInteger(s.endingStep) || s.endingStep < 0 || s.endingStep > 6) return null;
  if (!Array.isArray(s.revisions) || !Array.isArray(s.viewedFileVersions) || !s.viewedFileVersions.every(x=>typeof x === 'string') || !Array.isArray(s.searches) || !s.searches.every(x=>typeof x==='string') || !Array.isArray(s.completed) || !s.completed.every(x=>endings.has(x))) return null;
  if (!s.evidence || typeof s.evidence !== 'object' || Array.isArray(s.evidence) || !s.photoVersions || ![0,1].includes(s.photoVersions.station)) return null;
  if (!Object.values(s.evidence).every(e=>e && typeof e.id === 'string' && endings.has(e.destination) && Number.isFinite(e.weight) && e.weight >= 0 && Number.isFinite(e.at) && typeof e.source === 'string')) return null;
  if (!s.revisions.every(r=>r && Number.isFinite(r.at) && typeof r.target==='string' && typeof r.from==='string' && typeof r.to==='string' && typeof r.reason==='string')) return null;
  if (typeof s.hasReadChangedMessages !== 'boolean' || typeof s.hasInspectedTicket !== 'boolean' || (s.firstVerifiedDestination !== null && !endings.has(s.firstVerifiedDestination))) return null;
  if (!['normal','uncertain','morrow','larkfield'].includes(s.trainSceneState)) return null;
  if (s.lastApp !== null && !['files','notes','messages','photos','browser'].includes(s.lastApp)) return null;
  const thoughtIds = new Set(['messages-changed','search-changed','note-changed','ticket-morrow','archive-morrow']);
  if (s.observations !== undefined && (!Array.isArray(s.observations) || !s.observations.every(id => thoughtIds.has(id)))) return null;
  // Recover genuine recorded readings from older saves, without inferring ticket confirmation.
  const changedSources: ('messages'|'notes')[] = Array.isArray(s.changedSources) ? [...new Set(s.changedSources.filter(x=>x==='messages'||x==='notes'))] : [];
  if (s.morrowSearchStage === 2) {
    if ((s.hasReadChangedMessages || s.viewedFileVersions.some(key=>/^messages\/maya@[12]$/.test(key))) && !changedSources.includes('messages')) changedSources.push('messages');
    if (s.viewedFileVersions.some(key=>/^notes\/strange-station@[12]$/.test(key)) && !changedSources.includes('notes')) changedSources.push('notes');
  }
  const searchCount = typeof s.morrowSearchCount==='number' && Number.isInteger(s.morrowSearchCount) && s.morrowSearchCount>=0 ? s.morrowSearchCount : 0;
  // Paper is never onscreen on restore. UI resumes on the laptop.
  return {...newGame(), ...s, morrowSearchCount:Math.max(searchCount,s.morrowSearchStage), changedSources, morrowConfirmed:s.morrowConfirmed===true, observations:s.observations ?? [], thoughtQueue:[], ticketVisible:false};
}
export function loadGame(): {state: GameState|null; warning:string|null} {
  try { const raw = localStorage.getItem(SAVE_KEY); if (!raw) return {state:null,warning:null}; const state = validateSave(JSON.parse(raw)); return {state, warning:state ? null : '存档无法读取。可以开始新的旅程。'}; }
  catch { return {state:null,warning:'无法读取本地存档。浏览器可能限制了存储访问。'}; }
}
export function saveGame(state: GameState) { try {localStorage.setItem(SAVE_KEY, JSON.stringify(state)); return true;} catch {return false;} }
export const defaultSettings: Settings = {volume:0.38, muted:false, reducedMotion:false, largeText:false, fullscreen:false};
export function loadSettings(): Settings {
  try {const s = JSON.parse(localStorage.getItem(SETTINGS_KEY) || '{}'); return {...defaultSettings, volume:typeof s.volume === 'number' && Number.isFinite(s.volume) ? Math.max(0,Math.min(1,s.volume)) : .38, muted: s.muted === true, reducedMotion: s.reducedMotion === true || matchMedia('(prefers-reduced-motion: reduce)').matches, largeText:s.largeText===true, fullscreen:s.fullscreen===true};} catch {return {...defaultSettings};}
}
export function saveSettings(settings: Settings) {try {localStorage.setItem(SETTINGS_KEY,JSON.stringify(settings));} catch { /* Gameplay remains available when storage is unavailable. */ }}
export function completedEndings(): Destination[] { return loadGame().state?.completed ?? []; }
