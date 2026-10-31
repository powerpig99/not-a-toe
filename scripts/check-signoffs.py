#!/usr/bin/env python3
"""
Deterministic Stage 3 sign-off and sha256 handoff verifier (`scripts/check-signoffs.py`).

Checks for each `work/<slug>/` DELTA node before Stage 3 interleaving:
  1. `work/<slug>/debate-en.md` ends with a `CRITIC: confirmed` line whose `sha256`
     matches the current `sha256(work/<slug>/en.md)`.
  2. `work/<slug>/debate-zh.md` (or `debate-en.md`) records `HANDOFF_CONFIRMED` with
     the same `en.md` `sha256`.
  3. `work/<slug>/debate-zh.md` ends with a `STYLIST: confirmed` line whose `sha256`
     matches `sha256(work/<slug>/zh.md)` and whose `source_sha256` matches
     `sha256(work/<slug>/en.md)`.

Usage:
  python3 scripts/check-signoffs.py <slug> [<slug2> ...]
"""

from __future__ import annotations

import hashlib
import pathlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parent.parent
HEX64 = r"([0-9a-f]{64})"


def sha256_file(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def last_match(pattern: str, text: str) -> re.Match[str] | None:
    matches = list(re.finditer(pattern, text, flags=re.MULTILINE))
    return matches[-1] if matches else None


def missing_or_decorated(
    slug: str,
    token: str,
    signoff_body_pattern: str,
    file_label: str,
    text: str,
    with_sha256: bool = True,
) -> str:
    if re.search(r"^[^\S\n]*\S[^\n]*?" + signoff_body_pattern, text, flags=re.MULTILINE):
        return (
            f"[{slug}] Found '{token}' in {file_label} but not at a line start "
            "(list marker, quote or backtick before it); write it as its own line"
        )
    suffix = " with sha256" if with_sha256 else ""
    return f"[{slug}] Missing '{token}'{suffix} in {file_label}"


def check_slug(slug: str) -> list[str]:
    errors: list[str] = []
    work_dir = ROOT / "work" / slug
    en_path = work_dir / "en.md"
    zh_path = work_dir / "zh.md"
    deb_en_path = work_dir / "debate-en.md"
    deb_zh_path = work_dir / "debate-zh.md"

    for p in (en_path, zh_path, deb_en_path, deb_zh_path):
        if not p.is_file():
            errors.append(f"[{slug}] Missing {p.relative_to(ROOT)}")
    if errors:
        return errors

    en_sha = sha256_file(en_path)
    zh_sha = sha256_file(zh_path)
    deb_en = deb_en_path.read_text(encoding="utf-8")
    deb_zh = deb_zh_path.read_text(encoding="utf-8")

    critic_body = r"CRITIC:\s*confirmed\b[^\n]*?" + HEX64
    m_critic = last_match(r"^" + critic_body, deb_en)
    if not m_critic:
        errors.append(
            missing_or_decorated(
                slug,
                "CRITIC: confirmed",
                critic_body,
                "debate-en.md",
                deb_en,
            )
        )
    elif m_critic.group(1) != en_sha:
        errors.append(
            f"[{slug}] CRITIC sha256 ({m_critic.group(1)[:12]}...) != en.md ({en_sha[:12]}...)"
        )

    handoff_body = r"HANDOFF_CONFIRMED:[^\n]*?" + HEX64
    m_handoff = last_match(r"^" + handoff_body, deb_zh) or last_match(
        r"^" + handoff_body, deb_en
    )
    if not m_handoff:
        errors.append(
            missing_or_decorated(
                slug,
                "HANDOFF_CONFIRMED",
                handoff_body,
                "debate-zh.md (or debate-en.md)",
                deb_zh + "\n" + deb_en,
            )
        )
    elif m_handoff.group(1) != en_sha:
        errors.append(
            f"[{slug}] HANDOFF_CONFIRMED sha256 ({m_handoff.group(1)[:12]}...) != en.md ({en_sha[:12]}...)"
        )

    m_stylist = last_match(r"^STYLIST:\s*confirmed\b([^\n]*)", deb_zh)
    if not m_stylist:
        errors.append(
            missing_or_decorated(
                slug,
                "STYLIST: confirmed",
                r"STYLIST:\s*confirmed\b[^\n]*?\bsha256:\s*" + HEX64,
                "debate-zh.md",
                deb_zh,
                with_sha256=False,
            )
        )
    else:
        tail = m_stylist.group(1)
        m_zh_sha = re.search(r"\bsha256:\s*" + HEX64, tail)
        m_src_sha = re.search(r"\bsource_sha256:\s*" + HEX64, tail)
        if not m_zh_sha:
            errors.append(f"[{slug}] STYLIST: confirmed missing 'sha256: <64-hex>'")
        elif m_zh_sha.group(1) != zh_sha:
            errors.append(
                f"[{slug}] STYLIST sha256 ({m_zh_sha.group(1)[:12]}...) != zh.md ({zh_sha[:12]}...)"
            )
        if not m_src_sha:
            errors.append(
                f"[{slug}] STYLIST: confirmed missing 'source_sha256: <en.md 64-hex>'"
            )
        elif m_src_sha.group(1) != en_sha:
            errors.append(
                f"[{slug}] STYLIST source_sha256 ({m_src_sha.group(1)[:12]}...) != en.md ({en_sha[:12]}...)"
            )

    return errors


def main(argv: list[str]) -> int:
    slugs = [arg.removesuffix(".md") for arg in argv[1:] if not arg.startswith("-")]
    if not slugs:
        print("Usage: python3 scripts/check-signoffs.py <slug> [<slug2> ...]", file=sys.stderr)
        return 2

    all_errors: list[str] = []
    for slug in slugs:
        errs = check_slug(slug)
        if errs:
            all_errors.extend(errs)
        else:
            print(f"Sign-offs verified: work/{slug}/ (CRITIC + HANDOFF_CONFIRMED + STYLIST)")

    if all_errors:
        for e in all_errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
