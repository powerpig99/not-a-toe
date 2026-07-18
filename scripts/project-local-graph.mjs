#!/usr/bin/env node
/**
 * Disposable graph projection of project living trackers + local memory map.
 *
 * Temporary ground: docs/local-memory.md (manifest) and the .md files it lists.
 * Graph is disposable — never hand-edit. Regenerate after /sleep.
 *
 * Usage:
 *   node scripts/project-local-graph.mjs
 *   node scripts/project-local-graph.mjs --stdout
 *   node scripts/project-local-graph.mjs --mermaid
 */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(scriptDir, '..');
const args = process.argv.slice(2);
const stdout = args.includes('--stdout');
const wantMermaid = args.includes('--mermaid');

const outJson = path.join(root, 'docs', 'local.graph.json');
const outMmd = path.join(root, 'docs', 'local.graph.mmd');
const manifestPath = path.join(root, 'docs', 'local-memory.md');

const MEMORY_CANDIDATES = [
  path.join(
    process.env.HOME || '',
    '.claude/projects/-Users-jingliang-Projects-not-a-toe/memory/MEMORY.md',
  ),
];

// Fixed tracker map (must match docs/local-memory.md living trackers table)
const TRACKERS = [
  { id: 'posts', rel: 'content/posts/README.md', owns: 'authoring' },
  { id: 'format', rel: 'docs/essay-format.md', owns: 'llm-format' },
  { id: 'export', rel: 'docs/export-for-substack.md', owns: 'substack-export' },
  { id: 'export-stub', rel: 'export/README.md', owns: 'export-pointer' },
  { id: 'covers', rel: 'assets/covers/STYLES.md', owns: 'cover-styles' },
  { id: 'root', rel: 'README.md', owns: 'index' },
  { id: 'local', rel: 'docs/local-memory.md', owns: 'manifest' },
  { id: 'build', rel: 'build.mjs', owns: 'site-build', kind: 'script' },
  { id: 'export-script', rel: 'scripts/export-absolute-md.mjs', owns: 'export-projection', kind: 'script' },
  { id: 'local-graph-script', rel: 'scripts/project-local-graph.mjs', owns: 'local-graph-projection', kind: 'script' },
];

function slug(s) {
  return String(s)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
}

function firstSentence(text, max = 180) {
  const t = text.replace(/\s+/g, ' ').trim();
  const m = t.match(/^(.+?[.!?])(?:\s|$)/);
  const s = (m ? m[1] : t).slice(0, max);
  return s.length < t.length && s.length === max ? `${s}…` : s;
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

function extractHeadings(md) {
  const heads = [];
  for (const line of md.split('\n')) {
    const m = line.match(/^(#{1,3})\s+(.+)$/);
    if (m) heads.push({ level: m[1].length, title: m[2].trim() });
  }
  return heads;
}

function resolveRel(fromFile, href) {
  if (/^https?:\/\//i.test(href) || href.startsWith('mailto:') || href.startsWith('#')) {
    return null;
  }
  const base = path.dirname(fromFile);
  const cleaned = href.split('#')[0];
  if (!cleaned) return null;
  try {
    const abs = path.normalize(path.join(base, cleaned));
    if (!abs.startsWith(root)) return null;
    return path.relative(root, abs);
  } catch {
    return null;
  }
}

function fileHash(p) {
  if (!fs.existsSync(p)) return null;
  return crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex').slice(0, 12);
}

function coverCount() {
  const dir = path.join(root, 'assets', 'covers');
  if (!fs.existsSync(dir)) return 0;
  return fs.readdirSync(dir).filter((f) => /\.(jpe?g|png|webp)$/i.test(f)).length;
}

function postCount() {
  const dir = path.join(root, 'content', 'posts');
  if (!fs.existsSync(dir)) return 0;
  return fs.readdirSync(dir).filter((f) => f.endsWith('.md') && f !== 'README.md').length;
}

function build() {
  const nodes = new Map();
  const edges = [];
  const missing = [];

  function addNode(n) {
    if (!nodes.has(n.id)) nodes.set(n.id, n);
    return n.id;
  }

  function edge(from, to, rel, meta = {}) {
    if (!from || !to || from === to) return;
    edges.push({ from, to, rel, ...meta });
  }

  addNode({
    id: 'project:not-a-toe',
    kind: 'project',
    name: 'not-a-toe',
    summary: 'Vanilla JS static site for Not a ToE essays.',
    layer: 'root',
  });

  // Trackers
  for (const t of TRACKERS) {
    const abs = path.join(root, t.rel);
    const exists = fs.existsSync(abs);
    if (!exists) missing.push(t.rel);
    const md = exists && t.rel.endsWith('.md') ? fs.readFileSync(abs, 'utf8') : '';
    const id = `tracker:${t.id}`;
    addNode({
      id,
      kind: t.kind || 'tracker',
      name: t.id,
      path: t.rel,
      owns: t.owns,
      exists,
      hash: fileHash(abs),
      summary: md ? firstSentence(md.replace(/^#[^\n]*\n+/, '')) : exists ? 'binary/script' : 'missing',
      headings: md ? extractHeadings(md).map((h) => h.title).slice(0, 12) : [],
      layer: 'tracker',
    });
    edge('project:not-a-toe', id, 'has_tracker');
    if (t.owns) {
      addNode({
        id: `domain:${t.owns}`,
        kind: 'domain',
        name: t.owns,
        layer: 'domain',
      });
      edge(id, `domain:${t.owns}`, 'owns');
    }

    if (md) {
      for (const link of extractMdLinks(md)) {
        const rel = resolveRel(abs, link.href);
        if (!rel) continue;
        // link to another tracker?
        const target = TRACKERS.find((x) => x.rel === rel || rel.startsWith(x.rel.replace(/\.md$/, '')));
        if (target) {
          edge(id, `tracker:${target.id}`, 'points_to', { label: link.text });
        } else if (rel.endsWith('.md') || rel.endsWith('.mjs')) {
          const nid = `file:${slug(rel)}`;
          addNode({
            id: nid,
            kind: 'file_ref',
            name: path.basename(rel),
            path: rel,
            layer: 'ref',
          });
          edge(id, nid, 'points_to', { label: link.text });
        }
      }
    }
  }

  // MEMORY outside repo
  let memoryPath = null;
  for (const p of MEMORY_CANDIDATES) {
    if (p && fs.existsSync(p)) {
      memoryPath = p;
      break;
    }
  }
  if (memoryPath) {
    const md = fs.readFileSync(memoryPath, 'utf8');
    const mid = 'memory:project';
    addNode({
      id: mid,
      kind: 'memory',
      name: 'MEMORY.md',
      path: memoryPath.replace(process.env.HOME || '', '~'),
      hash: fileHash(memoryPath),
      summary: firstSentence(md.replace(/^#[^\n]*\n+/, '')),
      headings: extractHeadings(md).map((h) => h.title),
      layer: 'memory',
    });
    edge('project:not-a-toe', mid, 'has_memory');
    // MEMORY should point to trackers when it mentions them
    for (const t of TRACKERS) {
      if (md.includes(t.rel) || md.includes(path.basename(t.rel))) {
        edge(mid, `tracker:${t.id}`, 'points_to', { implicit: true });
      }
    }
  } else {
    missing.push('MEMORY.md (claude project memory)');
  }

  // World residue counts (not nodes of essays — summary only)
  const stats = {
    posts: postCount(),
    covers: coverCount(),
    trackers_listed: TRACKERS.length,
    trackers_present: TRACKERS.filter((t) => fs.existsSync(path.join(root, t.rel))).length,
  };

  // Hot: trackers with many outbound points_to (hubs)
  const outbound = {};
  for (const e of edges) {
    if (e.rel === 'points_to') outbound[e.from] = (outbound[e.from] || 0) + 1;
  }
  const hubs = Object.entries(outbound)
    .map(([id, count]) => ({ id, name: nodes.get(id)?.name || id, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 12);

  const byKind = {};
  for (const n of nodes.values()) {
    byKind[n.kind] = (byKind[n.kind] || 0) + 1;
  }

  const sources = {};
  for (const t of TRACKERS) {
    const h = fileHash(path.join(root, t.rel));
    if (h) sources[t.rel] = h;
  }
  if (memoryPath) sources['MEMORY.md'] = fileHash(memoryPath);

  return {
    meta: {
      projection: 'disposable',
      not_source_of_truth: true,
      regenerate: 'node scripts/project-local-graph.mjs',
      generated_at: new Date().toISOString(),
      project: 'not-a-toe',
      manifest: 'docs/local-memory.md',
      sources,
      stats,
      counts: {
        nodes: nodes.size,
        edges: edges.length,
        missing: missing.length,
        by_kind: byKind,
      },
      missing,
    },
    hubs,
    nodes: [...nodes.values()].sort((a, b) => a.id.localeCompare(b.id)),
    edges,
  };
}

function toMermaid(graph) {
  const live = graph.nodes.filter(
    (n) => n.layer === 'tracker' || n.layer === 'memory' || n.layer === 'root' || n.layer === 'domain',
  );
  const liveIds = new Set(live.map((n) => n.id));
  const liveEdges = graph.edges.filter(
    (e) => liveIds.has(e.from) && liveIds.has(e.to) && ['has_tracker', 'has_memory', 'owns', 'points_to'].includes(e.rel),
  );
  const lines = [
    '%% Disposable local-memory projection — regenerate; do not edit',
    'flowchart LR',
    '  classDef tracker fill:#1a1a2e,color:#eee,stroke:#e94560',
    '  classDef memory fill:#16213e,color:#eee,stroke:#0f3460',
    '  classDef domain fill:#0f3460,color:#eee,stroke:#533483',
    '  classDef root fill:#e94560,color:#fff,stroke:#fff',
  ];
  for (const n of live) {
    const label = (n.name || n.id).replace(/"/g, "'").slice(0, 36);
    const safe = n.id.replace(/[^a-zA-Z0-9_]/g, '_');
    lines.push(`  ${safe}["${label}"]`);
    if (n.kind === 'project') lines.push(`  class ${safe} root`);
    else if (n.kind === 'memory') lines.push(`  class ${safe} memory`);
    else if (n.kind === 'domain') lines.push(`  class ${safe} domain`);
    else lines.push(`  class ${safe} tracker`);
  }
  for (const e of liveEdges) {
    const a = e.from.replace(/[^a-zA-Z0-9_]/g, '_');
    const b = e.to.replace(/[^a-zA-Z0-9_]/g, '_');
    const arrow = e.rel === 'owns' ? '-->|owns|' : '-->';
    lines.push(`  ${a} ${arrow} ${b}`);
  }
  return `${lines.join('\n')}\n`;
}

const graph = build();
const json = `${JSON.stringify(graph, null, 2)}\n`;

if (stdout) {
  process.stdout.write(json);
} else {
  fs.mkdirSync(path.dirname(outJson), { recursive: true });
  fs.writeFileSync(outJson, json);
  console.log(`Wrote ${path.relative(root, outJson)}`);
  console.log(
    `  nodes=${graph.meta.counts.nodes} edges=${graph.meta.counts.edges} missing=${graph.meta.counts.missing}`,
  );
  console.log(`  posts=${graph.meta.stats.posts} covers=${graph.meta.stats.covers}`);
  if (graph.meta.missing.length) {
    console.log('  missing:');
    for (const m of graph.meta.missing) console.log(`    ${m}`);
  }
  console.log('  hubs:');
  for (const h of graph.hubs.slice(0, 6)) console.log(`    ${h.count}\t${h.name}`);
  if (wantMermaid) {
    fs.writeFileSync(outMmd, toMermaid(graph));
    console.log(`Wrote ${path.relative(root, outMmd)}`);
  }
  console.log('Projection only — regenerate after /sleep. Trackers are temporary ground.');
}
