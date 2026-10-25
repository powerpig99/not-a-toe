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
  python3 scripts/interleave-post.py --split <slug> [<slug2> ...]
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
    if block.startswith("### "):
        return "h3"
    if block.startswith("```mermaid"):
        return "mermaid"
    if (
        block.startswith("*")
        and not block.startswith("**")
        and block.endswith("*")
        and not block.endswith("**")
        and "\n" not in block
    ):
        return "subtitle"
    return "prose"


def interleave_blocks(slug: str, zh_blocks: list[str], en_blocks: list[str]) -> list[str]:
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
    return out


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
    out = interleave_blocks(slug, zh_blocks, en_blocks)
    out_path.write_text("\n\n".join(out) + "\n", encoding="utf-8")
    return out_path


def split_bilingual_pair(slug: str, block: str, prefix: str, suffix: str = "") -> tuple[str, str]:
    inner = block[len(prefix) : len(block) - len(suffix) if suffix else len(block)]
    if " / " not in inner:
        raise ValueError(f"[{slug}] Missing ' / ' separator in {block[:60]!r}")
    zh_part, en_part = inner.split(" / ", 1)
    return f"{prefix}{zh_part.strip()}{suffix}", f"{prefix}{en_part.strip()}{suffix}"


def split_slug(slug: str) -> tuple[pathlib.Path, pathlib.Path]:
    post_path = ROOT / "content" / "posts" / f"{slug}.md"
    if not post_path.exists():
        raise FileNotFoundError(f"Missing {post_path}")

    blocks = split_blocks(post_path.read_text(encoding="utf-8"))
    zh_blocks: list[str] = []
    en_blocks: list[str] = []

    i = 0
    n = len(blocks)
    while i < n:
        b = blocks[i]
        k = block_kind(b)
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

    rebuilt = interleave_blocks(slug, zh_blocks, en_blocks)
    if rebuilt != blocks:
        raise ValueError(f"[{slug}] Round-trip interleave mismatch after split")

    work_dir = ROOT / "work" / slug
    work_dir.mkdir(parents=True, exist_ok=True)
    zh_path = work_dir / "zh.md"
    en_path = work_dir / "en.md"
    zh_path.write_text("\n\n".join(zh_blocks) + "\n", encoding="utf-8")
    en_path.write_text("\n\n".join(en_blocks) + "\n", encoding="utf-8")
    return zh_path, en_path


def main(argv: list[str]) -> int:
    split_mode = "--split" in argv[1:]
    slugs = [arg.removesuffix(".md") for arg in argv[1:] if not arg.startswith("-")]
    if not slugs:
        print(
            "Usage: python3 scripts/interleave-post.py [--split] <slug> [<slug2> ...]",
            file=sys.stderr,
        )
        return 2

    for slug in slugs:
        if split_mode:
            zh_path, en_path = split_slug(slug)
            print(
                f"Split content/posts/{slug}.md -> "
                f"{zh_path.relative_to(ROOT)}, {en_path.relative_to(ROOT)}"
            )
        else:
            out_path = interleave_slug(slug)
            print(f"Interleaved work/{slug}/{{zh,en}}.md -> {out_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
