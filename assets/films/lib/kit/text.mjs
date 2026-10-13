// Overlay text that is placed on the frame, not on the world: title, claim, quote, note and the end card.
// Anchored labels are labels.mjs and captions are captions.mjs; both take their type from here.
// All film text is DOM inside stage.overlay. Each string sits in an element with data-role, which is what
// labels.mjs dump() and its debug painter read: a role is one of title, claim, quote, note, label, caption, url.
//
//   texts(stage) -> { title, claim, quote, note, endCard, show, held }
//     title | claim | quote | note ({ text, from, to, at, width, size, fade })
//         Call them while the film is built: a block is measured once, there and then.
//         text      a string, or [{ text, from }] for parts that come up one after another and clear together
//         from, to  seconds; the block eases up over `fade` from `from` and down to `to` with motion.easing
//         at        [x, y] in 0..1 across the text area (inside the safe margins, above the caption band);
//                   the block is aligned the same way, so [0, 0] pins its top left and [1, 0] its top right
//         width     the widest the block may run, as a share of the frame width
//         size      font px; the default is the role's floor in contract type.floors_px times SCALE
//         A note has a home: the top right of the text area, which is where it stands when no `at` is given.
//         The home holds one note at a time: a note there goes down as the next comes up.
//     endCard({ title, slug, from, veil, fade })   the title and contract end_card.url_template over a veil of
//         palette.ground, from `from` to the end of the film: a dissolve over `fade` seconds, from rest to rest
//         (motion.camera_easing). The veil covers what was added to the overlay before it, so add the end card
//         last; every other block is down by `from`. The URL stands on one line, at the size that fits the
//         text area; a URL that does not fit at its floor fails the build.
//     show(t)   call once per frame
//     held(t)   the boxes of the blocks that are up at t, as [[x, y, w, h]] in format px: what labels.mjs
//               keeps its chips clear of
//
//   font(stage, role, size)        CSS for a role: family by language, weight, size, line height, colour
//   floor(contract, role, cjk)     the role's floor in px
//   area(stage)                    the box non-caption text may use, in format px
//   scrim(stage, alpha)            palette.ground at an alpha, as a CSS colour: what labels, notes and captions sit on
//   halo(stage)                    CSS for a ground-coloured glow round the letters: what title, claim and quote
//                                  carry, so that large type needs no panel behind it
//   el(parent, css, text)          a div
import { between, curves } from './rails.mjs';

// Size of each role over its floor. Design values, not floors: a film may pass its own size. With the floors
// of today they come to title 70, claim 45, quote 38, url 36, caption 44 (Latin) and 40 (CJK), label 28, note 24.
const SCALE = { title: 2.5, claim: 1.6, quote: 1.35, url: 1.5, caption: 1.1, label: 1, note: 1 };
const FLOOR = { title: 'body', claim: 'body', quote: 'body', label: 'label' };
const FADE = 0.4;

export const floor = ({ type }, role, cjk) => type.floors_px[role === 'caption' ? (cjk ? 'caption_cjk' : 'caption_latin') : FLOOR[role] ?? 'minimum'];

export const el = (parent, css, text) => {
  const e = document.createElement('div');
  e.style.cssText = css;
  if (text !== undefined) e.textContent = text;
  parent.append(e);
  return e;
};

export const font = ({ lang, contract }, role, size) => {
  const { type, palette } = contract;
  const zh = lang === 'zh';
  const serif = zh ? type.cjk : type.serif;
  // The mono face has no Han glyphs, and what Chrome falls back to for them is a sans, which the brand does not use.
  const mono = zh && role !== 'url' ? type.cjk : type.mono;
  const px = size ?? Math.round(floor(contract, role, zh) * SCALE[role]);
  return {
    title: `font:700 ${px}px/1.15 ${serif};letter-spacing:-0.015em;color:${palette.ink}`,
    claim: `font:400 ${px}px/1.3 ${serif};color:${palette.ink}`,
    quote: `font:400 ${px}px/1.35 ${serif};color:${palette.ink}`,
    caption: `font:400 ${px}px/1.3 ${serif};color:${palette.ink}`,
    label: `font:400 ${px}px/1.2 ${mono};color:${palette.ink}`,
    note: `font:400 ${px}px/1.25 ${mono};color:${palette.muted}`,
    url: `font:400 ${px}px/1.4 ${mono};color:${palette.muted}`,
  }[role];
};

export const area = ({ width, height, contract: { safe } }) => ({
  x0: width * safe.margin_pct / 100, y0: height * safe.margin_pct / 100,
  x1: width * (1 - safe.margin_pct / 100), y1: height * (1 - safe.caption_band_pct / 100),
});

export const scrim = ({ contract: { palette } }, alpha) => palette.ground + Math.round(alpha * 255).toString(16).padStart(2, '0');

export const halo = ({ contract: { palette } }) => `text-shadow:${[0.06, 0.14, 0.3, 0.6].map((em) => `0 0 ${em}em ${palette.ground}`).join(',')}`;

export function texts(stage) {
  const { overlay, width, height, contract } = stage;
  const { ease, glide } = curves(contract);
  const box = area(stage);
  const shown = [], blocks = [];
  let card = Infinity; // seconds at which the end card begins

  const backing = { title: halo(stage), claim: halo(stage), quote: `${halo(stage)};padding:0.1em 0 0.1em 0.8em;border-left:3px solid ${contract.palette.muted}`, note: `background:${scrim(stage, 0.9)};padding:5px 12px`, url: 'white-space:nowrap' };
  const zoom = width / overlay.getBoundingClientRect().width;
  const range = document.createRange();

  // One block: parts stacked in a column, each with its own backing and its own time to come up.
  const block = (role, { text, from, to = Infinity, at: [ax, ay], width: share, size, fade = FADE, gap = 0, curve = ease, home = false }) => {
    const align = ax < 1 / 3 ? 'left' : ax > 2 / 3 ? 'right' : 'center', parts = [];
    const root = el(overlay, `position:absolute;left:${box.x0 + ax * (box.x1 - box.x0)}px;top:${box.y0 + ay * (box.y1 - box.y0)}px;
      transform:translate(${-ax * 100}%,${-ay * 100}%);width:max-content;max-width:${share * width}px;display:flex;flex-direction:column;
      gap:${gap}px;align-items:${{ left: 'flex-start', center: 'center', right: 'flex-end' }[align]};text-align:${align}`);
    for (const part of typeof text === 'string' ? [{ text }] : text) {
      const kind = part.role ?? role;
      const back = el(root, backing[kind]);
      const words = el(back, `display:inline-block;text-wrap:balance;${font(stage, kind, part.size ?? size)}`, part.text);
      words.dataset.role = kind;
      // A wrapped block is as wide as the room it was given; its box is brought in to its longest line.
      range.selectNodeContents(words);
      words.style.width = `${Math.ceil(range.getBoundingClientRect().width * zoom)}px`;
      parts.push({ node: back, from: part.from ?? from, to, fade, strength: 1, curve });
    }
    shown.push(...parts);
    const r = root.getBoundingClientRect(), o = overlay.getBoundingClientRect();
    blocks.push({ parts, home, from, rect: [(r.x - o.x) * zoom, (r.y - o.y) * zoom, r.width * zoom, r.height * zoom] });
  };

  // The largest size, no larger than the role's own, at which a string stands on one line of the text area.
  const fit = (role, string) => {
    const probe = el(overlay, `position:absolute;visibility:hidden;white-space:nowrap;${font(stage, role)}`, string), px = parseFloat(probe.style.fontSize);
    const size = Math.min(px, Math.floor(px * (box.x1 - box.x0) / (probe.getBoundingClientRect().width * zoom)));
    probe.remove();
    if (size < floor(contract, role)) throw new Error(`text: "${string}" does not fit one line of the text area at ${floor(contract, role)} px, the floor of ${role}`);
    return size;
  };
  const alpha = ({ from, to, fade, curve }, t) => between(t, from, to, fade, curve);

  return {
    title: (o) => block('title', { at: [0.5, 0.5], width: 0.8, ...o }),
    claim: (o) => block('claim', { at: [0, 0], width: 0.5, gap: 6, ...o }),
    quote: (o) => block('quote', { at: [0, 0], width: 0.5, ...o }),
    note: (o) => {
      block('note', { at: [1, 0], width: 0.4, home: !o.at, ...o });
      const mine = blocks.at(-1);
      if (!mine.home) return;
      for (const other of blocks.filter((b) => b.home && b !== mine)) {
        const [first, next] = other.from < mine.from ? [other, mine] : [mine, other];
        for (const part of first.parts) part.to = Math.min(part.to, next.from);
      }
    },
    endCard: ({ title, slug, from, veil = 0.9, fade = FADE }) => {
      const url = contract.end_card.url_template.replace('<slug>', slug);
      for (const b of blocks) for (const part of b.parts) part.to = Math.min(part.to, from);
      card = from;
      shown.push({ node: el(overlay, `position:absolute;inset:0;background:${contract.palette.ground}`), from, to: Infinity, fade, strength: veil, curve: glide });
      block('title', { at: [0.5, 0.5], width: 0.9, gap: Math.round(height * 0.04), from, fade, curve: glide, text: [{ text: title }, { role: 'url', text: url, size: fit('url', url) }] });
    },
    show: (t) => {
      for (const part of shown) {
        const a = alpha(part, t);
        part.node.style.visibility = a ? '' : 'hidden';
        part.node.style.opacity = a * part.strength;
      }
    },
    held: (t) => (t < card ? blocks.filter((b) => b.parts.some((part) => alpha(part, t))).map((b) => b.rect) : []),
  };
}
