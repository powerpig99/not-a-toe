#!/usr/bin/env node
/**
 * Disposable graph projection of essay cross-links under content/posts/.
 *
 * Source of truth for relations: relative markdown links in essay prose
 *   [text](../other-slug/)
 * Graph is disposable — never hand-edit. Regenerate after /sleep or link edits.
 *
 * Usage:
 *   node scripts/project-posts-graph.mjs
 *   node scripts/project-posts-graph.mjs --stdout
 *   node scripts/project-posts-graph.mjs --mermaid
 *   node scripts/project-posts-graph.mjs --neighbors <slug>
 *   node scripts/project-posts-graph.mjs --diff   # compare hashes to existing docs/posts.graph.json
 */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(scriptDir, '..');
const postsDir = path.join(root, 'content', 'posts');
const args = process.argv.slice(2);
const stdout = args.includes('--stdout');
const wantMermaid = args.includes('--mermaid');
const wantDiff = args.includes('--diff');
const neighborsIdx = args.indexOf('--neighbors');
const neighborsSlug = neighborsIdx >= 0 ? args[neighborsIdx + 1] : null;

const outJson = path.join(root, 'docs', 'posts.graph.json');
const outMmd = path.join(root, 'docs', 'posts.graph.mmd');

function fileHash(p) {
  if (!fs.existsSync(p)) return null;
  return crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex').slice(0, 12);
}

function extractTitle(md) {
  const m = md.match(/^#\s+(.+)$/m);
  return m ? m[1].trim() : null;
}

function extractMdLinks(md) {
  const links = [];
  const re = /\[([^\]]+)\]\(([^)]+)\)/g;
  let m;
  while ((m = re.exec(md))) {
    links.push({ text: m[1], href: m[2].trim() });
  }
  return links;
}

/** Normalize internal post href to slug, or null if not a post-relative link. */
function hrefToSlug(href) {
  if (!href || /^https?:\/\//i.test(href) || href.startsWith('mailto:') || href.startsWith('#')) {
    return null;
  }
  const cleaned = href.split('#')[0].trim();
  // Standard form: ../slug/ or ../slug
  let m = cleaned.match(/^\.\.\/([a-z0-9][a-z0-9-]*)\/?$/i);
  if (m) return m[1].toLowerCase();
  // Alternate: ../slug.md
  m = cleaned.match(/^\.\.\/([a-z0-9][a-z0-9-]*)\.md$/i);
  if (m) return m[1].toLowerCase();
  return null;
}

function listPostFiles() {
  if (!fs.existsSync(postsDir)) return [];
  return fs
    .readdirSync(postsDir)
    .filter((f) => f.endsWith('.md') && f !== 'README.md')
    .map((f) => path.join(postsDir, f))
    .sort();
}

function build() {
  const files = listPostFiles();
  const slugSet = new Set(files.map((f) => path.basename(f, '.md')));
  const nodesBySlug = new Map();
  const edges = [];
  const missing = [];
  const linksOutMap = new Map(); // slug -> unique target slugs in order
  const inCount = new Map();
  const outCount = new Map();

  for (const abs of files) {
    const slug = path.basename(abs, '.md');
    const md = fs.readFileSync(abs, 'utf8');
    const title = extractTitle(md) || slug;
    const hash = fileHash(abs);
    const seen = new Set();
    const linksOut = [];

    for (const link of extractMdLinks(md)) {
      const to = hrefToSlug(link.href);
      if (!to) continue;
      if (to === slug) continue;
      if (!slugSet.has(to)) {
        missing.push({ from: slug, to, label: link.text });
        continue;
      }
      edges.push({ from: slug, to, rel: 'points_to', label: link.text });
      if (!seen.has(to)) {
        seen.add(to);
        linksOut.push(to);
      }
    }

    linksOutMap.set(slug, linksOut);
    outCount.set(slug, linksOut.length);
    if (!inCount.has(slug)) inCount.set(slug, 0);

    nodesBySlug.set(slug, {
      id: `post:${slug}`,
      kind: 'post',
      slug,
      path: path.relative(root, abs),
      title,
      hash,
      in_degree: 0,
      out_degree: linksOut.length,
      links_out: linksOut,
    });
  }

  for (const e of edges) {
    inCount.set(e.to, (inCount.get(e.to) || 0) + 1);
  }
  // in_degree should count unique inbound? Plan used degree from edges; use unique sources for cleaner hubs
  const uniqueIn = new Map();
  for (const e of edges) {
    if (!uniqueIn.has(e.to)) uniqueIn.set(e.to, new Set());
    uniqueIn.get(e.to).add(e.from);
  }

  for (const [slug, node] of nodesBySlug) {
    const inDeg = uniqueIn.get(slug)?.size || 0;
    node.in_degree = inDeg;
    node.out_degree = linksOutMap.get(slug)?.length || 0;
  }

  const edgeKey = (e) => `${e.from}->${e.to}`;
  const uniqueDirected = new Set(edges.map(edgeKey));
  let oneWay = 0;
  for (const key of uniqueDirected) {
    const [from, to] = key.split('->');
    if (!uniqueDirected.has(`${to}->${from}`)) oneWay += 1;
  }

  const orphans = [...nodesBySlug.values()]
    .filter((n) => n.in_degree === 0 && n.out_degree === 0)
    .map((n) => n.slug)
    .sort();

  const hubsIn = [...nodesBySlug.values()]
    .filter((n) => n.in_degree > 0)
    .sort((a, b) => b.in_degree - a.in_degree || a.slug.localeCompare(b.slug))
    .slice(0, 20)
    .map((n) => ({ slug: n.slug, in_degree: n.in_degree }));

  const hubsOut = [...nodesBySlug.values()]
    .filter((n) => n.out_degree > 0)
    .sort((a, b) => b.out_degree - a.out_degree || a.slug.localeCompare(b.slug))
    .slice(0, 20)
    .map((n) => ({ slug: n.slug, out_degree: n.out_degree }));

  const sources = {};
  for (const [slug, node] of nodesBySlug) {
    sources[node.path] = node.hash;
  }

  return {
    meta: {
      projection: 'disposable',
      not_source_of_truth: true,
      regenerate: 'node scripts/project-posts-graph.mjs',
      generated_at: new Date().toISOString(),
      project: 'not-a-toe',
      source_glob: 'content/posts/*.md',
      link_pattern: '](../slug/)',
      sources,
      stats: {
        posts: nodesBySlug.size,
        edges: edges.length,
        unique_directed: uniqueDirected.size,
        missing_targets: missing.length,
        one_way: oneWay,
        isolated: orphans.length,
        posts_with_outbound: [...nodesBySlug.values()].filter((n) => n.out_degree > 0).length,
      },
    },
    hubs_in: hubsIn,
    hubs_out: hubsOut,
    missing,
    orphans,
    nodes: [...nodesBySlug.values()].sort((a, b) => a.slug.localeCompare(b.slug)),
    edges,
  };
}

function neighborsOf(graph, slug) {
  const node = graph.nodes.find((n) => n.slug === slug);
  if (!node) return null;
  const out = node.links_out.slice();
  const inbound = graph.edges
    .filter((e) => e.to === slug)
    .map((e) => e.from);
  const inUnique = [...new Set(inbound)].sort();
  return {
    slug,
    title: node.title,
    out,
    in: inUnique,
    // 1-hop set for sleep review (neighbors only, not the seed)
    review: [...new Set([...out, ...inUnique])].sort(),
  };
}

function loadPrevious() {
  if (!fs.existsSync(outJson)) return null;
  try {
    return JSON.parse(fs.readFileSync(outJson, 'utf8'));
  } catch {
    return null;
  }
}

function diffHashes(prev, next) {
  if (!prev?.nodes) {
    return {
      seeds: next.nodes.map((n) => n.slug),
      note: 'no previous graph; all posts treated as seeds',
    };
  }
  const prevHash = new Map(prev.nodes.map((n) => [n.slug, n.hash]));
  const prevSlugs = new Set(prev.nodes.map((n) => n.slug));
  const nextSlugs = new Set(next.nodes.map((n) => n.slug));
  const added = [];
  const changed = [];
  const removed = [];
  for (const n of next.nodes) {
    if (!prevSlugs.has(n.slug)) added.push(n.slug);
    else if (prevHash.get(n.slug) !== n.hash) changed.push(n.slug);
  }
  for (const s of prevSlugs) {
    if (!nextSlugs.has(s)) removed.push(s);
  }
  return { added, changed, removed, seeds: [...added, ...changed].sort() };
}

function toMermaid(graph, maxNodes = 40) {
  // Live view: top in-degree hubs plus any of their mutual edges
  const hubSlugs = new Set(graph.hubs_in.slice(0, 18).map((h) => h.slug));
  // Include high out-degree that aren't hubs yet
  for (const h of graph.hubs_out.slice(0, 10)) hubSlugs.add(h.slug);
  const nodes = graph.nodes.filter((n) => hubSlugs.has(n.slug)).slice(0, maxNodes);
  const ids = new Set(nodes.map((n) => n.slug));
  const liveEdges = [];
  const seen = new Set();
  for (const e of graph.edges) {
    if (!ids.has(e.from) || !ids.has(e.to)) continue;
    const k = `${e.from}->${e.to}`;
    if (seen.has(k)) continue;
    seen.add(k);
    liveEdges.push(e);
  }
  const lines = [
    '%% Disposable posts lattice — regenerate; do not edit',
    '%% Source of truth: relative cross-links in content/posts/*.md',
    'flowchart LR',
    '  classDef post fill:#1a1a2e,color:#eee,stroke:#e94560',
  ];
  for (const n of nodes) {
    const safe = n.slug.replace(/[^a-zA-Z0-9_]/g, '_');
    const label = (n.title || n.slug).replace(/"/g, "'").slice(0, 32);
    lines.push(`  ${safe}["${label}"]`);
    lines.push(`  class ${safe} post`);
  }
  for (const e of liveEdges) {
    const a = e.from.replace(/[^a-zA-Z0-9_]/g, '_');
    const b = e.to.replace(/[^a-zA-Z0-9_]/g, '_');
    lines.push(`  ${a} --> ${b}`);
  }
  return `${lines.join('\n')}\n`;
}

function printNeighbors(graph, slug) {
  const n = neighborsOf(graph, slug);
  if (!n) {
    console.error(`Unknown slug: ${slug}`);
    process.exitCode = 1;
    return;
  }
  console.log(`# neighbors of ${n.slug}`);
  console.log(`title: ${n.title}`);
  console.log(`out (${n.out.length}):`);
  for (const s of n.out) console.log(`  → ${s}`);
  console.log(`in (${n.in.length}):`);
  for (const s of n.in) console.log(`  ← ${s}`);
  console.log(`review_set (${n.review.length}):`);
  for (const s of n.review) console.log(`  ${s}`);
}

const graph = build();

if (neighborsSlug) {
  printNeighbors(graph, neighborsSlug);
  process.exit(process.exitCode || 0);
}

if (wantDiff) {
  const prev = loadPrevious();
  const d = diffHashes(prev, graph);
  console.log(JSON.stringify(d, null, 2));
  if (d.seeds?.length) {
    console.log('\n# review sets for seeds');
    for (const seed of d.seeds) {
      const n = neighborsOf(graph, seed);
      if (!n) continue;
      console.log(`\nseed: ${seed}`);
      console.log(`  review (${n.review.length}): ${n.review.join(', ') || '(none)'}`);
    }
  }
  process.exit(0);
}

const json = `${JSON.stringify(graph, null, 2)}\n`;

if (stdout) {
  process.stdout.write(json);
} else {
  fs.mkdirSync(path.dirname(outJson), { recursive: true });
  fs.writeFileSync(outJson, json);
  console.log(`Wrote ${path.relative(root, outJson)}`);
  const s = graph.meta.stats;
  console.log(
    `  posts=${s.posts} edges=${s.edges} unique=${s.unique_directed} missing=${s.missing_targets} one_way=${s.one_way} isolated=${s.isolated} with_out=${s.posts_with_outbound}`,
  );
  if (graph.missing.length) {
    console.log('  missing targets:');
    for (const m of graph.missing.slice(0, 20)) {
      console.log(`    ${m.from} → ${m.to}`);
    }
  }
  console.log('  hubs_in:');
  for (const h of graph.hubs_in.slice(0, 8)) {
    console.log(`    ${h.in_degree}\t${h.slug}`);
  }
  if (wantMermaid) {
    fs.writeFileSync(outMmd, toMermaid(graph));
    console.log(`Wrote ${path.relative(root, outMmd)}`);
  }
  console.log('Projection only — regenerate after /sleep or link edits. Prose links are ground.');
}
