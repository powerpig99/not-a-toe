// Time and camera. Every value here is a pure function of t, so a frame can be drawn alone and out of order.
// Runs in Node and in the page: a film that keeps its camera in a module of its own can be measured without a browser.
//
// Easing and time
//   bezier([x1, y1, x2, y2])        CSS cubic-bezier as (x) => y
//   curves(contract)                { ease, glide }: motion.easing for elements that come up on screen,
//                                   motion.camera_easing for camera moves (it starts and ends at rest)
//   span(t, t0, t1)                 progress of t through [t0, t1): 0 before, 1 after. t1 > t0.
//   between(t, t0, t1, fade, ease)  1 inside [t0, t1], eased up over `fade` from t0 and down over `fade` to t1.
//                                   t1 may be Infinity.
//   cues(timeline)                  (beat, name) => seconds; the beat's start when no name is given. A cue the
//                                   timeline does not hold throws: a NaN time would draw nothing and say nothing.
//
// Camera. A pose is { position, target, up }. A path is (u, pose, t) => pose for u in [0, 1].
//   pose(position, target, up)      plain arrays in, Vector3s out; up defaults to +Y
//   rail(points, targets, up)       Catmull-Rom through `points` at even speed. The look-at point runs through
//                                   `targets` in step with the knots: one target holds it still, as many as
//                                   there are points gives each knot its own.
//   scaleMove(a, b)                 pose a to pose b for moves across scales. The LOG of the distance to the
//                                   target moves evenly, so equal ratios of distance take equal time; the target
//                                   shifts with the distance, so what the move starts on stays in frame while it
//                                   is near and what it ends on is centred as it arrives; the line of sight turns
//                                   at an even rate. With equal distances it is an arc or a track.
//   camera(stage, moves, shots)     (t) => pose. moves: [{ t0, t1, path, ease }] in time order, eased with
//                                   `glide` unless a move brings its own curve. The camera rests on the end of a
//                                   move until the next begins. shots: [{ t0, lock }] in time order, one per
//                                   beat. Under stage.params.lockcam the pose is the one at `lock`, or at the
//                                   shot's t0 when it names none, for the whole shot.
//   aim(camera, pose)               writes a pose into a three camera
//   peakTurn(cam, t0, t1, fps)      largest orbit rate in degrees per second, frame to frame, over [t0, t1]:
//                                   the number contract motion.max_orbit_deg_per_s bounds
import { CatmullRomCurve3, MathUtils, Vector3 } from 'three';

export const bezier = ([x1, y1, x2, y2]) => (x) => {
  if (x <= 0 || x >= 1) return Math.min(1, Math.max(0, x)); // the ends are exact: a move lands on its pose, a fade on 1
  const at = (a, b, u) => 3 * a * u * (1 - u) ** 2 + 3 * b * u * u * (1 - u) + u ** 3;
  let lo = 0, hi = 1, u = x;
  for (let i = 0; i < 40; i++) {
    u = (lo + hi) / 2;
    if (at(x1, x2, u) < x) lo = u; else hi = u;
  }
  return at(y1, y2, u);
};

export const curves = ({ motion }) => ({ ease: bezier(motion.easing), glide: bezier(motion.camera_easing) });

export const span = (t, t0, t1) => Math.min(1, Math.max(0, (t - t0) / (t1 - t0)));

export const between = (t, t0, t1, fade, ease) => ease(span(t, t0, t0 + fade)) * (1 - ease(span(t, t1 - fade, t1)));

export const cues = (timeline) => (beat, name) => {
  const b = timeline.beats.find(({ id }) => id === beat);
  const t = name === undefined ? b?.t0 : b?.cues[name];
  if (t === undefined) throw new Error(`timeline has no cue ${beat} ${name ?? ''}`);
  return t;
};

export const pose = (position = [0, 0, 0], target = [0, 0, 0], up = [0, 1, 0]) =>
  ({ position: new Vector3(...position), target: new Vector3(...target), up: new Vector3(...up) });

export const rail = (points, targets, up = [0, 1, 0]) => {
  const curve = (list) => new CatmullRomCurve3(list.map((p) => new Vector3(...p)), false, 'centripetal');
  const path = curve(points);
  const look = targets.length > 1 ? curve(targets) : null;
  return (u, out) => {
    const k = path.getUtoTmapping(u);
    path.getPoint(k, out.position);
    if (look) look.getPoint(k, out.target); else out.target.set(...targets[0]);
    out.up.set(...up);
    return out;
  };
};

export const scaleMove = (a, b) => {
  const da = a.position.distanceTo(a.target), db = b.position.distanceTo(b.target);
  const ra = a.position.clone().sub(a.target).normalize(), rb = b.position.clone().sub(b.target).normalize();
  const angle = ra.angleTo(rb), sin = Math.sin(angle);
  const dir = new Vector3(), other = new Vector3();
  // The share of the way the target has gone is the share of the distance covered, taken from the same exponent
  // as the distance: it is even in u when the two distances are equal, and nearly so when they are nearly equal.
  const k = Math.log(db / da), whole = Math.expm1(k);
  return (u, out) => {
    const d = da * Math.exp(k * u);
    const w = whole ? Math.expm1(k * u) / whole : u;
    if (sin < 1e-9) dir.copy(ra);
    else dir.copy(ra).multiplyScalar(Math.sin((1 - u) * angle) / sin).add(other.copy(rb).multiplyScalar(Math.sin(u * angle) / sin));
    out.target.lerpVectors(a.target, b.target, w);
    out.position.copy(dir).multiplyScalar(d).add(out.target);
    out.up.lerpVectors(a.up, b.up, u).normalize();
    return out;
  };
};

export const camera = ({ params, contract }, moves, shots) => {
  const { glide } = curves(contract);
  const out = pose();
  return (t) => {
    if (params.lockcam) {
      const shot = shots.findLast((s) => s.t0 <= t) ?? shots[0];
      t = shot.lock ?? shot.t0;
    }
    const m = moves[Math.max(0, moves.findLastIndex((move) => move.t0 <= t))];
    return m.path((m.ease ?? glide)(span(t, m.t0, m.t1)), out, t);
  };
};

export const aim = (cam, { position, target, up }) => {
  cam.position.copy(position);
  cam.up.copy(up);
  cam.lookAt(target);
  cam.updateMatrixWorld();
};

export const peakTurn = (cam, t0, t1, fps) => {
  const dir = (t) => {
    const { position, target } = cam(t);
    return position.clone().sub(target).normalize();
  };
  let peak = 0;
  for (let n = Math.round(t0 * fps), before = dir(n / fps); n < Math.round(t1 * fps); n++) {
    const after = dir((n + 1) / fps);
    peak = Math.max(peak, MathUtils.radToDeg(before.angleTo(after)) * fps);
    before = after;
  }
  return peak;
};
