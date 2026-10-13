// The three names of three.js that the kit's modules import. A flat film draws in the overlay and never calls
// them; they exist so that the modules load without three.js. A film that needs a camera or a curve needs three.
const no = (name) => () => { throw new Error(`three-lite: ${name} is not available in a live flat film`); };
export class Vector3 {
  constructor(x = 0, y = 0, z = 0) { this.x = x; this.y = y; this.z = z; }
  set(x, y, z) { this.x = x; this.y = y; this.z = z; return this; }
  copy(v) { return this.set(v.x, v.y, v.z); }
  clone() { return new Vector3(this.x, this.y, this.z); }
  project() { return no('Vector3.project')(); }
}
export class CatmullRomCurve3 { constructor() { no('CatmullRomCurve3')(); } }
export const MathUtils = {
  clamp: (x, a, b) => Math.min(b, Math.max(a, x)),
  lerp: (a, b, t) => a + (b - a) * t,
  smoothstep: (x, a, b) => { const t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); },
  degToRad: (d) => d * Math.PI / 180,
};
