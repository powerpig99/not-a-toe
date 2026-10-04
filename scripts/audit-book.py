#!/usr/bin/env python3
"""
Audit the live book (content/book/*.md) against the essay corpus.

Structure lives only as relative links in content/book/*.md; this audit verifies
that the links form a complete, single-placement reading of the corpus and that
the authored book prose obeys the same invariants as essays.

Usage:
  python3 scripts/audit-book.py              # full audit
  python3 scripts/audit-book.py --slug <s>   # placement check for one post (ship step)

Exit code 0 = CLEAN PASS or PASSED WITH ADVISORIES, 1 = FAILED.
"""
import argparse
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / 'content' / 'posts'
BOOK_DIR = ROOT / 'content' / 'book'
BUILD = ROOT / 'build.mjs'

BANNED = ['纯粹', '绝对', '完全', '彻底', '绝不', '通常', '往往', '或许', '某种意义上',
          '降维重构', '本质', '根本', '自始至终', '缰绳', '物理现实', '平庸', '物理意志']
TITLE_DELIMS = ['：', ':', ' - ', ' — ', '——']
LABELS = {
    '科学 / Scientific', '数学 / Mathematical', '哲学 / Philosophical', '宗教 / Religious',
    '意识形态 / Ideological', '经济 / Economic', '技术 / Technological', '成功学 / Self-Help',
}
ESSAYS_RE = re.compile(r'^##\s+篇目\s*/\s*Essays\s*$')
LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
POST_HREF_RE = re.compile(r'^\.\./\.\./posts/([A-Za-z0-9][A-Za-z0-9_-]*)/?(#.*)?$')
BOOK_HREF_RE = re.compile(r'^\.\./([a-z0-9-]+)/?(#.*)?$')
CJK_RE = re.compile(r'[\u3400-\u9fff]')
LATIN_WORD_RE = re.compile(r'[A-Za-z]{2,}')


def part_order():
    src = BUILD.read_text(encoding='utf-8')
    m = re.search(r'const PART_ORDER = \[(.*?)\];', src, re.S)
    if not m:
        sys.exit('Cannot find PART_ORDER in build.mjs')
    return re.findall(r"'([^']+)'", m.group(1))


def post_slugs():
    return sorted(p.stem for p in POSTS_DIR.glob('*.md') if p.name != 'README.md')


def creation_dates():
    """slug -> first-commit date (YYYY-MM-DD), single git pass."""
    out = subprocess.run(
        ['git', 'log', '--diff-filter=A', '--name-only', '--format=@%cs', '--', 'content/posts'],
        cwd=ROOT, capture_output=True, text=True, check=False,
    ).stdout
    dates, current = {}, None
    for line in out.splitlines():
        if line.startswith('@'):
            current = line[1:]
        elif line.startswith('content/posts/') and line.endswith('.md'):
            slug = Path(line).stem
            dates[slug] = current  # log is newest-first; last write wins = earliest add
    return dates


def strip_links(text):
    return LINK_RE.sub('', text)


def lang_of(paragraph):
    cjk = len(CJK_RE.findall(paragraph))
    latin = len(LATIN_WORD_RE.findall(paragraph))
    if cjk >= 8 and cjk >= latin:
        return 'zh'
    if latin >= 4:
        return 'en'
    return '?'


def paragraphs(lines):
    paras, buf = [], []
    for line in lines:
        if line.strip():
            buf.append(line.strip())
        elif buf:
            paras.append(' '.join(buf))
            buf = []
    if buf:
        paras.append(' '.join(buf))
    return paras


def check_prose(name, title, lines, errors, warnings):
    """Common authored-prose invariants for a book page (excluding link labels)."""
    if any(d in title for d in TITLE_DELIMS):
        errors.append(f'{name}: title contains a compound delimiter: {title}')
    body = '\n'.join(lines)
    scan = strip_links(title + '\n' + body)
    for w in BANNED:
        if w in scan:
            errors.append(f'{name}: banned word "{w}"')
    if '$' in scan:
        errors.append(f'{name}: raw "$" found')
    for href in (m.group(2) for m in LINK_RE.finditer(body)):
        if re.match(r'^https?://', href):
            errors.append(f'{name}: absolute URL in book prose: {href}')


def check_alternation(name, prose_lines, errors):
    paras = [p for p in paragraphs(prose_lines)
             if not p.startswith('#') and not (p.startswith('*') and p.endswith('*'))]
    langs = [lang_of(p) for p in paras]
    expected = 'zh'
    for i, lang in enumerate(langs):
        if lang == '?':
            continue
        if lang != expected:
            errors.append(f'{name}: paragraph {i + 1} is {lang}, expected {expected} (CN/EN alternation)')
            return
        expected = 'en' if expected == 'zh' else 'zh'
    if expected == 'en' and langs:
        errors.append(f'{name}: final Chinese paragraph has no English counterpart')


def read_book_file(slug):
    path = BOOK_DIR / f'{slug}.md'
    if not path.exists():
        return None, None
    lines = path.read_text(encoding='utf-8').splitlines()
    return lines[0][2:].strip() if lines and lines[0].startswith('# ') else '', lines[1:]


def audit_parts(order, slugs, errors, warnings):
    placement = {}
    per_part = {}
    for slug in order:
        title, lines = read_book_file(slug)
        if lines is None:
            errors.append(f'content/book/{slug}.md missing')
            continue
        idx = next((i for i, l in enumerate(lines) if ESSAYS_RE.match(l.strip())), None)
        if idx is None:
            errors.append(f'{slug}.md: no "## 篇目 / Essays" section')
            idx = len(lines)
        prose, essays = lines[:idx], lines[idx + 1:]
        check_prose(f'{slug}.md', title, prose, errors, warnings)
        check_alternation(f'{slug}.md', prose, errors)
        if not any(l.strip().startswith('*') and l.strip().endswith('*') for l in prose[:4]):
            errors.append(f'{slug}.md: missing italic subtitle line')
        listed = []
        for line in essays:
            for m in LINK_RE.finditer(line):
                pm = POST_HREF_RE.match(m.group(2).strip())
                if not pm or pm.group(1) not in slugs:
                    errors.append(f'{slug}.md: unresolved essay link {m.group(2)}')
                    continue
                s = pm.group(1)
                if s in placement:
                    errors.append(f'{s} placed in two parts: {placement[s]} and {slug}')
                    continue
                placement[s] = slug
                listed.append(s)
        per_part[slug] = listed
    return placement, per_part


def audit_index(slugs, errors, warnings):
    title, lines = read_book_file('index-of-premises')
    if lines is None:
        errors.append('content/book/index-of-premises.md missing')
        return {}, Counter(), Counter(), set()
    intro_end = next((i for i, l in enumerate(lines) if l.startswith('## ')), len(lines))
    check_prose('index-of-premises.md (intro)', title, lines[:intro_end], errors, warnings)
    check_alternation('index-of-premises.md (intro)', lines[:intro_end], errors)

    entries, section, entry = {}, None, None
    by_label, by_section = Counter(), Counter()
    linked = set()

    def finish():
        if not entry:
            return
        key = f"{section}:{entry['title']}"
        if key in entries:
            errors.append(f'index: duplicate entry {key}')
        entries[key] = entry
        if not entry['label']:
            errors.append(f"index: {entry['title']} has no label line")
        elif entry['label'] not in LABELS:
            errors.append(f"index: {entry['title']} has unknown label `{entry['label']}`")
        langs = [lang_of(p) for p in entry['paras']]
        if langs[:2] != ['zh', 'en']:
            errors.append(f"index: {entry['title']} needs one Chinese then one English premise sentence (got {langs})")
        if not entry['links']:
            errors.append(f"index: {entry['title']} has no post link")
        by_label[entry['label']] += 1
        by_section[section] += 1

    for raw in lines[intro_end:]:
        line = raw.strip()
        if line.startswith('### '):
            finish()
            entry = {'title': line[4:].strip(), 'label': '', 'paras': [], 'links': []}
            if ' / ' not in entry['title']:
                errors.append(f"index: entry heading not bilingual: {entry['title']}")
            continue
        if line.startswith('## '):
            finish()
            entry = None
            section = line[3:].strip()
            continue
        if not line or entry is None:
            continue
        if re.fullmatch(r'`[^`]+`', line):
            entry['label'] = line[1:-1]
        elif line.startswith('→'):
            for m in LINK_RE.finditer(line):
                pm = POST_HREF_RE.match(m.group(2).strip())
                if not pm or pm.group(1) not in slugs:
                    errors.append(f"index: {entry['title']} unresolved link {m.group(2)}")
                    continue
                entry['links'].append(pm.group(1))
                linked.add(pm.group(1))
        else:
            entry['paras'].append(line)
            scan = strip_links(line)
            for w in BANNED:
                if w in scan:
                    errors.append(f"index: {entry['title']} banned word \"{w}\"")
            if '$' in scan:
                errors.append(f"index: {entry['title']} raw \"$\"")
    finish()
    return entries, by_label, by_section, linked


def audit_preface(errors, warnings):
    title, lines = read_book_file('preface')
    if lines is None:
        errors.append('content/book/preface.md missing')
        return
    check_prose('preface.md', title, lines, errors, warnings)
    check_alternation('preface.md', lines, errors)
    for m in LINK_RE.finditer('\n'.join(lines)):
        href = m.group(2).strip()
        if not (POST_HREF_RE.match(href) or BOOK_HREF_RE.match(href)):
            errors.append(f'preface.md: link must be relative (../../posts/<slug>/ or ../<part>/): {href}')


def report(errors, warnings, passed):
    print('\n[PASSED INVARIANTS]')
    for p in passed:
        print(f'  ✓ {p}')
    if warnings:
        print('\n[CONTEXTUAL WARNINGS / DRIFT ADVISORIES]')
        for w in warnings:
            print(f'  ⚠ {w}')
    if errors:
        print('\n[CRITICAL VIOLATIONS]')
        for e in errors[:200]:
            print(f'  ✗ {e}')
        if len(errors) > 200:
            print(f'  … {len(errors) - 200} more')
        print('\nResult: FAILED.')
        return 1
    print('\nResult: PASSED WITH ADVISORIES.' if warnings else '\nResult: CLEAN PASS.')
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--slug')
    args = ap.parse_args()

    order = part_order()
    slugs = set(post_slugs())
    errors, warnings, passed = [], [], []

    print('=' * 70)
    print('BOOK AUDIT' + (f': placement of {args.slug}' if args.slug else ''))
    print('=' * 70)

    placement, per_part = audit_parts(order, slugs, errors, warnings)

    if args.slug:
        if args.slug not in slugs:
            errors.append(f'unknown post slug {args.slug}')
        elif args.slug not in placement:
            errors.append(f'{args.slug} is not placed in any part (add it to the "## 篇目 / Essays" list of one content/book/<part>.md)')
        else:
            part = placement[args.slug]
            passed.append(f'{args.slug} placed in part `{part}` (position {per_part[part].index(args.slug) + 1}/{len(per_part[part])})')
            if per_part[part][-1] != args.slug:
                warnings.append(f'{args.slug} is not last in `{part}`; parts list essays in the order written')
            _, _, _, linked = audit_index(slugs, [], [])
            if args.slug in linked:
                passed.append(f'{args.slug} is linked from the Index of Premises')
            else:
                warnings.append(f'{args.slug} has no Index of Premises entry; add/extend entries for figures, theories, or concepts it substantively dissects')
        return report(errors, warnings, passed)

    audit_preface(errors, warnings)
    entries, by_label, by_section, linked = audit_index(slugs, errors, warnings)

    unplaced = sorted(slugs - set(placement))
    if unplaced:
        errors.append(f'{len(unplaced)} post(s) not placed: {", ".join(unplaced)}')
    else:
        passed.append(f'coverage {len(placement)}/{len(slugs)} posts, each in exactly one part')

    dates = creation_dates()
    for part, listed in per_part.items():
        seq = [dates.get(s, '9999') for s in listed]
        if seq != sorted(seq):
            warnings.append(f'part `{part}` is not in the order written')
    passed.append('parts: ' + ', '.join(f'{p}={len(per_part.get(p, []))}' for p in order))

    if entries:
        passed.append(f'index: {len(entries)} entries · ' + ' · '.join(f'{k} {v}' for k, v in by_section.items()))
        passed.append('index labels: ' + ' · '.join(f'{k} {v}' for k, v in sorted(by_label.items(), key=lambda kv: -kv[1])))
        passed.append(f'index reaches {len(linked)}/{len(slugs)} posts')

    return report(errors, warnings, passed)


if __name__ == '__main__':
    sys.exit(main())
