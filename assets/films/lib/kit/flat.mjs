// The flat whole-post film: what every such film sets up and draws with. SVG and DOM in the overlay, rebuilt on
// every frame as a pure function of t; every string a label of script.<lang>.json, so the cuts in two languages
// are the same film.
//
//   flat(stage, { slug, base, card, claim, sheet, face }) -> { K, W, T, c, card, script, zh, ease, up, on, frame }
//     base    the film's import.meta.url: script.<lang>.json is read from beside it
//     card    seconds the end card stands, counted back from the film's end
//     claim   { until: (T, c) => seconds }: the label `claim` stands top left from 0.3 s until then
//     sheet   { x, y, w, h, r, fill }: a sheet of paper the film is drawn on, under every plate; the plates' veil
//             is then the sheet's own colour over the sheet, and the ground shows round it
//     face    { en, zh, weight, size }: the labels' font family by language (the contract's mono and cjk when left
//             out), their weight, and the size a label has when none is given
//     K       the palette by name: mind, fail, scaffold, model, loop, ink, muted, rule, ground
//     W       the labels of the script; T the first second of each beat; c(name, beat) a cue's second
//     up(t, t0, d)       eased 0 to 1 over d seconds from t0
//     on(t, t0, t1, d)   1 inside [t0, t1], eased up and down over d
//     frame(t, draw)     draw(pen) builds the frame; then the overlay, the frame text and the caption are set
//   pen: lab(key, x, y, color, a, size, role)                a label centred on (x, y), by its own opacity
//        line(x0, y0, x1, y1, color, a, p, { sw, dash, head })   drawn on by p, an arrow head unless head is false
//        rect(x, y, w, h, stroke, a, { dash, sw, fill })     box(...) the same, centred on (x, y)
//        bar(x, y, w, h, fill, a)   dot(x, y, r, fill, a)   ring(x, y, r, stroke, a, dash, sw)
//        path(d, stroke, a, { sw, dash, fill })              raw(svg)
//        plates([[draw, [[t0, t1], ..]], ..])                each draw(lv) stands on its spans. Plates cross-fade
//                                                            under one veil of ground over the 0.4 s before a change
//                                                            (a faded group would be a layer of its own); lv takes a
//                                                            plate's strings down before that and up after it.
import { captions } from './captions.mjs';
import { labels } from './labels.mjs';
import { between, cues, curves, span } from './rails.mjs';
import { el, texts } from './text.mjs';

export const lerp = (a, b, p) => a + (b - a) * p;

export async function flat(stage, { slug, base, card: hold, claim, sheet, face: faces }) {
  const { overlay, width, height, contract, timeline, lang } = stage;
  const { palette } = contract, zh = lang === 'zh';
  const face = (faces?.[lang] ?? (zh ? contract.type.cjk : contract.type.mono)).replaceAll('"', "'"), weight = faces?.weight ?? 400;
  const leaf = sheet && `x="${sheet.x}" y="${sheet.y}" width="${sheet.w}" height="${sheet.h}" rx="${sheet.r ?? 0}" fill="${sheet.fill}"`;
  const { ease } = curves(contract);
  const c = (name, beat) => cues(timeline)(beat, name);
  const K = { ...Object.fromEntries(Object.entries(palette.semantic).map(([k, v]) => [k, v.hex])), ink: palette.ink, muted: palette.muted, rule: palette.rule, ground: palette.ground };
  const script = await (await fetch(new URL(`./script.${lang}.json`, base))).json();
  const W = script.labels;

  const root = el(overlay, 'position:absolute;inset:0');
  window.__texts = labels(stage).dump;
  const text = texts(stage);
  const T = Object.fromEntries(timeline.beats.map((x) => [x.id, x.t0]));
  const card = timeline.seconds - hold;
  if (claim) text.claim({ text: W.claim, from: 0.3, to: claim.until(T, c), at: [0, 0], width: 0.7 });
  const caption = captions(stage);
  text.endCard({ title: script.title, slug, from: card, veil: 1 });

  const up = (t, t0, d = 0.6) => ease(span(t, t0, t0 + d));
  // With no end it is exactly 1 once up: a plate that never comes down must count as fully up, or the plate before
  // it is still drawn, and veiled, over a canvas plate.
  const on = (t, t0, t1 = Infinity, d = 0.4) => (t1 === Infinity ? ease(span(t, t0, t0 + d)) : between(t, t0, t1, d, ease));

  const frame = (t, draw) => {
    let s = sheet ? `<rect ${leaf}/>` : '', h = '';
    const dim = 1 - up(t, card - 0.3, 0.3);
    const pen = {
      raw: (svg) => { s += svg; },
      lab: (key, x, y, color, a, size = faces?.size ?? 32, role = 'label') => {
        if (!(key in W)) throw new Error(`flat: the script has no label ${key}`);
        if (a > 0) h += `<div data-role="${role}" style="position:absolute;left:${x}px;top:${y}px;transform:translate(-50%,-50%);white-space:nowrap;font:${weight} ${zh ? size + 4 : size}px/1.2 ${face};color:${color};opacity:${a * dim}">${W[key]}</div>`;
      },
      line: (x0, y0, x1, y1, color, a, p = 1, { sw = 4, dash = '', head = true } = {}) => {
        if (a <= 0 || p <= 0) return;
        const x = lerp(x0, x1, p), y = lerp(y0, y1, p), ang = Math.atan2(y1 - y0, x1 - x0) * 180 / Math.PI;
        s += `<line x1="${x0}" y1="${y0}" x2="${x.toFixed(1)}" y2="${y.toFixed(1)}" stroke="${color}" stroke-width="${sw}" ${dash && `stroke-dasharray="${dash}"`} opacity="${a}"/>`;
        if (head) s += `<path d="M0 0l-22 -11v22z" fill="${color}" opacity="${a}" transform="translate(${x.toFixed(1)} ${y.toFixed(1)}) rotate(${ang.toFixed(1)})"/>`;
      },
      rect: (x, y, w, hh, stroke, a, { dash = '', sw = 3, fill = 'none' } = {}) => {
        if (a > 0) s += `<rect x="${x}" y="${y}" width="${w}" height="${hh}" rx="12" fill="${fill}" stroke="${stroke}" stroke-width="${sw}" ${dash && `stroke-dasharray="${dash}"`} opacity="${a}"/>`;
      },
      box: (x, y, w, hh, stroke, a, o) => pen.rect(x - w / 2, y - hh / 2, w, hh, stroke, a, o),
      bar: (x, y, w, hh, fill, a = 1) => { if (a > 0 && hh > 0) s += `<rect x="${x}" y="${y.toFixed(1)}" width="${w}" height="${hh.toFixed(1)}" fill="${fill}" opacity="${a}"/>`; },
      dot: (x, y, r, fill, a = 1) => { if (a > 0) s += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${r}" fill="${fill}" opacity="${a}"/>`; },
      ring: (x, y, r, stroke, a, dash = '12 9', sw = 5) => { if (a > 0) s += `<circle cx="${x.toFixed(1)}" cy="${y}" r="${r}" fill="none" stroke="${stroke}" stroke-width="${sw}" ${dash && `stroke-dasharray="${dash}"`} opacity="${a}"/>`; },
      path: (d, stroke, a, { sw = 4, dash = '', fill = 'none' } = {}) => { if (a > 0) s += `<path d="${d}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}" ${dash && `stroke-dasharray="${dash}"`} opacity="${a}"/>`; },
      plates: (spec) => {
        const live = spec.flatMap(([draw, spans]) => spans.map(([a, b]) => ({ draw, a, pv: on(t, a - 0.4, b + 0.4, 0.4), lv: on(t, a, b - 0.4, 0.3) }))).filter((p) => p.pv > 0).sort((p, q) => p.a - q.a);
        // A plate that is fully up hides every plate before it.
        for (const { draw, pv, lv } of live.slice(Math.max(0, live.findLastIndex((p) => p.pv >= 1)))) {
          draw(lv);
          if (pv < 1) s += sheet ? `<rect ${leaf} opacity="${1 - pv}"/>` : `<rect width="${width}" height="${height}" fill="${K.ground}" opacity="${1 - pv}"/>`;
        }
      },
    };
    draw(pen);
    // The strings go down just before the end card, each by its own opacity; the shapes stay under the card's veil
    // until the veil is full.
    root.innerHTML = t < card + 0.5 ? `<svg width="${width}" height="${height}" style="position:absolute;left:0;top:0">${s}</svg>${t < card ? h : ''}` : '';
    text.show(t);
    caption(t);
  };

  return { K, W, T, c, card, script, zh, ease, up, on, frame };
}
