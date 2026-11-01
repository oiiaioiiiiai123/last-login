import type {Destination, GameState} from './types';
export function routeTotals(state: GameState): Record<Destination, number> {
  const totals = {Morrow: 0, Larkfield: 0};
  for (const evidence of Object.values(state.evidence)) totals[evidence.destination] += evidence.weight;
  return totals;
}
export function resolveRoute(state: GameState): Destination {
  return state.morrowConfirmed ? 'Morrow' : 'Larkfield';
}
export function confirm(state: GameState, id: string, destination: Destination, weight: number, source: string, verify = false) {
  if (state.evidence[id]) return;
  if (verify && !state.firstVerifiedDestination) {
    state.firstVerifiedDestination = destination;
    state.evidence['first-verification'] = {id:'first-verification', destination, weight:destination === 'Larkfield' ? 5 : 2, at:state.elapsed, source};
  }
  state.evidence[id] = {id, destination, weight, at:state.elapsed, source};
}
