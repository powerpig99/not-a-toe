// Captions: paged from the script's own words, timed from their timestamps, burned in by the page.
//
//   page(words, limits, lang, rate) -> [{ t0, t1, lines }]     pure; runs in Node and in the page
//     words   [{ w, t0, t1 }] in spoken order: timeline beats[].words, joined
//     limits  contract.captions
//     lang    'zh' pages by character: the text is cut into Intl.Segmenter words, punctuation stays with the
//             word it belongs to, and a timed word's span is shared evenly among its characters. Any other
//             lang pages by word.
//     rate    the most characters a second a page may ask of a reader: contract qa.caption_cps_<latin|cjk>.
//             Left out, pages are cut and timed without it.
//     Every sentence starts a page. A sentence too long for one page is cut, into pages and into lines alike,
//     where the text allows it best: at a clause mark; else where a phrase begins (the voice pauses there, or a
//     conjunction, a preposition, an auxiliary or one of the commonest verbs follows: of two such places the one
//     that leaves the lines more even, so a subject is kept whole and its verb starts the line under it, where
//     that is the evener cut, and a preposition starts it where that is); else before a determiner; else before "of". A cut
//     between two other words is made only when the sentence cannot be paged without one, since it may part an
//     adjective from its noun (the pager knows no parts of speech), and a cut after a word that leans on the
//     next (any of those above, a possessive, a subject pronoun, "not") only when even that fails. A page cut
//     out of a sentence is up for BRIEF or more, and no page reads faster than `rate`, while the words allow
//     it. Among cuts as good, fewer pages and even lines. A page starts on its first word, or as much before it
//     as its text needs at `rate`, up to limits.sync_tolerance_s; it ends when the next page starts or LINGER
//     after its last word (when the next page starts within BLINK of that, it stays until then), and never
//     outlasts limits.max_seconds. Text that cannot fit a line throws.
//     The pager is the one source of the timeline's `captions`: build them in Node and let the page draw them.
//
//   captions(stage) -> (t) => void     draws the page of stage.timeline.captions that holds t, in the caption band
import { el, font, scrim } from './text.mjs';

// Seconds a page stays after its last word when no page follows at once. contract.json has no key for it.
const LINGER = 0.5;
// Seconds under which a page cut out of a sentence cannot be read. contract.json has no key for it.
const BRIEF = 1;
// Seconds of bare band between two pages under which the band is not bared: the first page stays until the
// second starts. A page that lingers out a frame or two before the next comes up is a blink of the backing.
// contract.json has no key for it.
const BLINK = 0.3;
// What a cut costs in a line, by its level (see `level`), a cut between pages twice that, and a page; one unit
// is two characters of uneven lines. A cut of level 5 or 6 outweighs any paging of a sentence without one. FAST
// is what each character a second over `rate` costs a page, and SHORT each second it is under BRIEF: a page a
// twentieth of a character a second over the rate, or a hundredth of a second too brief, outweighs any cut, and
// a character a second over weighs what a sixth of a second too brief does.
const LINE = [0, 1, 12, 18, 40, 1e4, 1e5], CUT = LINE.map((c) => 2 * c), PAGE = 10, FAST = 4e6, SHORT = 2.5e7;
// Seconds of silence between two words from which the voice has paused: more than two steps of the aligner's
// 80 ms grid, as one or two come and go inside a phrase (measured on kokoro-george). contract.json has no key for it.
const HUSH = 0.2;

const STOP = /[.!?…。！？]["'”’」』）》)\]]*$/u;
const PAUSE = /[,;:—–，、；：]["'”’」』）》)\]]*$/u;
const CLOSE = /^[\s，。！？；：、…—·”’」』）》〉】,.!?;:)\]]+$/u; // goes with what comes before it
const OPEN = /[“‘「『（《〈【(\[]$/u; // goes with what comes after it
const set = (list) => new Set(list.split(' '));
// Where a phrase begins: conjunctions and prepositions, and auxiliaries (the subject ends before one).
const JOIN = set('and or but nor so yet because if while when where what which who whose how why whether although though unless until since as than that'
  + ' to in on at by for with from into onto over under above below across against along among around round behind beneath beside between beyond inside outside past through toward towards upon within without about after before during');
const AUX = set('is are was were be been being am has have had does do did can could will would shall should may might must cannot ought');
// The commonest verbs, in the one form that is a finite verb and nothing else: a subject ends before one too. The
// pager knows no parts of speech, so a verb whose form is also a noun (runs, turns, moves) is not here.
const VERB = set('takes comes goes makes gives gets keeps becomes brings puts says sees knows seems begins follows belongs carries stays holds sits lets tells thinks happens appears allows requires provides includes continues');
const DET = set('a an the this these those its their his her my your each every any some no both either neither one all more most many much few several');
// Subject pronouns, and "not": like every word above, and "of", they lean on the word after them.
const LEAN = set('it they he she i you we not');

const units = (words, cjk) => {
  if (!cjk) return words.map(({ w, t0, t1 }) => ({ text: w, t0, t1 }));
  const chars = words.flatMap(({ w, t0, t1 }) => {
    const cs = [...w];
    return cs.map((c, i) => ({ c, t0: t0 + (t1 - t0) * i / cs.length, t1: t0 + (t1 - t0) * (i + 1) / cs.length }));
  });
  const out = [];
  let i = 0;
  for (const { segment } of new Intl.Segmenter('zh', { granularity: 'word' }).segment(chars.map(({ c }) => c).join(''))) {
    const n = [...segment].length, last = out.at(-1);
    if (last && (CLOSE.test(segment) || OPEN.test(last.text))) Object.assign(last, { text: last.text + segment, t1: chars[i + n - 1].t1 });
    else out.push({ text: segment, t0: chars[i].t0, t1: chars[i + n - 1].t1 });
    i += n;
  }
  return out;
};

export function page(words, limits, lang, rate) {
  const cjk = lang === 'zh';
  const max = cjk ? limits.max_chars_cjk : limits.max_chars_latin;
  const u = units(words, cjk), join = cjk ? '' : ' ';
  const text = (a, b) => u.slice(a, b).map((x) => x.text).join(join).trim();
  const size = (a, b) => [...text(a, b)].length;
  const word = (i) => u[i].text.toLowerCase().replace(/[^a-z]/g, '');
  // A possessive leans on the next word too. A pronoun before a conjunction or a preposition is an object, and free.
  const leans = (i) => /['’]s$/.test(u[i].text) || JOIN.has(word(i)) || AUX.has(word(i)) || DET.has(word(i)) || word(i) === 'of' || (LEAN.has(word(i)) && !JOIN.has(word(i + 1)));
  // A verb that carries on its clause: one that ends it (a mark follows) is not parted from its subject.
  const verb = (i) => VERB.has(word(i)) && !STOP.test(u[i].text) && !PAUSE.test(u[i].text);
  // How well the text takes a cut after unit i: 0 a sentence end, 1 a clause mark, 6 after a word that leans on
  // the next, 2 where a phrase begins, 3 before a determiner (it parts a verb from its object), 4 before "of" (it
  // hangs on the noun before it), 5 between two other words.
  const level = (i) => STOP.test(u[i].text) ? 0 : PAUSE.test(u[i].text) ? 1 : leans(i) ? 6
    : u[i + 1].t0 - u[i].t1 >= HUSH || JOIN.has(word(i + 1)) || AUX.has(word(i + 1)) || verb(i + 1) ? 2 : DET.has(word(i + 1)) ? 3 : word(i + 1) === 'of' ? 4 : 5;

  // Units [a, b) as one line if they fit, else as up to n lines cut at the best places; nothing if they need more.
  const lines = (a, b, n) => {
    const whole = size(a, b);
    if (whole <= max) return { cuts: [], cost: 0, lo: whole, hi: whole };
    let best;
    for (let k = a + 1; n > 1 && k < b && size(a, k) <= max; k++) {
      const rest = lines(k, b, n - 1);
      if (!rest) continue;
      const lo = Math.min(size(a, k), rest.lo), hi = Math.max(size(a, k), rest.hi);
      const cost = LINE[level(k - 1)] + rest.cost + (hi - lo - rest.hi + rest.lo) / 2;
      if (!best || cost < best.cost) best = { cuts: [k, ...rest.cuts], cost, lo, hi };
    }
    return best;
  };

  // One sentence, units [a, b), as the cheapest run of pages.
  const sentence = (a, b) => {
    const best = [{ cost: 0 }];
    // How long a page of units [j, k) is up: to the next page of the sentence, or LINGER after the sentence's
    // last word, or to the sentence that follows if that is sooner.
    const up = (j, k) => Math.min(k < u.length ? u[k].t0 : Infinity, u[k - 1].t1 + LINGER) - u[j].t0;
    for (let k = a + 1; k <= b; k++) {
      for (let j = a; j < k; j++) {
        const fit = best[j - a] && u[k - 1].t1 - u[j].t0 <= limits.max_seconds && lines(j, k, limits.max_lines);
        if (!fit) continue;
        // A page may start limits.sync_tolerance_s ahead of its first word: it reads too fast only past that.
        const fast = rate ? Math.max(0, size(j, k) / (up(j, k) + limits.sync_tolerance_s) - rate) : 0;
        const short = j > a || k < b ? Math.max(0, BRIEF - up(j, k)) : 0;
        const cost = best[j - a].cost + PAGE + fit.cost + (k < b && CUT[level(k - 1)]) + Math.max(0, max / 2 - size(j, k)) + FAST * fast + SHORT * short;
        if (!best[k - a] || cost < best[k - a].cost) best[k - a] = { cost, from: j, cuts: fit.cuts };
      }
      if (!best[k - a] && k === b) throw new Error(`caption text does not fit a line of ${max}: ${text(a, b)}`);
    }
    const pages = [];
    for (let k = b; k > a; k = best[k - a].from) pages.unshift([best[k - a].from, ...best[k - a].cuts, k]);
    return pages;
  };

  const pages = [];
  for (let a = 0, i = 0; i < u.length; i++) {
    if (STOP.test(u[i].text) || i === u.length - 1) {
      pages.push(...sentence(a, i + 1));
      a = i + 1;
    }
  }
  // Timed from the last page back: a page starts on its first word, or before it by what its text needs at
  // `rate` of the time it is up, which the page after it may already have cut short.
  const out = [];
  for (let p = pages.length - 1, next = Infinity; p >= 0; p--) {
    const edges = pages[p], first = u[edges[0]].t0, lingers = u[edges.at(-1) - 1].t1 + LINGER, end = next - lingers < BLINK ? next : lingers;
    const t0 = rate ? Math.max(first - limits.sync_tolerance_s, Math.min(first, end - size(edges[0], edges.at(-1)) / rate)) : first;
    out.unshift({ t0, t1: Math.min(end, t0 + limits.max_seconds), lines: edges.slice(1).map((b, i) => text(edges[i], b)) });
    next = t0;
  }
  return out;
}

export function captions(stage) {
  const { overlay, contract: { safe }, timeline } = stage;
  const back = scrim(stage, 0.72);
  const root = el(overlay, `position:absolute;left:0;right:0;bottom:${safe.margin_pct}%;display:flex;justify-content:center`);
  const box = el(root, `text-align:center;white-space:nowrap;${font(stage, 'caption')}`);
  box.dataset.role = 'caption';
  let shown;
  return (t) => {
    const cue = timeline.captions.find((c) => c.t0 <= t && t < c.t1);
    if (cue === shown) return;
    shown = cue;
    root.style.visibility = cue ? '' : 'hidden';
    box.replaceChildren(...(cue?.lines ?? []).map((line) => {
      const row = document.createElement('div');
      // The backing runs past the text on both sides as shadow, so the box QA measures is the text alone.
      el(row, `display:inline-block;background:${back};box-shadow:-0.45em 0 0 ${back},0.45em 0 0 ${back}`, line);
      return row;
    }));
  };
}
