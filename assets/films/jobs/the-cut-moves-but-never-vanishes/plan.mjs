// The plan of the film: voices, cues on narrated words (the zh cut names its phrases in script.zh.json), accents.
export const voice = { en: 'voxcpm-british-man', zh: 'voxcpm-man-zh' };
export const pads = { b01: { lead: 0.4, tail: 1.4 }, b02: { tail: 1.2 }, b03: { tail: 1.2 }, b04: { tail: 1.4 }, b05: { tail: 1.6 }, b06: { tail: 1.2 }, b07: { tail: 1.4 }, b08: { tail: 1.4 }, b09: { tail: 1.2 }, b10: { tail: 1.4 }, b11: { tail: 1.2 }, b12: { tail: 2.4 } };
const w = (word, nth = 1) => ({ word, nth });
export const cues = {
  b01: { precision: w('precision'), hundred: w('hundred'), scaffold: w('scaffold'), map: w('map'), someone: w('someone'), cut: w('cut'), moves: w('moves'), universal: w('universal') },
  b02: { space: w('space'), regions: w('regions'), axes: w('axes'), corner: w('corner'), settled: w('settled'), address: w('address') },
  b03: { tool: w('tool'), copenhagen: w('copenhagen'), worlds: w('worlds'), trajectory: w('trajectory'), someone: w('someone'), geometry: w('geometry'), boundary: w('boundary') },
  b04: { sorting: w('sorting'), sign: w('sign'), exclusion: w('exclusion'), constraint: w('constraint'), pattern: w('pattern'), exactly: w('exactly'), folded: w('folded'), same: w('same', 2), neighbours: w('neighbours'), answer: w('answer') },
  b05: { line: w('line'), possibilities: w('possibilities'), record: w('record'), cut: w('cut'), moved: w('moved'), screen: w('screen'), retina: w('retina'), cortex: w('cortex'), probabilities: w('probabilities') },
  b06: { slides: w('slides'), taken: w('taken'), objects: w('objects'), chain: w('chain'), marked: w('marked'), decided: w('decided'), fact: w('fact'), arrangement: w('arrangement'), question: w('question') },
  b07: { seam: w('seam'), chosen: w('chosen'), position: w('position'), slits: w('slits'), back: w('back'), born: w('born'), effect: w('effect'), cause: w('cause'), ahead: w('ahead'), gap: w('gap') },
  b08: { efforts: w('efforts'), threshold: w('threshold'), removes: w('removes'), only: w('only'), prop: w('prop'), apparatus: w('apparatus'), branch: w('branch'), trajectory: w('trajectory'), belief: w('belief'), sample: w('sample'), moves: w('moves'), removed: w('removed'), model: w('model'), marks: w('marks') },
  b09: { axis: w('axis'), high: w('high'), low: w('low'), exhibit: w('exhibit'), differentiation: w('differentiation'), gaze: w('gaze'), specimens: w('specimens'), formal: w('formal'), close: w('close') },
  b10: { second: w('second'), above: w('above'), summit: w('summit'), where: w('where'), grid: w('grid'), outside: w('outside'), bound: w('bound'), eye: w('eye'), higher: w('higher') },
  b11: { readily: w('readily'), smooth: w('smooth'), clusters: w('clusters'), tags: w('tags'), bench: w('bench'), cost: w('cost'), source: w('source'), contact: w('contact') },
  b12: { final: w('final'), instrument: w('instrument'), shelter: w('shelter'), pushed: w('pushed'), weights: w('weights'), asserted: w('asserted'), physics: w('physics'), reaches: w('reaches'), nowhere: w('nowhere'), open: w('open'), vanishes: w('vanishes', 2) },
};
export const sound = [
  { beat: 'b01', kind: 'mark' }, { beat: 'b01', cue: 'cut', kind: 'contact' }, { beat: 'b01', cue: 'moves', kind: 'tick' },
  { beat: 'b02', kind: 'reset' }, { beat: 'b02', cue: 'regions', kind: 'mark' },
  { beat: 'b03', kind: 'tick' }, { beat: 'b03', cue: 'boundary', kind: 'mark' },
  { beat: 'b04', kind: 'reset' }, { beat: 'b04', cue: 'exactly', kind: 'contact' }, { beat: 'b04', cue: 'same', kind: 'contact' },
  { beat: 'b05', kind: 'mark' }, { beat: 'b05', cue: 'screen', kind: 'tick' }, { beat: 'b05', cue: 'retina', kind: 'tick' }, { beat: 'b05', cue: 'cortex', kind: 'tick' },
  { beat: 'b06', kind: 'reset' }, { beat: 'b06', cue: 'objects', kind: 'gap' }, { beat: 'b06', cue: 'decided', kind: 'contact' },
  { beat: 'b07', kind: 'mark' }, { beat: 'b07', cue: 'back', kind: 'contact' }, { beat: 'b07', cue: 'ahead', kind: 'rise' },
  { beat: 'b08', kind: 'reset' }, { beat: 'b08', cue: 'threshold', kind: 'fall' }, { beat: 'b08', cue: 'removes', kind: 'gap' }, { beat: 'b08', cue: 'removed', kind: 'mark' },
  { beat: 'b09', kind: 'tick' }, { beat: 'b09', cue: 'close', kind: 'gap' },
  { beat: 'b10', kind: 'reset' }, { beat: 'b10', cue: 'where', kind: 'mark' }, { beat: 'b10', cue: 'higher', kind: 'fall' },
  { beat: 'b11', kind: 'tick' }, { beat: 'b11', cue: 'bench', kind: 'gap' },
  { beat: 'b12', kind: 'reset' }, { beat: 'b12', cue: 'pushed', kind: 'tick' }, { beat: 'b12', cue: 'open', kind: 'rise' }, { beat: 'b12', cue: 'vanishes', kind: 'mark' },
];
export const CARD = 3.6;
