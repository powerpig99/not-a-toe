// A slide rule on a blueprint. The measurement chain is one long rule with five stations on it: the particle and its
// slits, the screen, the retina, the nerve, the cortex. A glass cursor with a hairline rides the rule and is set by
// a green tab. Left of the hairline the track is a bundle of waves; right of it, one dot on a straight line. Under
// the rule a readout of seven bars never changes height, wherever the cursor is slid and whatever name is hung over
// it. Over the rule a chart of outlined regions is the map of interpretations. Green is the tab and what is chosen;
// red the rivet, the strike-out and the sheet that is not there; amber names, scales and the chart; pale blue-white
// the drawing itself; purple the loop of self-reference. Every moment is a cue of the timeline and every string a
// label of script.<lang>.json. The frame is a pure function of t.
import { flat, lerp } from '../../lib/kit/flat.mjs';
import { CARD } from './plan.mjs';

const SLUG = 'the-cut-moves-but-never-vanishes';
const FACE = { en: "'Film Sans', 'Avenir Next', 'Helvetica Neue', sans-serif", zh: "'Film Sans', 'PingFang SC', 'Avenir Next', sans-serif", weight: 600, size: 32 };
const BLUE = '#143e73', SHEET = { x: 60, y: 44, w: 1800, h: 840, r: 6, fill: BLUE };
const C = { ink: '#eef4ff', soft: '#a9c3e6', faint: '#2a5594', mind: '#8ff0a4', fail: '#ff9d8f', amber: '#ffd27a', loop: '#d3b8ff' };
const RX0 = 200, RX1 = 1720, RY = 560, RT = 470, RB = 650;
const ST = { particle: 300, screen: 640, retina: 980, nerve: 1320, cortex: 1640 };
const GAP = { a: 470, b: 810, c: 1150, d: 1480 };
const BARS = [0.25, 0.7, 0.35, 1, 0.35, 0.7, 0.25], BX0 = 758, BW = 44, BG = 16, BBASE = 852, BH = 86;
const CH = { x: 520, y: 150, w: 880, h: 250 }, OX = 548, OY = 392;
const REG = [[640, 330, 70, 38], [800, 235, 74, 36], [960, 318, 66, 40], [1130, 228, 78, 36], [1290, 312, 64, 38]];
const hex = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
const mix = (a, k, b = BLUE) => { const A = hex(a), B = hex(b); return '#' + A.map((v, i) => Math.round(lerp(v, B[i], k)).toString(16).padStart(2, '0')).join(''); };
const rng = (seed) => () => { seed |= 0; seed = seed + 0x6d2b79f5 | 0; let r = Math.imul(seed ^ seed >>> 15, 1 | seed); r = r + Math.imul(r ^ r >>> 7, 61 | r) ^ r; return ((r ^ r >>> 14) >>> 0) / 4294967296; };
const rnd = rng(382), CLUSTER = Array.from({ length: 22 }, (_, i) => { const a = rnd() * 6.283, r = 12 + rnd() * 46, right = i % 2; return [(right ? 1030 : 880) + Math.cos(a) * r * 1.25, 280 + Math.sin(a) * r * 0.8, right]; });
let GRID = '';
for (let x = 120; x < 1860; x += 60) GRID += `M${x} 44V884`;
for (let y = 104; y < 884; y += 60) GRID += `M60 ${y}H1860`;
let TICKS = '';
for (let i = 0; i <= 80; i++) { const x = RX0 - 40 + i * 20; TICKS += `M${x} ${RT}v${i % 5 ? 9 : 18}M${x} ${RB}v${i % 5 ? -9 : -18}`; }

export default async function film(stage) {
  const { W, T, c, zh, up, on, frame } = await flat(stage, { slug: SLUG, base: import.meta.url, card: CARD, face: FACE, sheet: SHEET });
  const ORDER = Object.keys(T).sort((a, b) => T[a] - T[b]);
  const ctx = document.createElement('canvas').getContext('2d'), widths = new Map();
  const wd = (key, size) => {
    const id = `${key}/${size}`;
    if (!widths.has(id)) { ctx.font = `${FACE.weight} ${zh ? size + 4 : size}px ${zh ? FACE.zh : FACE.en}`; widths.set(id, ctx.measureText(W[key]).width); }
    return widths.get(id);
  };
  // moments that outlast their beat
  const M = {
    rule: T.b01 + 0.3, bars: c('precision', 'b01') - 0.4, cur: c('cut', 'b01') - 0.2,
    chart1: c('space', 'b02') - 0.3, lift: c('objects', 'b06'), set: c('decided', 'b06') - 0.5,
    rivet: c('threshold', 'b08'), strike: c('removes', 'b08'), undo: c('prop', 'b08'), model: c('model', 'b08') - 0.3,
    bench: c('bench', 'b11'), again: c('instrument', 'b12') - 0.3,
  };
  const SLIDES = [
    [c('moves', 'b01'), GAP.c, 1.2], [c('moves', 'b01') + 1.7, GAP.b, 1.2],
    [c('screen', 'b05') - 0.3, GAP.a, 0.8], [c('retina', 'b05') - 0.3, GAP.b, 0.8], [c('cortex', 'b05') - 0.3, GAP.d, 0.9],
    [c('slides', 'b06'), GAP.b, 1.4], [M.set, 700, 0.8], [T.b08, GAP.b, 0.8], [c('moves', 'b08'), GAP.c, 1.2], [c('removed', 'b08'), GAP.b, 1.0],
    [c('pushed', 'b12') - 0.2, GAP.a, 0.9], [c('pushed', 'b12') + 1.0, GAP.d, 1.8], [c('physics', 'b12'), GAP.b, 1.4],
  ];
  const FLASH = [c('exactly', 'b04'), c('same', 'b04'), c('probabilities', 'b05'), c('weights', 'b12'), ...SLIDES.map(([t0, , d]) => t0 + d)];

  const renderAt = (t) => frame(t, (pen) => {
    const backs = [];
    const U = (t0, d = 0.6) => up(t, t0, d);
    const id = ORDER.findLast((b) => t >= T[b]) ?? ORDER[0], next = T[ORDER[ORDER.indexOf(id) + 1]] ?? Infinity;
    const g = (n) => c(n, id), till = (x0, x1 = Infinity) => on(t, x0, Math.min(x1, next - 0.45), 0.35);
    const is = (b) => id === b;
    // A label on a plate of the sheet's blue, so that no line shows through its letters; kept inside the safe margin.
    const tag = (key, x, y, color, a, size = FACE.size, role = 'label') => {
      if (!(a > 0)) return;
      const w = wd(key, size) + 30, h = (zh ? size + 4 : size) * 1.2 + 12;
      x = Math.min(1810 - w / 2, Math.max(110 + w / 2, x));
      backs.push([x - w / 2, y - h / 2, w, h, Math.min(1, a * 1.6)]);
      pen.lab(key, x, y, color, a, size, role);
    };
    const head = (key, color, a, size = 40, role = 'label') => tag(key, 960, 104, color, a, size, role);
    const seg = (x0, y0, x1, y1, color, a, sw = 3, dash = '') => pen.line(x0, y0, x1, y1, color, a, 1, { sw, dash, head: false });

    // ---- the sheet
    pen.path(GRID, C.faint, 0.55, { sw: 1 });
    pen.rect(78, 62, 1764, 804, C.faint, 0.9, { sw: 2 });

    // ---- what stands when
    const seam = on(t, T.b07, T.b08 - 0.5, 0.5);
    const chartA = Math.max(on(t, M.chart1, T.b05 - 0.45, 0.4), on(t, T.b09 + 0.2, T.b12 - 0.45, 0.4));
    const chartFocus = Math.max(on(t, M.chart1, T.b04 - 0.4, 0.5), on(t, T.b09 + 0.3, M.bench - 0.4, 0.5));
    const ruleA = U(M.rule, 0.8) * (1 - seam), dimK = 0.5 * chartFocus, INK = mix(C.ink, dimK), SOFT = mix(C.soft, dimK);
    const lifted = on(t, M.lift, M.set, 0.5), struck = on(t, M.strike, M.undo, 0.4), away = on(t, M.bench, M.again, 0.5);
    const present = U(M.cur, 0.5) * (1 - lifted) * (1 - struck) * (1 - away);
    const cx = SLIDES.reduce((x, [t0, to, d]) => lerp(x, to, up(t, t0, d)), GAP.b);
    const modelA = on(t, M.model, T.b09 - 0.45, 0.4);

    // ---- the rule: body, scales, stations, track
    if (ruleA > 0) {
      const draw = U(M.rule, 1.4);
      pen.line(RX0 - 40, RT, RX1 + 40, RT, INK, ruleA, draw, { sw: 4, head: false }); pen.line(RX0 - 40, RB, RX1 + 40, RB, INK, ruleA, draw, { sw: 4, head: false });
      const body = ruleA * U(M.rule + 1.0, 0.6);
      seg(RX0 - 40, RT, RX0 - 40, RB, INK, body, 4); seg(RX1 + 40, RT, RX1 + 40, RB, INK, body, 4);
      pen.path(TICKS, SOFT, 0.8 * body, { sw: 2 });
      // the track: waves up to the hairline, then one dot on a straight line
      const wave = (k, x1) => { let d = ''; for (let x = RX0; x <= x1; x += 8) d += `${x === RX0 ? 'M' : 'L'}${x} ${(RY + Math.sin(x / (34 + k * 9) + t * (1.1 + k * 0.4) + k * 2) * (16 + k * 5)).toFixed(1)}`; return d; };
      for (let k = 0; k < 3; k++) {
        pen.path(wave(k, RX1), SOFT, body * (1 - present) * 0.9, { sw: 3 });
        if (present > 0) pen.path(wave(k, Math.max(RX0 + 8, cx)), SOFT, body * present * 0.9, { sw: 3 });
      }
      seg(cx, RY, RX1, RY, INK, body * present, 4);
      pen.dot(Math.min(RX1 - 20, cx + 70), RY, 11, C.ink, body * present);
      // the stations
      const sa = body;
      pen.dot(ST.particle, RY, 12, BLUE, sa); pen.ring(ST.particle, RY, 12, INK, sa, '', 4);
      [[-52, -22], [-10, 10], [22, 52]].forEach(([a, b]) => seg(ST.particle + 62, RY + a, ST.particle + 62, RY + b, INK, sa, 5));
      pen.rect(ST.screen - 9, RY - 58, 18, 116, INK, sa, { sw: 4, fill: BLUE });
      pen.path(`M${ST.retina + 26} ${RY - 54}A58 58 0 0 0 ${ST.retina + 26} ${RY + 54}`, INK, sa, { sw: 5 });
      pen.path(`M${ST.nerve - 44} ${RY}l14 -24l20 48l20 -48l20 48l14 -24`, INK, sa, { sw: 4 });
      pen.rect(ST.cortex - 32, RY - 32, 64, 64, INK, sa, { sw: 4, fill: BLUE });
      pen.path(`M${ST.cortex - 11} ${RY - 32}v64M${ST.cortex + 11} ${RY - 32}v64M${ST.cortex - 32} ${RY - 11}h64M${ST.cortex - 32} ${RY + 11}h64`, INK, sa, { sw: 2 });
    }

    // ---- the cursor: a glass frame, a hairline, a green tab
    const curA = ruleA * U(M.cur, 0.5) * (1 - away) * (1 - 0.6 * struck) * (1 - 0.75 * lifted), dy = -60 * lifted;
    if (curA > 0) {
      pen.raw(`<rect x="${(cx - 46).toFixed(1)}" y="${RT - 26 + dy}" width="92" height="${RB - RT + 52}" rx="10" fill="${C.ink}" opacity="${(0.07 * curA).toFixed(3)}"/>`);
      pen.raw(`<rect x="${(cx - 46).toFixed(1)}" y="${RT - 26 + dy}" width="92" height="${RB - RT + 52}" rx="10" fill="none" stroke="${C.ink}" stroke-width="4" opacity="${curA.toFixed(3)}"/>`);
      seg(cx, RT - 26 + dy, cx, RB + 26 + dy, C.amber, curA, 3);
      pen.raw(`<rect x="${(cx - 30).toFixed(1)}" y="${RT - 60 + dy}" width="60" height="30" rx="8" fill="${C.mind}" opacity="${curA.toFixed(3)}"/>`);
    }
    const rivet = ruleA * on(t, M.rivet, M.strike - 0.3, 0.4);
    if (rivet > 0) { pen.dot(cx, RT - 2, 15, C.fail, rivet); seg(cx - 8, RT - 10, cx + 8, RT + 6, BLUE, rivet, 4); seg(cx - 8, RT + 6, cx + 8, RT - 10, BLUE, rivet, 4); pen.dot(cx, RB + 2, 15, C.fail, rivet); }
    const sx = ruleA * struck;
    if (sx > 0) { const p = U(M.strike, 0.5); pen.line(cx - 70, RT - 50, cx + 70, RB + 50, C.fail, sx, p, { sw: 7, head: false }); pen.line(cx + 70, RT - 50, cx - 70, RB + 50, C.fail, sx, U(M.strike + 0.25, 0.5), { sw: 7, head: false }); }

    // ---- the readout: seven bars that never change height
    const barsA = ruleA * U(M.bars, 0.6) * (1 - away) * (1 - modelA);
    if (barsA > 0) {
      const fl = Math.max(0, ...FLASH.map((f) => on(t, f - 0.1, f + 0.9, 0.25)));
      pen.rect(BX0 - 26, BBASE - BH - 16, 7 * BW + 6 * BG + 52, BH + 26, mix(C.soft, 0.3 - 0.3 * fl), barsA, { sw: 3 });
      BARS.forEach((h, i) => pen.bar(BX0 + i * (BW + BG), BBASE - h * BH, BW, h * BH, mix(C.ink, 0.25 - 0.25 * fl), barsA));
    }

    // ---- the chart: the map of interpretations
    if (chartA > 0) {
      const smooth = is('b11') ? U(c('smooth', 'b11') - 0.3, 0.8) : 0, CK = is('b04') ? 0.45 : 0, AMB = mix(C.amber, CK);
      pen.rect(CH.x, CH.y, CH.w, CH.h, AMB, chartA, { sw: 3, fill: BLUE });
      const ax = chartA * (t < T.b05 ? U(c('axes', 'b02') - 0.3, 0.6) : 1) * (1 - smooth);
      pen.line(OX, OY, 1380, OY, AMB, ax, t < T.b05 ? U(c('axes', 'b02') - 0.3, 0.8) : 1, { sw: 3 }); pen.line(OX, OY, OX, 168, AMB, ax, t < T.b05 ? U(c('axes', 'b02') + 0.2, 0.8) : 1, { sw: 3 });
      pen.line(OX, OY, 1150, 172, AMB, 0.8 * ax, t < T.b05 ? U(c('axes', 'b02') + 0.7, 0.8) : 1, { sw: 3, dash: '10 8' });
      const sel = is('b03') ? ['copenhagen', 'worlds', 'trajectory', 'someone', 'geometry'].map((n, i, a) => on(t, g(n) - 0.2, i + 1 < a.length ? g(a[i + 1]) - 0.3 : g('boundary') - 0.3, 0.3)) : [0, 0, 0, 0, 0];
      const all = is('b03') ? U(g('boundary') - 0.3, 0.5) : 0, corner = is('b02') ? on(t, g('corner') - 0.6, g('settled') - 0.3, 0.4) : 0;
      const score = is('b09') ? [on(t, g('low') - 0.2, g('exhibit') - 0.3, 0.3), 0, 0, on(t, g('high') - 0.2, g('exhibit') - 0.3, 0.3), 0] : [0, 0, 0, 0, 0];
      REG.forEach(([x, y, rx, ry], i) => {
        const a = chartA * (t < T.b05 ? U(c('regions', 'b02') - 0.3 + i * 0.18, 0.5) : 1) * (1 - smooth), hot = Math.max(sel[i], all * 0.7, i === 0 || i === 2 ? corner : 0, score[i]);
        if (a > 0) pen.raw(`<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="${BLUE}" stroke="${mix(hot > 0 ? C.amber : C.soft, CK + (hot > 0 ? 0 : 0.15))}" stroke-width="${hot > 0.5 ? 5 : 3}" ${all > 0.5 ? 'stroke-dasharray="12 8"' : ''} opacity="${a.toFixed(3)}"/>`);
      });
      if (smooth > 0) {
        [[150, 78], [215, 104], [285, 118]].forEach(([rx, ry], k) => pen.raw(`<path d="M${955 - rx} 282c0 ${-ry * 1.25} ${rx * 0.9} ${-ry} ${rx} ${-ry * 0.7}s${rx} ${ry * 0.1} ${rx} ${ry * 0.7}s${-rx * 0.8} ${ry} ${-rx} ${ry * 0.8}s${-rx} ${-ry * 0.1} ${-rx} ${-ry * 0.8}z" fill="none" stroke="${C.soft}" stroke-width="2.5" opacity="${(chartA * smooth * (0.9 - k * 0.2)).toFixed(3)}"/>`));
        CLUSTER.forEach(([x, y, right], i) => pen.dot(x, y, 7, right ? C.ink : C.amber, chartA * U(c('clusters', 'b11') - 0.3 + i * 0.05, 0.4)));
        const ta = chartA * U(c('tags', 'b11') - 0.2, 0.5);
        [[850, 215, -1], [1060, 215, 1]].forEach(([x, y, s]) => { seg(x, y + 22, x + s * 46, y - 18, C.loop, ta, 3); pen.rect(x + s * 46 - (s < 0 ? 64 : 0), y - 34, 64, 30, C.loop, ta, { sw: 3, fill: BLUE }); });
      }
    }

    // ---- what each beat adds
    if (is('b01')) {
      head('claim', C.ink, Math.max(till(0.3, g('hundred') - 0.5), till(g('moves') - 0.3)), 40, 'claim');
      tag('precision', 1420, 800, C.ink, till(g('precision') - 0.2, g('map') - 0.3)); head('century', C.amber, till(g('hundred') - 0.2, g('scaffold') - 0.4));
      head('scaffold', C.amber, till(g('scaffold') - 0.2, g('someone') - 0.4));
      tag('thecut', cx, RT - 96, C.mind, till(g('cut') - 0.1, g('moves') - 0.5), 34);
    }

    if (is('b02')) {
      head('regions', C.amber, till(g('regions') - 0.2, g('axes') - 0.4)); head('address', C.amber, till(g('address') - 0.3));
      const a0 = g('axes'), k = (g('corner') - a0) / 4.6, end = g('settled') - 0.3;
      tag('process', 1290, OY - 26, C.amber, till(a0 + 0.9 * k, end), 28); tag('implicate', 690, 182, C.amber, till(a0 + 1.7 * k, end), 28);
      tag('wholeness', 1240, 182, C.amber, till(a0 + 2.6 * k, end), 28); tag('selfref', 760, OY - 26, C.loop, till(a0 + 3.4 * k, end), 28);
    }

    if (is('b03')) {
      ['copenhagen', 'manyworlds', 'bohm', 'held', 'geometry'].forEach((key, i) => { const n = ['copenhagen', 'worlds', 'trajectory', 'someone', 'geometry']; tag(key, REG[i][0], REG[i][1], C.ink, till(g(n[i]) - 0.2, i < 4 ? g(n[i + 1]) - 0.3 : g('boundary') - 0.3), 28); });
      head('boundary', C.amber, till(g('boundary') - 0.3));
    }

    if (is('b04')) {
      const plate = (key, a, b) => tag(key, 960, 716, C.amber, till(a, b), 30);
      plate('exclusion', g('exclusion') - 0.2, g('constraint') - 0.3); plate('constraint', g('constraint') - 0.1, g('pattern') - 0.3); plate('pattern', g('pattern') - 0.1, g('folded') - 1.6);
      plate('folded', g('folded') - 1.2, g('neighbours') - 0.4); tag('same', 1420, 800, C.ink, till(g('same') - 0.5, g('neighbours') - 0.4));
      head('neighbours', C.amber, till(g('neighbours') - 0.3));
    }

    if (is('b05')) {
      tag('possibilities', 430, 400, C.soft, till(g('possibilities') - 0.8, g('moved') - 0.3)); tag('record', 1490, 400, C.ink, till(g('record') - 0.8, g('moved') - 0.3));
      head('mcut', C.mind, till(g('cut') - 0.6));
      tag('screen', ST.screen, 692, C.ink, till(g('screen') - 0.2), 28); tag('retina', ST.retina, 692, C.ink, till(g('retina') - 0.2), 28); tag('cortex', ST.cortex, 692, C.ink, till(g('cortex') - 0.2), 28);
      tag('nochange', 1420, 800, C.ink, till(g('probabilities') + 0.3));
    }

    if (is('b06')) {
      head('slides', C.mind, till(g('slides') - 0.3, g('taken') - 0.6)); head('notout', C.mind, till(g('taken') - 0.5, g('objects') - 0.3));
      const s0 = g('chain'), s1 = g('marked'), p = Math.min(1, Math.max(0, (t - s0) / (s1 - s0))), sxx = lerp(ST.particle, ST.cortex, p * p * (3 - 2 * p)), sa = till(s0 - 0.3, g('decided') - 0.6);
      pen.ring(sxx, RY, 74, C.fail, sa, '12 9', 4);
      tag('here', sxx, 400, C.fail, till(s0 + 0.2, g('decided') - 0.6), 30);
      head('decided', C.mind, till(g('decided') - 0.3, g('arrangement') - 0.5)); tag('fact', 1490, 400, C.ink, till(g('fact') - 0.6, g('arrangement') - 0.5));
      head('question', C.mind, till(g('question') - 1.2));
    }

    if (is('b07')) {
      const SX = 960, a = till(T.b07 + 0.3);
      pen.line(SX, 170, SX, 730, C.amber, a, U(g('seam') - 0.6, 0.9), { sw: 6, head: false });
      head('seam', C.amber, till(g('seam') - 0.6, g('chosen') - 0.6));
      // the side that is chosen: a tab set to one of three notches
      const NY = [300, 440, 580], la = till(g('chosen') - 0.8), ky = lerp(lerp(NY[0], NY[1], U(g('slits') - 0.2, 0.6)), NY[2], U(g('back') - 2.4, 0.6));
      NY.forEach((y) => { pen.ring(430, y, 20, C.soft, la, '', 3); seg(456, y, 520, y, C.soft, 0.6 * la, 2, '6 8'); });
      pen.dot(430, ky, 24, C.mind, la); pen.line(462, ky, SX - 16, ky, C.mind, la, U(g('chosen') - 0.4, 0.8), { sw: 5 });
      tag('chosen', 430, 216, C.mind, till(g('chosen') - 0.4, g('effect') - 0.6), 34);
      // the side that is not: bars that fill to their own heights
      const ra = till(g('back') - 0.4), X0 = 1140, BWW = 54, GG = 20, BASE = 610, HH = 270;
      BARS.forEach((h, i) => pen.bar(X0 + i * (BWW + GG), BASE - h * HH * U(g('back') + i * 0.14, 1.8), BWW, h * HH * U(g('back') + i * 0.14, 1.8), C.ink, ra));
      seg(X0 - 20, BASE + 3, X0 + 7 * BWW + 6 * GG + 20, BASE + 3, C.soft, ra, 3);
      tag('notchosen', X0 + 250, 216, C.ink, till(g('back') + 0.4, g('effect') - 0.6), 34); tag('born', X0 + 250, 664, C.amber, till(g('born') - 0.3, g('effect') - 0.6), 30);
      // each reading an effect and a cause: dots landed one by one, a green mark one step ahead
      const e0 = g('effect') - 0.3, ea = till(e0), n = Math.min(8, Math.max(0, (t - e0) / 0.55)), k = Math.floor(n), DX = (i) => 430 + i * 130, DY = 772;
      for (let i = 0; i < Math.min(k + 1, 8); i++) pen.dot(DX(i), DY, 12, C.ink, ea * (i < k ? 1 : n - k));
      for (let i = 0; i < Math.min(k, 7); i++) seg(DX(i) + 18, DY, DX(i + 1) - 18, DY, C.soft, ea, 3);
      if (ea > 0) { pen.raw(`<path d="M0 -16l15 16l-15 16l-15 -16z" fill="${C.mind}" opacity="${ea.toFixed(3)}" transform="translate(${DX(n + 1).toFixed(1)} ${DY})"/>`); }
      tag('effect', 620, 836, C.ink, till(g('effect') - 0.3, g('gap') - 2.2), 30); tag('cause', 1300, 836, C.mind, till(g('cause') - 0.3, g('gap') - 2.2), 30);
      head('ahead', C.mind, till(g('ahead') - 0.8));
    }

    if (is('b08')) {
      head('thing', C.fail, till(g('threshold') - 0.2, g('removes') - 0.5)); head('removes', C.fail, till(g('removes') - 0.2, g('only') - 1.2));
      head('onereading', C.ink, till(g('only') - 1.0, g('prop') - 1.6)); head('prop', C.fail, till(g('prop') - 0.4, g('apparatus') - 1.8));
      const names = ['apparatus', 'branch', 'trajectory', 'belief', 'sample'], keys = ['apparatus', 'branch', 'traj', 'belief', 'sample'], xs = [600, 900, 1090, 1260, 1480];
      names.forEach((nm, i) => {
        const a = till(g(nm) - 0.3, g('removed') - 0.4);
        if (a > 0) pen.raw(`<path d="M0 0l-13 24h26z" fill="${C.amber}" opacity="${a.toFixed(3)}" transform="translate(${xs[i]} ${RB + 8})"/>`);
        head(keys[i], C.amber, till(g(nm) - 0.3, i < 4 ? g(names[i + 1]) - 0.35 : g('moves') - 0.5));
      });
      head('firstperson', C.mind, till(g('removed') + 0.6, g('model') - 0.9));
      // a model shrunk weight by weight: grids of numbers, and no mark between any two
      const GX = [520, 740, 960, 1180, 1400], N = [6, 5, 4, 3, 2];
      GX.forEach((x, i) => { const a = modelA * U(M.model + i * 0.3, 0.5), n = N[i]; for (let r = 0; r < n; r++) for (let q = 0; q < n; q++) pen.dot(x + (q - (n - 1) / 2) * 15, 800 + (r - (n - 1) / 2) * 15, 4.5, C.soft, a); });
      for (let i = 0; i < 4; i++) seg(GX[i] + 60, 800, GX[i + 1] - 60, 800, C.soft, 0.7 * modelA * U(M.model + 0.4 + i * 0.3, 0.5), 2, '5 8');
      head('nomark', C.ink, till(g('marks') - 0.8));
    }

    if (is('b09')) {
      head('axis', C.loop, till(g('axis') - 0.3, g('exhibit') - 0.5));
      const p = U(g('axis') - 0.3, 0.9), aa = till(g('axis') - 0.3) * chartA;
      pen.line(OX, OY, 1150, 172, C.loop, aa, p, { sw: 5 });
      for (let i = 1; i < 6; i++) { const x = lerp(OX, 1150, i / 6), y = lerp(OY, 172, i / 6); seg(x - 4, y - 11, x + 4, y + 11, C.loop, aa * U(g('axis') + i * 0.1, 0.3), 3); }
      tag('high', REG[3][0], REG[3][1], C.loop, till(g('high') - 0.2, g('exhibit') - 0.3), 28); tag('low', REG[0][0], REG[0][1], C.loop, till(g('low') - 0.2, g('exhibit') - 0.3), 28);
      head('exhibit', C.ink, till(g('exhibit') - 0.4, g('gaze') - 0.8)); head('gaze', C.loop, till(g('gaze') - 0.6, g('formal') - 0.5));
      // a loop that tries to pass through its own start and is left open
      const la = till(g('differentiation') - 0.6), lp = 0.9 * U(g('differentiation') - 0.6, 1.6), LX = 300, LY = 290, R = 86;
      if (la > 0) {
        pen.raw(`<circle cx="${LX}" cy="${LY}" r="${R}" fill="none" stroke="${C.loop}" stroke-width="6" stroke-linecap="round" pathLength="1" stroke-dasharray="${lp.toFixed(3)} 1" transform="rotate(-90 ${LX} ${LY})" opacity="${la.toFixed(3)}"/>`);
        const ang = lp * 6.283 - 1.571; pen.raw(`<path d="M0 0l-20 -10v20z" fill="${C.loop}" opacity="${la.toFixed(3)}" transform="translate(${(LX + Math.cos(ang) * R).toFixed(1)} ${(LY + Math.sin(ang) * R).toFixed(1)}) rotate(${(ang * 57.296 + 90).toFixed(1)})"/>`);
      }
      tag('close', 330, 430, C.loop, till(g('close') - 1.2), 28);
    }

    if (is('b10')) {
      head('nowhere', C.fail, till(g('second') - 0.2, g('summit') - 0.5)); head('where', C.mind, till(g('where') - 0.3, g('eye') - 0.6)); head('higher', C.fail, till(g('higher') - 1.0));
      // the mark for you are here: an empty green ring that finds no place on the chart
      const stops = [[REG[0][0], REG[0][1] - 62], [REG[2][0], REG[2][1] - 66], [REG[4][0], REG[4][1] - 62], [REG[1][0], REG[1][1] + 58], [REG[3][0], REG[3][1] + 60]], w0 = g('where') - 0.2, w1 = g('outside') - 0.4;
      const k = Math.min(stops.length - 1.001, Math.max(0, (t - w0) / ((w1 - w0) / (stops.length - 1)))), i = Math.floor(k), f = k - i, e = f * f * (3 - 2 * f), out = U(w1, 0.9);
      const rx = lerp(lerp(stops[i][0], stops[i + 1][0], e), 1436, out), ry = lerp(lerp(stops[i][1], stops[i + 1][1], e), 200, out), ra = till(w0 - 0.2);
      // a further sheet, one level above, that is not there
      const pa = till(g('outside') - 0.4), pp = U(g('outside') - 0.4, 1.0);
      if (pa > 0) pen.raw(`<path d="M${CH.x + 70} ${CH.y - 6}v-18h${CH.w}v${CH.h}h-58" pathLength="1" fill="none" stroke="${C.fail}" stroke-width="4" stroke-dasharray="0.012 0.008" opacity="${(pa * pp).toFixed(3)}"/>`);
      pen.ring(rx, ry, 20, C.mind, ra, '', 5); pen.dot(rx, ry, 6, C.mind, ra * out);
      tag('outside', 1640, 250, C.fail, till(g('outside') - 0.2, g('eye') - 0.6), 28); tag('nocut', 1640, 310, C.fail, till(g('bound') - 0.2, g('eye') - 0.6), 28);
    }

    if (is('b11')) {
      head('smooth', C.soft, till(g('smooth') - 0.4, g('bench') - 0.8)); tag('clusters', 955, 372, C.ink, till(g('clusters') - 0.3, g('bench') - 0.8), 28); tag('tags', 1250, 196, C.loop, till(g('tags') - 0.3, g('bench') - 0.8), 28);
      head('nobench', C.fail, till(g('bench') - 0.6, g('source') - 0.9)); tag('cost', 960, 800, C.fail, till(g('cost') - 0.4, g('source') - 0.9), 30);
      head('nosource', C.fail, till(g('source') - 0.7));
    }

    if (is('b12')) {
      head('contact', C.mind, till(g('instrument') - 0.2, g('shelter') - 0.7)); head('shelter', C.amber, till(g('shelter') - 0.5, g('pushed') - 0.6));
      tag('weights', 1440, 800, C.ink, till(g('weights') - 0.4, g('physics') - 0.5)); head('asserted', C.mind, till(g('asserted') - 0.6, g('physics') - 1.6));
      const da = till(g('reaches') - 0.9, g('vanishes') - 2.2), dp = U(g('reaches') - 0.9, 1.0);
      pen.line(RX0 - 40, 706, RX1 + 40, 706, C.amber, da, dp, { sw: 3, head: false }); seg(RX0 - 40, 692, RX0 - 40, 720, C.amber, da, 3); seg(RX1 + 40, 692, RX1 + 40, 720, C.amber, da * U(g('reaches'), 0.3), 3);
      tag('reaches', 480, 706, C.amber, till(g('reaches') - 0.6, g('vanishes') - 2.2), 28);
      pen.line(RX1 + 52, RY, 1836, RY, C.mind, till(g('open') - 0.8), U(g('open') - 0.8, 0.8), { sw: 5 }); tag('open', 1640, 400, C.mind, till(g('open') - 0.6, g('vanishes') - 2.2));
      head('claim', C.ink, till(g('vanishes') - 1.8), 40, 'claim');
    }

    // the labels' plates go on last, over every line
    pen.raw(backs.map(([x, y, w, h, a]) => `<rect x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${w.toFixed(1)}" height="${h.toFixed(1)}" rx="6" fill="${BLUE}" opacity="${a.toFixed(3)}"/>`).join(''));
  });

  return { seconds: stage.timeline.seconds, renderAt };
}
