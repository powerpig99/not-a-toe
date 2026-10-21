#!/usr/bin/env python3
"""
Deterministic Stage 3 Assembler for Not a ToE (`scripts/interleave-post.py`).

Interleaves locked `work/<slug>/zh.md` and `work/<slug>/en.md` into
`content/posts/<slug>.md` adhering strictly to `AGENTS.md` invariants:
  - Line 1: `# <Chinese Title> / <English Title>`
  - Line 3: `*<Chinese Subtitle> / <English Subtitle>*`
  - Section Headings: `## 一、 <Chinese Heading> / 1. <English Heading>`
  - Blank lines inside ```mermaid ... ``` blocks are stripped before splitting
    so Mermaid diagrams never fracture into multiple blocks.
  - Diagrams are attached immediately to their preceding prose paragraph in
    each language (`CN Paragraph -> CN Diagram -> EN Paragraph -> EN Diagram`).

Usage:
  python3 scripts/interleave-post.py <slug> [<slug2> ...]
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


def block_kind(block: str) -> str:
    if block.startswith("# "):
        return "h1"
    if block.startswith("## "):
        return "h2"
    if block.startswith("```mermaid"):
        return "mermaid"
    if block.startswith("*") and block.endswith("*") and "\n" not in block:
        return "subtitle"
    return "prose"


def interleave_slug(slug: str) -> pathlib.Path:
    work_dir = ROOT / "work" / slug
    zh_path = work_dir / "zh.md"
    en_path = work_dir / "en.md"
    out_path = ROOT / "content" / "posts" / f"{slug}.md"

    if not zh_path.exists():
        raise FileNotFoundError(f"Missing {zh_path}")
    if not en_path.exists():
        raise FileNotFoundError(f"Missing {en_path}")

    zh_blocks = split_blocks(zh_path.read_text(encoding="utf-8"))
    en_blocks = split_blocks(en_path.read_text(encoding="utf-8"))

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
        zk, ek = block_kind(z), block_kind(e)
        if zk != ek:
            raise ValueError(
                f"[{slug}] Block kind mismatch at index {i}: zh={zk} ({z[:40]!r}) vs en={ek} ({e[:40]!r})"
            )

        if zk == "h1":
            out.append(f"{z} / {e[2:].strip()}")
            i += 1
        elif zk == "subtitle":
            out.append(f"*{z[1:-1].strip()} / {e[1:-1].strip()}*")
            i += 1
        elif zk == "h2":
            out.append(f"{z} / {e[3:].strip()}")
            i += 1
        elif zk == "prose":
            # Look ahead for consecutive Mermaid diagram(s) attached to this paragraph
            j = i + 1
            while j < n and block_kind(zh_blocks[j]) == "mermaid":
                if block_kind(en_blocks[j]) != "mermaid":
                    raise ValueError(
                        f"[{slug}] Diagram parity mismatch at index {j}: zh is mermaid, en is {block_kind(en_blocks[j])}"
                    )
                j += 1
            out.extend(zh_blocks[i:j])
            out.extend(en_blocks[i:j])
            i = j
        else:
            # Standalone mermaid block not preceded by prose
            out.append(z)
            out.append(e)
            i += 1

    out_path.write_text("\n\n".join(out) + "\n", encoding="utf-8")
    return out_path


def main(argv: list[str]) -> int:
    slugs = [arg.removesuffix(".md") for arg in argv[1:] if not arg.startswith("-")]
    if not slugs:
        print("Usage: python3 scripts/interleave-post.py <slug> [<slug2> ...]", file=sys.stderr)
        return 2

    for slug in slugs:
        out_path = interleave_slug(slug)
        print(f"Interleaved work/{slug}/{{zh,en}}.md -> {out_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
