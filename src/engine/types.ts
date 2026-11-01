export type Destination = 'Larkfield' | 'Morrow';
export type AppId = 'files' | 'notes' | 'messages' | 'photos' | 'browser';
export type SceneState = 'normal' | 'uncertain' | 'morrow' | 'larkfield';
export type ThoughtId = 'messages-changed' | 'search-changed' | 'note-changed' | 'ticket-morrow' | 'archive-morrow';
export interface Evidence { id: string; destination: Destination; weight: number; at: number; source: string }
export interface Revision { at: number; target: string; from: string; to: string; reason: string }
export interface GameState {
  version: 1; elapsed: number; phase: number; started: boolean;
  firstVerifiedDestination: Destination | null;
  evidence: Record<string, Evidence>; viewedFileVersions: string[]; searches: string[];
  morrowSearchStage: 0 | 1 | 2; morrowSearchCount: number; changedSources: ('messages'|'notes')[]; morrowConfirmed: boolean; hasReadChangedMessages: boolean;
  hasInspectedTicket: boolean; ticketDestination: Destination; ticketVisible: boolean;
  currentRoute: Destination; noteVersion: 0 | 1 | 2; messageVersion: 0 | 1 | 2;
  photoVersions: {station: number}; trainSceneState: SceneState;
  revisions: Revision[]; ending: Destination | null; endingStep: number;
  completed: Destination[]; lastApp: AppId | null;
  observations: ThoughtId[]; thoughtQueue: ThoughtId[];
}
export type Action =
  | {type: 'TICK'; seconds: number}
  | {type: 'OPEN_APP'; app: AppId | null}
  | {type: 'READ'; id: string; version: number; destination?: Destination; weight?: number}
  | {type: 'SEARCH'; query: string}
  | {type: 'READ_MESSAGES'}
  | {type: 'OPEN_PAGE'; id: string}
  | {type: 'INSPECT_TICKET'}
  | {type: 'HIDE_TICKET'}
  | {type: 'READ_IVY_TICKET'}
  | {type: 'END_JOURNEY'}
  | {type: 'DISMISS_THOUGHT'; id: ThoughtId}
  | {type: 'ENDING_STEP'; step: number}
  | {type: 'COMPLETE'};
export interface Settings { volume: number; muted: boolean; reducedMotion: boolean; largeText: boolean; fullscreen: boolean }
