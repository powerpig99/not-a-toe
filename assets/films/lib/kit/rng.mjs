// Seeded randomness for procedural geometry. A film never calls Math.random: every draw comes from a seed,
// so a world is rebuilt identically in every tab and on every run. Runs in Node and in the page.
//
//   rng(seed)     () => number in [0, 1). seed is an integer or a name; give each use its own name, so that a
//                 draw added in one place does not shift every draw after it.
//   noise3(seed)  (x, y, z) => simplex noise, about -1 to 1
//   fbm(seed, { octaves, lacunarity, gain })
//                 (x, y, z) => octaves of noise3 summed and scaled back to about -1 to 1
import { SimplexNoise } from 'three/addons/math/SimplexNoise.js';

// FNV-1a
const hash = (name) => {
  let h = 2166136261;
  for (const c of String(name)) h = Math.imul(h ^ c.codePointAt(0), 16777619);
  return h >>> 0;
};

// mulberry32
export const rng = (seed) => {
  let a = typeof seed === 'number' ? seed : hash(seed);
  return () => {
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
};

export const noise3 = (seed) => {
  const simplex = new SimplexNoise({ random: rng(seed) });
  return (x, y, z) => simplex.noise3d(x, y, z);
};

export const fbm = (seed, { octaves = 5, lacunarity = 2, gain = 0.5 } = {}) => {
  const noise = noise3(seed);
  let total = 0;
  for (let o = 0, amp = 1; o < octaves; o++, amp *= gain) total += amp;
  return (x, y, z) => {
    let sum = 0;
    for (let o = 0, amp = 1, f = 1; o < octaves; o++, amp *= gain, f *= lacunarity) sum += amp * noise(x * f, y * f, z * f);
    return sum / total;
  };
};
