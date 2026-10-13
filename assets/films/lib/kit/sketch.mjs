// The stroke kit: line drawing by hand, on the pen of flat.mjs. Every shape is one SVG path whose points carry a
// small wobble drawn from a seed (its `id`, or its own coordinates), so a shape is the same on every frame and in
// every tab, and no two shapes wobble alike. A path is drawn on by arc length: `p` runs 0 to 1, and a shape of
// several strokes draws them one after another.
//
//   hand(pen, { ink }) -> { line, path, box, oval, hatch, arrow, person, cloud, lens, rays }
//   Every shape takes a last argument { p, a, c, w, id }: progress, opacity, colour, width, seed.
//     line(x0, y0, x1, y1)              path(points)             one stroke through the points
//     box(x, y, w, h)                   four strokes that overshoot their corners a little
//     oval(cx, cy, rx, ry, { rot })     one stroke that runs a little past where it began
//     hatch(x, y, w, h, { gap })        pencil shading: parallel strokes at 45 degrees inside the box
//     arrow(x0, y0, x1, y1)             a stroke and its head
//     person(x, y, { s, dir, arm })     an anonymous figure standing on (x, y): head, body, legs, one arm raised
//                                       `arm` degrees above level toward `dir`. Returns where that hand is.
//     cloud(cx, cy, rx, ry, { tail })   a thought: a scalloped outline, and small rings toward `tail` [x, y]
//     lens(x, y, r)                     a magnifying glass      rays(x, y, r)   a small mark that shines
import { rng } from './rng.mjs';

const f = (n) => n.toFixed(1);
const through = (pts) => {
  if (pts.length < 3) return `M${f(pts[0][0])} ${f(pts[0][1])}L${f(pts.at(-1)[0])} ${f(pts.at(-1)[1])}`;
  let d = `M${f(pts[0][0])} ${f(pts[0][1])}`;
  for (let i = 1; i < pts.length - 1; i++) d += `Q${f(pts[i][0])} ${f(pts[i][1])} ${f((pts[i][0] + pts[i + 1][0]) / 2)} ${f((pts[i][1] + pts[i + 1][1]) / 2)}`;
  return `${d}L${f(pts.at(-1)[0])} ${f(pts.at(-1)[1])}`;
};
// One straight stroke as the hand makes it: a slight bow, and a tremor along it.
const stroke = (x0, y0, x1, y1, r, amp = 2) => {
  const len = Math.hypot(x1 - x0, y1 - y0) || 1, n = Math.max(2, Math.ceil(len / 48)), nx = -(y1 - y0) / len, ny = (x1 - x0) / len, bow = (r() - 0.5) * len * 0.025;
  return Array.from({ length: n + 1 }, (_, i) => {
    const u = i / n, k = bow * Math.sin(Math.PI * u) + amp * (r() - 0.5) * 2 * (i && i < n ? 1 : 0.4);
    return [x0 + (x1 - x0) * u + nx * k, y0 + (y1 - y0) * u + ny * k];
  });
};

export function hand(pen, { ink }) {
  const put = (d, { p = 1, a = 1, c = ink, w = 4 } = {}) => {
    if (a <= 0 || p <= 0) return;
    pen.raw(`<path d="${d}" fill="none" stroke="${c}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round" opacity="${a}"${p < 1 ? ` pathLength="1" stroke-dasharray="${p.toFixed(4)} 1"` : ''}/>`);
  };
  const seed = (o, ...key) => rng(o?.id ?? key.join(','));
  const line = (x0, y0, x1, y1, o) => put(through(stroke(x0, y0, x1, y1, seed(o, 'l', x0, y0, x1, y1))), o);
  const path = (pts, o) => {
    const r = seed(o, 'p', pts[0], pts.length);
    put(through(pts.map(([x, y]) => [x + (r() - 0.5) * 4, y + (r() - 0.5) * 4])), o);
  };
  const edges = (x, y, w, h, r) => [[x - 5, y, x + w + 5, y], [x + w, y - 5, x + w, y + h + 5], [x + w + 5, y + h, x - 5, y + h], [x, y + h + 5, x, y - 5]].map(([a, b, c2, d]) => through(stroke(a, b, c2, d, r))).join('');
  const box = (x, y, w, h, o) => put(edges(x, y, w, h, seed(o, 'b', x, y, w, h)), o);
  const ring = (cx, cy, rx, ry, r, rot = 0, turn = 1.05) => {
    const a0 = r() * 6.28, cos = Math.cos(rot), sin = Math.sin(rot), n = Math.max(14, Math.round((rx + ry) / 5));
    return through(Array.from({ length: n + 1 }, (_, i) => {
      const a = a0 + turn * 2 * Math.PI * i / n, k = 1 + (r() - 0.5) * 0.05, x = rx * k * Math.cos(a), y = ry * k * Math.sin(a);
      return [cx + x * cos - y * sin, cy + x * sin + y * cos];
    }));
  };
  const oval = (cx, cy, rx, ry = rx, o) => put(ring(cx, cy, rx, ry, seed(o, 'o', cx, cy, rx, ry), o?.rot), o);
  const hatch = (x, y, w, h, o) => {
    const r = seed(o, 'h', x, y, w, h), gap = o?.gap ?? 13;
    let d = '';
    for (let k = gap / 2 - h; k < w; k += gap) {
      const a = Math.max(0, k), b = Math.min(w, k + h);
      if (b - a > 4) d += through(stroke(x + a, y + h - (a - k), x + b, y + h - (b - k), r, 1.3));
    }
    put(d, { w: 2.5, ...o });
  };
  const arrow = (x0, y0, x1, y1, o) => {
    const r = seed(o, 'a', x0, y0, x1, y1), ang = Math.atan2(y1 - y0, x1 - x0), tip = (da) => [x1 - 24 * Math.cos(ang + da), y1 - 24 * Math.sin(ang + da)];
    put(through(stroke(x0, y0, x1, y1, r)) + through(stroke(...tip(0.45), x1, y1, r, 0.8)) + through(stroke(...tip(-0.45), x1, y1, r, 0.8)), o);
  };
  const person = (x, y, o = {}) => {
    const { s = 1, dir = 1, arm = -60 } = o, r = seed(o, 'm', x, y, dir), ang = arm * Math.PI / 180;
    const hx = x + dir * 64 * s * Math.cos(ang), hy = y - 118 * s - 64 * s * Math.sin(ang);
    put(ring(x, y - 158 * s, 24 * s, 24 * s, r) + through(stroke(x, y - 134 * s, x, y - 62 * s, r)) + through(stroke(x, y - 62 * s, x - 22 * s, y, r)) + through(stroke(x, y - 62 * s, x + 22 * s, y, r))
      + through(stroke(x, y - 118 * s, hx, hy, r)) + through(stroke(x, y - 118 * s, x - dir * 20 * s, y - 62 * s, r)), o);
    return [hx, hy];
  };
  const cloud = (cx, cy, rx, ry, o = {}) => {
    const r = seed(o, 'c', cx, cy, rx, ry), n = Math.max(9, Math.round((rx + ry) / 22));
    let d = '';
    for (let i = 0; i < n; i++) {
      const a = 2 * Math.PI * i / n, b = 2 * Math.PI * (i + 1) / n, m = (a + b) / 2, out = 1.16 + r() * 0.08;
      d += `${i ? 'L' : 'M'}${f(cx + rx * Math.cos(a))} ${f(cy + ry * Math.sin(a))}Q${f(cx + rx * out * Math.cos(m))} ${f(cy + ry * out * Math.sin(m))} ${f(cx + rx * Math.cos(b))} ${f(cy + ry * Math.sin(b))}`;
    }
    if (o.tail) [0.3, 0.55, 0.78].forEach((u, i) => { d += ring(cx + (o.tail[0] - cx) * u, cy + ry + (o.tail[1] - cy - ry) * u, 15 - i * 4, 12 - i * 3, r); });
    put(d, o);
  };
  const lens = (x, y, rad, o) => {
    const r = seed(o, 'g', x, y, rad);
    put(ring(x, y, rad, rad, r) + through(stroke(x + rad * 0.72, y + rad * 0.72, x + rad * 1.9, y + rad * 1.9, r)), o);
  };
  const rays = (x, y, rad, o) => {
    const r = seed(o, 'r', x, y, rad);
    put(ring(x, y, rad * 0.45, rad * 0.45, r) + Array.from({ length: 8 }, (_, i) => { const a = Math.PI * i / 4 + 0.2; return through(stroke(x + rad * 0.7 * Math.cos(a), y + rad * 0.7 * Math.sin(a), x + rad * 1.15 * Math.cos(a), y + rad * 1.15 * Math.sin(a), r, 0.6)); }).join(''), o);
  };
  return { line, path, box, oval, hatch, arrow, person, cloud, lens, rays };
}
