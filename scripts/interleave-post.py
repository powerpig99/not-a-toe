#!/usr/bin/env python3
"""
Deterministic Stage 3 Splitter, Parity Checker, and Assembler for Not a ToE (`scripts/interleave-post.py`).

Interleaves locked `work/<slug>/zh.md` and `work/<slug>/en.md` into
`content/posts/<slug>.md` (or `work/_book:<name>/{zh,en}.md` into
`content/book/<name>.md` for `_book:preface`, `_book:<part>`, and
`_book:index-of-premises`) adhering strictly to `AGENTS.md` invariants:
  - Line 1: `# <Chinese Title> / <English Title>`
  - Line 3: `*<Chinese Subtitle> / <English Subtitle>*`
  - Section Headings: `## 一、 <Chinese Heading> / 1. <English Heading>`
  - Blank lines inside ```mermaid ... ``` blocks are stripped before splitting
    so Mermaid diagrams never fracture into multiple blocks.
  - Diagrams are attached immediately to their preceding prose paragraph in
    each language (`CN Paragraph -> CN Diagram -> EN Paragraph -> EN Diagram`).
  - Book surfaces (`_book:<name>`) preserve `## 篇目 / Essays` rosters and
    `index-of-premises.md` (`##` domain sections + `###` entries with paired
    category labels and `→` link lines) with lossless round-trip parity.

Usage:
  python3 scripts/interleave-post.py <slug> [<slug2> ...]
  python3 scripts/interleave-post.py --check <slug> [<slug2> ...]
  python3 scripts/interleave-post.py --split <slug> [<slug2> ...]
  python3 scripts/interleave-post.py --self-test
"""

from __future__ import annotations

import pathlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parent.parent


def split_blocks(text: str) -> list[str]:
    def clean_mermaid(match: re.Match[str]) -> str:
        lines = [line for line in match.group(0).splitlines() if line.strip()]
        return "\n".join(lines)

    cleaned = re.sub(r"```mermaid.*?```", clean_mermaid, text, flags=re.DOTALL)
    return [block.strip() for block in re.split(r"\n\s*\n", cleaned.strip()) if block.strip()]


def block_kind(block: str, index: int = -1) -> str:
    if block.startswith("# "):
        return "h1"
    if block.startswith("## "):
        return "h2"
    if block.startswith("### "):
        return "h3"
    if block.startswith("```mermaid"):
        return "mermaid"
    if (
        index == 1
        and block.startswith("*")
        and not block.startswith("**")
        and block.endswith("*")
        and not block.endswith("**")
        and "\n" not in block
    ):
        return "subtitle"
    return "prose"


LINK_TARGET_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
MERMAID_LABEL_RE = re.compile(r'(\["[^"]*"\]|\("[^"]*"\)|\[[^\]]*\]|\([^)]*\))')
MERMAID_EDGE_LABEL_RE = re.compile(r'\|"[^"]*"\||\|[^|]*\|')
MERMAID_QUOTE_RE = re.compile(r'"[^"]*"')
MERMAID_IDENT_RE = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\b")


def extract_link_targets(block: str) -> list[str]:
    return sorted(m.group(1).strip() for m in LINK_TARGET_RE.finditer(block))


def extract_mermaid_skeleton(block: str) -> list[str]:
    structure: list[str] = []
    styles: list[str] = []
    id_map: dict[str, str] = {}

    def canon_id(name: str) -> str:
        if name not in id_map:
            id_map[name] = f"n{len(id_map)}"
        return id_map[name]

    raw_styles: list[tuple[str, str]] = []
    for raw in block.splitlines():
        line = raw.strip()
        if not line or line.startswith("```") or line.startswith("%%"):
            continue
        if line.startswith(("flowchart ", "graph ")):
            structure.append(re.sub(r"^graph\s+", "flowchart ", line))
        elif line.startswith("subgraph "):
            no_label = MERMAID_QUOTE_RE.sub("", MERMAID_LABEL_RE.sub("", line)).strip()
            parts = no_label.split(None, 2)
            if len(parts) >= 2:
                structure.append(f"subgraph {canon_id(parts[1])}")
            else:
                structure.append(no_label)
        elif line == "end" or line.startswith("direction "):
            structure.append(line)
        elif line.startswith("linkStyle "):
            raw_styles.append(("linkStyle", line))
        elif line.startswith(("style ", "classDef ")):
            raw_styles.append(("style", line))
        elif line.startswith("class "):
            raw_styles.append(("class", line))
        else:
            cleaned = MERMAID_EDGE_LABEL_RE.sub("||", line)
            cleaned = MERMAID_LABEL_RE.sub("[]", cleaned)
            cleaned = MERMAID_QUOTE_RE.sub('""', cleaned)
            cleaned = MERMAID_IDENT_RE.sub(lambda m: canon_id(m.group(0)), cleaned)
            structure.append(cleaned)

    for kind, line in raw_styles:
        if kind == "linkStyle":
            styles.append(line)
        elif kind == "style":
            parts = line.split(None, 2)
            if len(parts) >= 3:
                styles.append(f"{parts[0]} {canon_id(parts[1])} {parts[2]}")
            elif len(parts) == 2:
                styles.append(f"{parts[0]} {canon_id(parts[1])}")
            else:
                styles.append(line)
        elif kind == "class":
            parts = line.split(None, 2)
            if len(parts) == 3:
                targets = ",".join(canon_id(t.strip()) for t in parts[1].split(",") if t.strip())
                styles.append(f"class {targets} {canon_id(parts[2])}")
            else:
                styles.append(line)
    return structure + styles


def check_pair_alignment(slug: str, idx: int, kind: str, z: str, e: str) -> None:
    if kind == "prose":
        zh_links = extract_link_targets(z)
        en_links = extract_link_targets(e)
        if zh_links != en_links:
            raise ValueError(
                f"[{slug}] Link target multiset mismatch at block {idx}: zh={zh_links} vs en={en_links}"
            )
    elif kind == "mermaid":
        zh_skel = extract_mermaid_skeleton(z)
        en_skel = extract_mermaid_skeleton(e)
        if zh_skel != en_skel:
            raise ValueError(
                f"[{slug}] Mermaid skeleton mismatch at block {idx}:\n  zh={zh_skel}\n  en={en_skel}"
            )


def interleave_blocks(slug: str, zh_blocks: list[str], en_blocks: list[str], strict: bool = True) -> list[str]:
    if len(zh_blocks) != len(en_blocks):
        raise ValueError(
            f"[{slug}] Block count mismatch: zh.md has {len(zh_blocks)} blocks, "
            f"en.md has {len(en_blocks)} blocks."
        )

    out: list[str] = []
    i = 0
    n = len(zh_blocks)
    while i < n:
        z, e = zh_blocks[i], en_blocks[i]
        zk, ek = block_kind(z, i), block_kind(e, i)
        if zk != ek:
            raise ValueError(
                f"[{slug}] Block kind mismatch at index {i}: zh={zk} ({z[:40]!r}) vs en={ek} ({e[:40]!r})"
            )

        if zk == "h1":
            z_body, e_body = z[2:].strip(), e[2:].strip()
            if z_body == e_body and " / " in z_body:
                out.append(f"# {z_body}")
            else:
                if " / " in z_body:
                    z_body = z_body.split(" / ", 1)[0].strip()
                if " / " in e_body:
                    e_body = e_body.split(" / ", 1)[1].strip()
                out.append(f"# {z_body} / {e_body}")
            i += 1
        elif zk == "subtitle":
            z_body, e_body = z[1:-1].strip(), e[1:-1].strip()
            if z_body == e_body and " / " in z_body:
                out.append(f"*{z_body}*")
            else:
                if " / " in z_body:
                    z_body = z_body.split(" / ", 1)[0].strip()
                if " / " in e_body:
                    e_body = e_body.split(" / ", 1)[1].strip()
                out.append(f"*{z_body} / {e_body}*")
            i += 1
        elif zk in ("h2", "h3"):
            prefix = "## " if zk == "h2" else "### "
            z_body, e_body = z[len(prefix) :].strip(), e[len(prefix) :].strip()
            if z_body == e_body and " / " in z_body:
                out.append(f"{prefix}{z_body}")
            else:
                if " / " in z_body:
                    z_body = z_body.split(" / ", 1)[0].strip()
                if " / " in e_body:
                    e_body = e_body.split(" / ", 1)[1].strip()
                out.append(f"{prefix}{z_body} / {e_body}")
            i += 1
        elif zk == "prose":
            if strict:
                check_pair_alignment(slug, i, "prose", z, e)
            # Look ahead for consecutive Mermaid diagram(s) attached to this paragraph
            j = i + 1
            while j < n and block_kind(zh_blocks[j]) == "mermaid":
                if block_kind(en_blocks[j]) != "mermaid":
                    raise ValueError(
                        f"[{slug}] Diagram parity mismatch at index {j}: zh is mermaid, en is {block_kind(en_blocks[j])}"
                    )
                if strict:
                    check_pair_alignment(slug, j, "mermaid", zh_blocks[j], en_blocks[j])
                j += 1
            out.extend(zh_blocks[i:j])
            out.extend(en_blocks[i:j])
            i = j
        else:
            # Standalone mermaid block not preceded by prose
            if strict:
                check_pair_alignment(slug, i, zk, z, e)
            out.append(z)
            out.append(e)
            i += 1
    return out


BOOK_LABEL_PAIRS = {
    "科学": "Scientific",
    "数学": "Mathematical",
    "哲学": "Philosophical",
    "宗教": "Religious",
    "意识形态": "Ideological",
    "经济": "Economic",
    "技术": "Technological",
    "成功学": "Self-Help",
}
BOOK_TITLE_DELIMS = ("：", ":", " - ", " — ", "——")


def is_book_node(slug: str) -> bool:
    return slug.startswith("_book:")


def resolve_book_node(slug: str) -> tuple[str, pathlib.Path]:
    name = slug[6:].removesuffix(".md")
    if not name or "/" in name or ".." in name:
        raise ValueError(f"Invalid book surface node: {slug!r}")
    return f"_book:{name}", ROOT / "content" / "book" / f"{name}.md"


def split_bilingual_pair(slug: str, block: str, prefix: str, suffix: str = "") -> tuple[str, str]:
    inner = block[len(prefix) : len(block) - len(suffix) if suffix else len(block)]
    if " / " not in inner:
        raise ValueError(f"[{slug}] Missing ' / ' separator in {block[:80]!r}")
    zh_part, en_part = inner.split(" / ", 1)
    return f"{prefix}{zh_part.strip()}{suffix}", f"{prefix}{en_part.strip()}{suffix}"


def split_preface_or_part_blocks(node: str, text: str) -> tuple[list[str], list[str]]:
    blocks = split_blocks(text)
    zh_blocks: list[str] = []
    en_blocks: list[str] = []
    i = 0
    n = len(blocks)
    essays_idx = next(
        (k for k, b in enumerate(blocks) if re.match(r"^##\s+篇目\s*/\s*Essays\s*$", b)),
        None,
    )
    limit = essays_idx if essays_idx is not None else n
    while i < limit:
        b = blocks[i]
        k = block_kind(b, i)
        if k == "h1":
            z, e = split_bilingual_pair(node, b, "# ")
            zh_blocks.append(z)
            en_blocks.append(e)
            i += 1
        elif k == "subtitle":
            z, e = split_bilingual_pair(node, b, "*", "*")
            zh_blocks.append(z)
            en_blocks.append(e)
            i += 1
        elif k in ("h2", "h3"):
            prefix = "## " if k == "h2" else "### "
            z, e = split_bilingual_pair(node, b, prefix)
            zh_blocks.append(z)
            en_blocks.append(e)
            i += 1
        else:
            if i + 1 >= limit or block_kind(blocks[i + 1], i + 1) != k:
                raise ValueError(f"[{node}] Unpaired {k} block at index {i}: {b[:60]!r}")
            zh_blocks.append(blocks[i])
            en_blocks.append(blocks[i + 1])
            i += 2

    if essays_idx is not None:
        zh_blocks.append("## 篇目")
        en_blocks.append("## Essays")
        for b in blocks[essays_idx + 1 :]:
            zh_blocks.append(b)
            en_blocks.append(b)

    return zh_blocks, en_blocks


def interleave_preface_or_part_blocks(
    node: str, zh_blocks: list[str], en_blocks: list[str], strict: bool = True
) -> str:
    if len(zh_blocks) != len(en_blocks):
        raise ValueError(
            f"[{node}] Block count mismatch: zh.md has {len(zh_blocks)} blocks, "
            f"en.md has {len(en_blocks)} blocks."
        )
    out: list[str] = []
    in_essays = False
    for idx, (z, e) in enumerate(zip(zh_blocks, en_blocks)):
        z_is_essays = bool(re.match(r"^##\s+篇目(?:\s*/\s*Essays)?\s*$", z))
        e_is_essays = bool(re.match(r"^##\s+(?:篇目\s*/\s*)?Essays\s*$", e))
        if z_is_essays or e_is_essays:
            if not (z_is_essays and e_is_essays):
                raise ValueError(
                    f"[{node}] Essays heading mismatch at block {idx}: zh={z!r} vs en={e!r}"
                )
            in_essays = True
            out.append("## 篇目 / Essays")
            continue
        if in_essays:
            if z != e:
                raise ValueError(
                    f"[{node}] Essay roster mismatch under ## 篇目 / Essays at block {idx}:\n"
                    f"  zh={z!r}\n  en={e!r}"
                )
            out.append(z)
            continue

        zk, ek = block_kind(z, idx), block_kind(e, idx)
        if zk != ek:
            raise ValueError(
                f"[{node}] Block kind mismatch at index {idx}: zh={zk} ({z[:40]!r}) vs en={ek} ({e[:40]!r})"
            )
        if zk == "h1":
            zb, eb = z[2:].strip(), e[2:].strip()
            if " / " in zb:
                zb = zb.split(" / ", 1)[0].strip()
            if " / " in eb:
                eb = eb.split(" / ", 1)[-1].strip()
            combined_title = f"{zb} / {eb}"
            if strict and any(d in combined_title for d in BOOK_TITLE_DELIMS):
                raise ValueError(f"[{node}] Title contains prohibited compound delimiter: {combined_title!r}")
            out.append(f"# {combined_title}")
        elif zk == "subtitle":
            zb, eb = z[1:-1].strip(), e[1:-1].strip()
            if " / " in zb:
                zb = zb.split(" / ", 1)[0].strip()
            if " / " in eb:
                eb = eb.split(" / ", 1)[-1].strip()
            out.append(f"*{zb} / {eb}*")
        elif zk in ("h2", "h3"):
            prefix = "## " if zk == "h2" else "### "
            zb, eb = z[len(prefix) :].strip(), e[len(prefix) :].strip()
            if " / " in zb:
                zb = zb.split(" / ", 1)[0].strip()
            if " / " in eb:
                eb = eb.split(" / ", 1)[-1].strip()
            out.append(f"{prefix}{zb} / {eb}")
        else:
            if strict:
                check_pair_alignment(node, idx, zk, z, e)
            out.append(z)
            out.append(e)
    return "\n\n".join(out) + "\n"


def _parse_index_entries_from_lines(node: str, lines: list[str], bilingual: bool) -> list[dict]:
    items: list[dict] = []
    cur: dict | None = None

    def flush() -> None:
        nonlocal cur
        if cur is not None:
            items.append(cur)
            cur = None

    for raw in lines:
        s = raw.strip()
        if not s:
            continue
        if s.startswith("## "):
            flush()
            items.append({"kind": "section", "heading": s})
        elif s.startswith("### "):
            flush()
            cur = {
                "kind": "entry",
                "heading": s,
                "label": "",
                "paras": [],
                "arrow": "",
            }
        elif cur is not None:
            if re.fullmatch(r"`[^`]+`", s) and not cur["label"]:
                cur["label"] = s
            elif s.startswith("→") and not cur["arrow"]:
                cur["arrow"] = s
            else:
                cur["paras"].append(s)
        else:
            raise ValueError(f"[{node}] Unexpected line outside section/entry: {s[:80]!r}")
    flush()

    for it in items:
        if it["kind"] != "entry":
            continue
        if not it["label"]:
            raise ValueError(f"[{node}] Entry {it['heading']!r} missing backtick label")
        if not it["arrow"]:
            raise ValueError(f"[{node}] Entry {it['heading']!r} missing '→' link line")
        expected_paras = 2 if bilingual else 1
        if len(it["paras"]) != expected_paras:
            raise ValueError(
                f"[{node}] Entry {it['heading']!r} expected {expected_paras} premise paragraph(s), "
                f"got {len(it['paras'])}"
            )
    return items


def split_index_text(node: str, text: str) -> tuple[str, str]:
    lines = text.splitlines()
    first_h2_line = next((i for i, ln in enumerate(lines) if ln.strip().startswith("## ")), len(lines))
    intro_raw = "\n".join(lines[:first_h2_line]).strip() + "\n"
    zh_intro, en_intro = split_preface_or_part_blocks(node, intro_raw)
    items = _parse_index_entries_from_lines(node, lines[first_h2_line:], bilingual=True)

    zh_parts: list[str] = ["\n\n".join(zh_intro)]
    en_parts: list[str] = ["\n\n".join(en_intro)]
    for it in items:
        if it["kind"] == "section":
            hz, he = split_bilingual_pair(node, it["heading"], "## ")
            zh_parts.append(hz)
            en_parts.append(he)
        else:
            hz, he = split_bilingual_pair(node, it["heading"], "### ")
            lz, le = split_bilingual_pair(node, it["label"], "`", "`")
            zh_p, en_p = it["paras"][0], it["paras"][1]
            arrow = it["arrow"]
            zh_parts.append(f"{hz}\n{lz}\n\n{zh_p}\n\n{arrow}")
            en_parts.append(f"{he}\n{le}\n\n{en_p}\n\n{arrow}")

    return "\n\n".join(zh_parts) + "\n", "\n\n".join(en_parts) + "\n"


def interleave_index_texts(node: str, zh_text: str, en_text: str, strict: bool = True) -> str:
    z_lines = zh_text.splitlines()
    e_lines = en_text.splitlines()
    fz = next((i for i, ln in enumerate(z_lines) if ln.strip().startswith("## ")), len(z_lines))
    fe = next((i for i, ln in enumerate(e_lines) if ln.strip().startswith("## ")), len(e_lines))

    z_intro_blocks = split_blocks("\n".join(z_lines[:fz]))
    e_intro_blocks = split_blocks("\n".join(e_lines[:fe]))
    intro_out = interleave_preface_or_part_blocks(node, z_intro_blocks, e_intro_blocks, strict=strict).rstrip("\n")

    z_items = _parse_index_entries_from_lines(node, z_lines[fz:], bilingual=False)
    e_items = _parse_index_entries_from_lines(node, e_lines[fe:], bilingual=False)
    if len(z_items) != len(e_items):
        raise ValueError(
            f"[{node}] Index item count mismatch: zh.md has {len(z_items)} sections/entries, "
            f"en.md has {len(e_items)} sections/entries."
        )

    out_chunks: list[str] = [intro_out]
    for idx, (zi, ei) in enumerate(zip(z_items, e_items)):
        if zi["kind"] != ei["kind"]:
            raise ValueError(f"[{node}] Item kind mismatch at {idx}: zh={zi} vs en={ei}")
        if zi["kind"] == "section":
            zb = zi["heading"][3:].split(" / ", 1)[0].strip()
            eb = ei["heading"][3:].split(" / ", 1)[-1].strip()
            out_chunks.append(f"## {zb} / {eb}")
        else:
            zb = zi["heading"][4:].split(" / ", 1)[0].strip()
            eb = ei["heading"][4:].split(" / ", 1)[-1].strip()
            lz = zi["label"][1:-1].split(" / ", 1)[0].strip()
            le = ei["label"][1:-1].split(" / ", 1)[-1].strip()
            if strict and BOOK_LABEL_PAIRS.get(lz) != le:
                raise ValueError(
                    f"[{node}] Label mismatch under '{zb} / {eb}': zh=`{lz}` vs en=`{le}` "
                    f"(expected {BOOK_LABEL_PAIRS.get(lz)!r})"
                )
            if zi["arrow"] != ei["arrow"]:
                raise ValueError(
                    f"[{node}] '→' link line mismatch under '{zb} / {eb}':\n"
                    f"  zh={zi['arrow']}\n  en={ei['arrow']}"
                )
            zh_p = zi["paras"][0]
            en_p = ei["paras"][0]
            if strict:
                zh_links = extract_link_targets(zh_p)
                en_links = extract_link_targets(en_p)
                if zh_links != en_links:
                    raise ValueError(
                        f"[{node}] Premise paragraph link mismatch under '{zb} / {eb}': "
                        f"zh={zh_links} vs en={en_links}"
                    )
            out_chunks.append(f"### {zb} / {eb}\n`{lz} / {le}`\n\n{zh_p}\n\n{en_p}\n\n{zi['arrow']}")

    return "\n\n".join(out_chunks) + "\n"


def check_book_node(slug: str) -> str:
    node, _ = resolve_book_node(slug)
    work_dir = ROOT / "work" / node
    zh_path = work_dir / "zh.md"
    en_path = work_dir / "en.md"
    if not zh_path.is_file():
        raise FileNotFoundError(f"Missing {zh_path}")
    if not en_path.is_file():
        raise FileNotFoundError(f"Missing {en_path}")
    zh_txt = zh_path.read_text(encoding="utf-8")
    en_txt = en_path.read_text(encoding="utf-8")
    if node == "_book:index-of-premises":
        return interleave_index_texts(node, zh_txt, en_txt, strict=True)
    return interleave_preface_or_part_blocks(node, split_blocks(zh_txt), split_blocks(en_txt), strict=True)


def check_slug(slug: str) -> None:
    if is_book_node(slug):
        check_book_node(slug)
        return
    work_dir = ROOT / "work" / slug
    zh_path = work_dir / "zh.md"
    en_path = work_dir / "en.md"

    if not zh_path.exists():
        raise FileNotFoundError(f"Missing {zh_path}")
    if not en_path.exists():
        raise FileNotFoundError(f"Missing {en_path}")

    zh_blocks = split_blocks(zh_path.read_text(encoding="utf-8"))
    en_blocks = split_blocks(en_path.read_text(encoding="utf-8"))
    interleave_blocks(slug, zh_blocks, en_blocks, strict=True)


def sync_h1_change(slug: str, old_h1: str, new_h1: str) -> None:
    if old_h1 == new_h1 or not (old_h1.startswith("# ") and new_h1.startswith("# ")):
        return
    old_inner, new_inner = old_h1[2:].strip(), new_h1[2:].strip()
    if " / " not in old_inner or " / " not in new_inner:
        return
    old_zh, old_en = [p.strip() for p in old_inner.split(" / ", 1)]
    new_zh, new_en = [p.strip() for p in new_inner.split(" / ", 1)]
    updated_files = 0

    book_dir = ROOT / "content" / "book"
    work_root = ROOT / "work"
    book_targets: list[pathlib.Path] = sorted(book_dir.glob("*.md")) if book_dir.is_dir() else []
    if work_root.is_dir():
        book_targets.extend(sorted(work_root.glob("_book:*/en.md")) + sorted(work_root.glob("_book:*/zh.md")))
    old_book_link = f"[{old_inner}](../../posts/{slug}/)"
    new_book_link = f"[{new_inner}](../../posts/{slug}/)"
    old_book_zh_link = f"[{old_zh}](../../posts/{slug}/)"
    new_book_zh_link = f"[{new_zh}](../../posts/{slug}/)"
    old_book_en_link = f"[{old_en}](../../posts/{slug}/)"
    new_book_en_link = f"[{new_en}](../../posts/{slug}/)"
    for bf in book_targets:
        txt = bf.read_text(encoding="utf-8")
        new_txt = txt.replace(old_book_link, new_book_link)
        if old_zh != new_zh and old_book_zh_link in new_txt:
            new_txt = new_txt.replace(old_book_zh_link, new_book_zh_link)
        if old_en != new_en and old_book_en_link in new_txt:
            new_txt = new_txt.replace(old_book_en_link, new_book_en_link)
        if new_txt != txt:
            bf.write_text(new_txt, encoding="utf-8")
            updated_files += 1

    post_targets: list[pathlib.Path] = sorted((ROOT / "content" / "posts").glob("*.md"))
    if work_root.is_dir():
        for wf in sorted(work_root.glob("*/en.md")) + sorted(work_root.glob("*/zh.md")):
            if not wf.parent.name.startswith("_book:"):
                post_targets.append(wf)

    old_zh_link = f"[{old_zh}](../{slug}/)"
    new_zh_link = f"[{new_zh}](../{slug}/)"
    old_en_link = f"[{old_en}](../{slug}/)"
    new_en_link = f"[{new_en}](../{slug}/)"
    for pf in post_targets:
        if pf.name == "README.md" or pf == ROOT / "content" / "posts" / f"{slug}.md":
            continue
        txt = pf.read_text(encoding="utf-8")
        new_txt = txt
        if old_zh != new_zh and old_zh_link in new_txt:
            new_txt = new_txt.replace(old_zh_link, new_zh_link)
        if old_en != new_en and old_en_link in new_txt:
            new_txt = new_txt.replace(old_en_link, new_en_link)
        if new_txt != txt:
            pf.write_text(new_txt, encoding="utf-8")
            updated_files += 1

    print(
        f"Synced H1 change for {slug}: '{old_inner}' -> '{new_inner}' ({updated_files} file(s) updated)"
    )


def interleave_slug(slug: str) -> pathlib.Path:
    if is_book_node(slug):
        node, book_path = resolve_book_node(slug)
        assembled = check_book_node(node)
        book_path.write_text(assembled, encoding="utf-8")
        return book_path

    work_dir = ROOT / "work" / slug
    zh_path = work_dir / "zh.md"
    en_path = work_dir / "en.md"
    out_path = ROOT / "content" / "posts" / f"{slug}.md"

    if not zh_path.exists():
        raise FileNotFoundError(f"Missing {zh_path}")
    if not en_path.exists():
        raise FileNotFoundError(f"Missing {en_path}")

    old_h1 = ""
    if out_path.exists():
        old_blocks = split_blocks(out_path.read_text(encoding="utf-8"))
        if old_blocks and old_blocks[0].startswith("# "):
            old_h1 = old_blocks[0]

    zh_blocks = split_blocks(zh_path.read_text(encoding="utf-8"))
    en_blocks = split_blocks(en_path.read_text(encoding="utf-8"))
    out = interleave_blocks(slug, zh_blocks, en_blocks)
    out_path.write_text("\n\n".join(out) + "\n", encoding="utf-8")
    if old_h1 and out and out[0].startswith("# "):
        sync_h1_change(slug, old_h1, out[0])
    return out_path


def split_book_node(slug: str) -> tuple[pathlib.Path, pathlib.Path]:
    node, book_path = resolve_book_node(slug)
    if not book_path.is_file():
        raise FileNotFoundError(f"Missing {book_path}")
    work_dir = ROOT / "work" / node
    zh_path = work_dir / "zh.md"
    en_path = work_dir / "en.md"
    for existing in (en_path, zh_path):
        if existing.exists():
            raise FileExistsError(
                f"[{node}] Refusing to overwrite in-flight artifact {existing.relative_to(ROOT)} "
                f"(for read-only parity check use: python3 scripts/interleave-post.py --check {node})"
            )

    raw = book_path.read_text(encoding="utf-8")
    if node == "_book:index-of-premises":
        zh_txt, en_txt = split_index_text(node, raw)
        rebuilt = interleave_index_texts(node, zh_txt, en_txt, strict=False)
    else:
        zh_b, en_b = split_preface_or_part_blocks(node, raw)
        zh_txt = "\n\n".join(zh_b) + "\n"
        en_txt = "\n\n".join(en_b) + "\n"
        rebuilt = interleave_preface_or_part_blocks(node, zh_b, en_b, strict=False)

    if split_blocks(rebuilt) != split_blocks(raw):
        raise ValueError(f"[{node}] Round-trip interleave mismatch after split")

    work_dir.mkdir(parents=True, exist_ok=True)
    zh_path.write_text(zh_txt, encoding="utf-8")
    en_path.write_text(en_txt, encoding="utf-8")
    return zh_path, en_path


def split_slug(slug: str) -> tuple[pathlib.Path, pathlib.Path]:
    if is_book_node(slug):
        return split_book_node(slug)
    post_path = ROOT / "content" / "posts" / f"{slug}.md"
    if not post_path.exists():
        raise FileNotFoundError(f"Missing {post_path}")

    work_dir = ROOT / "work" / slug
    zh_path = work_dir / "zh.md"
    en_path = work_dir / "en.md"
    for existing in (en_path, zh_path):
        if existing.exists():
            raise FileExistsError(
                f"[{slug}] Refusing to overwrite in-flight artifact {existing.relative_to(ROOT)} "
                f"(for read-only parity check use: python3 scripts/interleave-post.py --check {slug})"
            )

    blocks = split_blocks(post_path.read_text(encoding="utf-8"))
    zh_blocks: list[str] = []
    en_blocks: list[str] = []

    i = 0
    n = len(blocks)
    while i < n:
        b = blocks[i]
        k = block_kind(b, i)
        if k == "h1":
            z, e = split_bilingual_pair(slug, b, "# ")
            zh_blocks.append(z)
            en_blocks.append(e)
            i += 1
        elif k == "subtitle":
            z, e = split_bilingual_pair(slug, b, "*", "*")
            zh_blocks.append(z)
            en_blocks.append(e)
            i += 1
        elif k in ("h2", "h3"):
            prefix = "## " if k == "h2" else "### "
            z, e = split_bilingual_pair(slug, b, prefix)
            zh_blocks.append(z)
            en_blocks.append(e)
            i += 1
        elif k == "prose":
            j = i + 1
            while j < n and block_kind(blocks[j]) == "mermaid":
                j += 1
            span = j - i
            if j + span > n:
                raise ValueError(f"[{slug}] Unpaired block at end of post starting at index {i}")
            zh_group = blocks[i:j]
            en_group = blocks[j : j + span]
            if [block_kind(x) for x in zh_group] != [block_kind(x) for x in en_group]:
                raise ValueError(
                    f"[{slug}] Group kind mismatch at index {i}: "
                    f"zh={[block_kind(x) for x in zh_group]} vs en={[block_kind(x) for x in en_group]}"
                )
            zh_blocks.extend(zh_group)
            en_blocks.extend(en_group)
            i = j + span
        else:
            if i + 1 >= n or block_kind(blocks[i + 1]) != k:
                raise ValueError(f"[{slug}] Unpaired standalone {k} block at index {i}")
            zh_blocks.append(blocks[i])
            en_blocks.append(blocks[i + 1])
            i += 2

    rebuilt = interleave_blocks(slug, zh_blocks, en_blocks, strict=False)
    if rebuilt != blocks:
        raise ValueError(f"[{slug}] Round-trip interleave mismatch after split")

    work_dir.mkdir(parents=True, exist_ok=True)
    zh_path.write_text("\n\n".join(zh_blocks) + "\n", encoding="utf-8")
    en_path.write_text("\n\n".join(en_blocks) + "\n", encoding="utf-8")
    return zh_path, en_path


def self_test() -> None:
    book_files = sorted((ROOT / "content" / "book").glob("*.md"))
    for bp in book_files:
        node = f"_book:{bp.stem}"
        raw = bp.read_text(encoding="utf-8")
        if node == "_book:index-of-premises":
            zh_txt, en_txt = split_index_text(node, raw)
            rebuilt = interleave_index_texts(node, zh_txt, en_txt, strict=True)
        else:
            zh_b, en_b = split_preface_or_part_blocks(node, raw)
            rebuilt = interleave_preface_or_part_blocks(node, zh_b, en_b, strict=True)
        exact = rebuilt == raw
        if not exact and split_blocks(rebuilt) != split_blocks(raw):
            raise ValueError(f"Self-test mismatch on {node}")
        print(f"SELF_TEST OK: {node} (byte_exact={exact})")


def main(argv: list[str]) -> int:
    split_mode = "--split" in argv[1:]
    check_mode = "--check" in argv[1:]
    self_test_mode = "--self-test" in argv[1:]
    if sum((split_mode, check_mode, self_test_mode)) > 1:
        print("Error: --split, --check, and --self-test are mutually exclusive.", file=sys.stderr)
        return 2
    unknown_flags = [
        arg for arg in argv[1:] if arg.startswith("-") and arg not in ("--split", "--check", "--self-test")
    ]
    if unknown_flags:
        print(
            f"Error: Unknown flag(s) {', '.join(unknown_flags)}. "
            "Usage: python3 scripts/interleave-post.py [--check | --split | --self-test] <slug> [<slug2> ...]",
            file=sys.stderr,
        )
        return 2
    if self_test_mode:
        try:
            self_test()
        except (ValueError, FileNotFoundError, FileExistsError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        return 0

    slugs = [arg.removesuffix(".md") for arg in argv[1:] if not arg.startswith("-")]
    if not slugs:
        print(
            "Usage: python3 scripts/interleave-post.py [--check | --split | --self-test] <slug> [<slug2> ...]",
            file=sys.stderr,
        )
        return 2

    try:
        for slug in slugs:
            if check_mode:
                check_slug(slug)
                print(f"Parity OK: {slug}")
            elif split_mode:
                zh_path, en_path = split_slug(slug)
                src_rel = (
                    f"content/book/{slug[6:]}.md"
                    if is_book_node(slug)
                    else f"content/posts/{slug}.md"
                )
                print(
                    f"Split {src_rel} -> "
                    f"{zh_path.relative_to(ROOT)}, {en_path.relative_to(ROOT)}"
                )
            else:
                out_path = interleave_slug(slug)
                work_label = f"_book:{slug[6:]}" if is_book_node(slug) else slug
                print(f"Interleaved work/{work_label}/{{zh,en}}.md -> {out_path.relative_to(ROOT)}")
    except (ValueError, FileNotFoundError, FileExistsError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
