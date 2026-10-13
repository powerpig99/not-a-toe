// Labels: DOM text at constant screen size, pinned every frame to a projected 3D point by a ring and a leader
// line, on a ground scrim. A label never shrinks on a pull-back. This module also owns the two things every
// overlay string answers to: the dump QA scripts read, and the debug painter.
//
//   labels(stage, { depth, clear, until }) -> { add, place, dump }
//     clear     (t) => [[x, y, w, h]], format px: boxes a chip is kept out of at t, by the shortest way that
//               leaves it in the text area (text.mjs held: the frame's own text, which does not move)
//     until     seconds: no label is up after it (the end card's first frame)
//     add({ text, anchor, offset, from, to, role, accent, leader, occlude, size })
//         Call it while the film is built: the chip is measured once, there and then.
//         anchor    a Vector3 in world space, read every frame: move it and the label follows
//         offset    [dx, dy] px from the anchor to the nearest corner or edge of the text chip. The chip is
//                   then held inside the safe margins and above the caption band, and the leader runs from the
//                   ring to the nearest point of the chip.
//         from, to  seconds; eased up and down with motion.easing
//         role      'label' (ring, leader, ink) or 'note' (muted, no ring or leader unless leader is set)
//         accent    ring colour: a palette.semantic hex that says what the thing is. Default palette.ink.
//         occlude   world units. When given, the label is hidden while the scene is nearer the camera than the
//                   anchor by more than this, at the anchor's pixel (use the size of the thing the anchor sits
//                   in). Needs `depth`, which is post.mjs depthAt.
//     place(camera, t)   call once per frame, after the scene is drawn and after every other overlay module
//                   has shown its text. A label is hidden while its anchor is behind the camera. An anchor
//                   outside the frame keeps its label: the chip stays in the safe box and the leader runs off.
//     dump()        every text box on screen, from every overlay module: [{ text, role, px, rect: [x, y, w, h],
//                   color, opacity, flags }] in format px. Also window.__texts(), which is how a QA script
//                   reaches it from outside the page. A box is the text itself, without the padding of its scrim.
//                   Hiding stage.overlay (visibility) hides every string and leaves no box.
//
//   audit(boxes, stage) -> one list per box of what it breaks: 'floor' (font under its role's floor in
//     contract type.floors_px), 'margin' (outside safe.margin_pct), 'band' (a non-caption in the bottom
//     safe.caption_band_pct), 'overlap' (shares pixels with another text box). Pure: runs in Node on a dump.
//
// With stage.params.debug the safe box and the top of the caption band are drawn in cyan and every box that
// breaks a rule is framed in pure magenta (255, 0, 255) with the rules it breaks, so a clean debug still holds
// no pure magenta pixel.
import { Vector3 } from 'three';
import { between, curves } from './rails.mjs';
import { area, el, floor, font, scrim } from './text.mjs';

const FADE = 0.4;
const RING = 8;
const PAD = [5, 12];
const HAN = /\p{Script=Han}/u;
const SVG = 'http://www.w3.org/2000/svg';

export const audit = (boxes, { width, height, contract }) => {
  const { x0, y0, x1, y1 } = area({ width, height, contract });
  const hit = ([ax, ay, aw, ah], [bx, by, bw, bh]) => Math.min(ax + aw, bx + bw) - Math.max(ax, bx) > 0.5 && Math.min(ay + ah, by + bh) - Math.max(ay, by) > 0.5;
  return boxes.map(({ text, role, px, rect: [x, y, w, h] }, i) => [
    px < floor(contract, role, HAN.test(text)) && 'floor',
    (x < x0 - 0.5 || y < y0 - 0.5 || x + w > x1 + 0.5 || y + h > height - y0 + 0.5) && 'margin',
    role !== 'caption' && y + h > y1 + 0.5 && 'band',
    boxes.some((other, j) => j !== i && hit(other.rect, [x, y, w, h])) && 'overlap',
  ].filter(Boolean));
};

const GAP = 14; // px a chip stands off a box it is kept out of
export function labels(stage, { depth, clear, until = Infinity } = {}) {
  const { overlay, width, height, params, contract } = stage;
  const { palette } = contract;
  const { ease } = curves(contract);
  const box = area(stage);
  const items = [];
  const v = new Vector3();

  const draw = (tag, attrs, parent) => {
    const node = document.createElementNS(SVG, tag);
    for (const [k, value] of Object.entries(attrs)) node.setAttribute(k, value);
    parent.append(node);
    return node;
  };
  const lines = draw('svg', { width, height, style: 'position:absolute;left:0;top:0' }, overlay);
  // Format px per CSS px of layout: the stage is scaled to the viewport, and rects come back in viewport px.
  const zoom = () => width / overlay.getBoundingClientRect().width;

  const add = ({ text, anchor, offset, from, to = Infinity, role = 'label', accent = palette.ink, leader = role === 'label', occlude, size }) => {
    const mark = leader && draw('g', {}, lines);
    const chip = el(overlay, `position:absolute;left:0;top:0;white-space:nowrap;padding:${PAD[0]}px ${PAD[1]}px;background:${scrim(stage, role === 'note' ? 0.9 : 0.8)}`);
    const words = el(chip, `display:inline-block;${font(stage, role, size)}`, text);
    words.dataset.role = role;
    const { width: w, height: h } = chip.getBoundingClientRect(), k = zoom();
    items.push({
      anchor, offset, from, to, occlude, chip, mark, w: w * k, h: h * k,
      // A dark line under the light one keeps the leader readable over a bright surface.
      under: mark && draw('path', { fill: 'none', stroke: palette.ground, 'stroke-opacity': 0.6, 'stroke-width': 5, 'stroke-linecap': 'round' }, mark),
      line: mark && draw('path', { fill: 'none', stroke: palette.ink, 'stroke-width': 2 }, mark),
      ring: mark && draw('circle', { r: RING, fill: 'none', stroke: accent, 'stroke-width': 2.5 }, mark),
    });
  };

  const dump = () => {
    const k = zoom();
    const boxes = [...overlay.querySelectorAll('[data-role]')].flatMap((node) => {
      const style = getComputedStyle(node);
      let opacity = 1;
      for (let n = node; n !== overlay; n = n.parentElement) opacity *= getComputedStyle(n).opacity;
      const r = node.getBoundingClientRect();
      if (style.visibility === 'hidden' || !opacity || !r.width) return [];
      return [{ text: node.innerText, role: node.dataset.role, px: parseFloat(style.fontSize), rect: [r.x * k, r.y * k, r.width * k, r.height * k], color: style.color, opacity }];
    });
    const flags = audit(boxes, stage);
    return boxes.map((b, i) => ({ ...b, flags: flags[i] }));
  };
  window.__texts = dump;

  const paint = params.debug && (() => {
    const layer = el(overlay, 'position:absolute;inset:0');
    const guide = `position:absolute;box-sizing:border-box;border:2px solid #00ffff`;
    return () => {
      overlay.append(layer); // on top of whatever was added since
      layer.replaceChildren();
      el(layer, `${guide};left:${box.x0}px;top:${box.y0}px;width:${box.x1 - box.x0}px;height:${height - 2 * box.y0}px`);
      el(layer, `${guide};border-width:2px 0 0;left:0;top:${box.y1}px;width:${width}px;height:0`);
      for (const { rect: [x, y, w, h], flags } of dump()) {
        if (!flags.length) continue;
        const frame = el(layer, `position:absolute;box-sizing:border-box;border:6px solid #ff00ff;left:${Math.round(x) - 8}px;top:${Math.round(y) - 8}px;width:${Math.round(w) + 16}px;height:${Math.round(h) + 16}px`);
        el(frame, `position:absolute;left:-6px;bottom:100%;padding:2px 8px;background:#ff00ff;white-space:nowrap;font:20px ${contract.type.mono};color:#000`, flags.join(' '));
      }
    };
  })();

  const place = (camera, t) => {
    for (const it of items) {
      v.copy(it.anchor).applyMatrix4(camera.matrixWorldInverse);
      it.z = -v.z;
      v.applyMatrix4(camera.projectionMatrix);
      it.x = (v.x + 1) / 2 * width;
      it.y = (1 - v.y) / 2 * height;
      it.a = it.z > camera.near ? between(t, it.from, Math.min(it.to, until), FADE, ease) : 0;
    }
    const kept = clear ? clear(t) : [];
    const asked = items.filter((it) => it.a && it.occlude !== undefined);
    if (asked.length) {
      const scene = depth(asked.map((it) => [it.x / width, 1 - it.y / height]));
      asked.forEach((it, i) => {
        if (scene[i] < it.z - it.occlude) it.a = 0;
      });
    }
    for (const { a, x, y, offset: [dx, dy], w, h, chip, mark, under, line, ring } of items) {
      chip.style.visibility = a ? '' : 'hidden';
      if (mark) mark.style.visibility = a ? '' : 'hidden';
      if (!a) continue;
      // The chip hangs off the offset point by its nearest corner or edge, then is held inside the text area.
      let left = Math.min(box.x1 - w, Math.max(box.x0, x + dx - (dx < 0 ? w : dx > 0 ? 0 : w / 2)));
      let top = Math.min(box.y1 - h, Math.max(box.y0, y + dy - (dy < 0 ? h : dy > 0 ? 0 : h / 2)));
      for (const [kx, ky, kw, kh] of kept) {
        if (left + w <= kx - GAP || left >= kx + kw + GAP || top + h <= ky - GAP || top >= ky + kh + GAP) continue;
        // The four ways out of the box, nearest first; the first that leaves the chip in the text area is taken.
        const ways = [[kx - GAP - w, top], [kx + kw + GAP, top], [left, ky - GAP - h], [left, ky + kh + GAP]]
          .filter(([l, u]) => l >= box.x0 && l + w <= box.x1 && u >= box.y0 && u + h <= box.y1)
          .sort((a, b) => Math.hypot(a[0] - left, a[1] - top) - Math.hypot(b[0] - left, b[1] - top));
        if (ways.length) [left, top] = ways[0];
      }
      chip.style.opacity = a;
      chip.style.transform = `translate(${left}px,${top}px)`;
      if (!mark) continue;
      const qx = Math.min(left + w, Math.max(left, x)), qy = Math.min(top + h, Math.max(top, y));
      const reach = Math.hypot(qx - x, qy - y);
      const d = reach > RING ? `M${x + (qx - x) * RING / reach} ${y + (qy - y) * RING / reach}L${qx} ${qy}` : '';
      mark.setAttribute('opacity', a);
      under.setAttribute('d', d);
      line.setAttribute('d', d);
      ring.setAttribute('cx', x);
      ring.setAttribute('cy', y);
    }
    if (paint) paint();
  };

  return { add, place, dump };
}
