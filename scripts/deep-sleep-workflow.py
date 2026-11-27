#!/usr/bin/env python3
"""
Tier 1 Antigravity `run_workflow` dispatcher for `/deep-sleep` (`not-a-toe`).

Executes inside Antigravity's `run_workflow` Python runtime where `agent`,
`parallel`, `phase`, `log`, and `args` are provided as workflow globals.
Replaces repeated outer-loop LLM yield/kill turns with a deterministic Python
loop over bounded `asyncio.Semaphore(W)` `drafter -> translator` streamlines,
deterministic Stage 3 assembly/audits/deploy/`--record-batch`, conditional batch
`recap`, and cleanup of settled `work/<slug>/` workspaces.
"""

from __future__ import annotations

import asyncio
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(WORKSPACES[0]) if "WORKSPACES" in globals() and WORKSPACES else Path.cwd()
SITE_BASE = "https://powerpig99.github.io/not-a-toe"
TRACKED_STAGE3_PATHS = (
    "content/posts/",
    "content/book/",
    "data/title-translations.json",
    "docs/posts.graph.json",
)
IGNORED_REPO_PREFIXES = (
    ".git",
    "work",
    "memory",
    "public",
    "studio",
    "drafts",
    ".claude",
    ".grok",
    "__pycache__",
)
PROTECTED_OUTER_ANCHOR_PATHS = (
    "scripts/audit-post.py",
    "scripts/audit-book.py",
    "scripts/check-signoffs.py",
    "scripts/interleave-post.py",
    "scripts/deep-sleep-workflow.py",
    "AGENTS.md",
)
PROTECTED_OUTER_ANCHOR_PREFIXES = (
    "studio/kits/shared/checks/",
)

DRAFTER_SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "enum": ["PASS", "HOLD", "FAIL"]},
        "verdict": {"type": "string", "enum": ["DELTA", "NO_DELTA", "HOLD"]},
        "sha256": {"type": "string"},
        "log": {"type": "string"},
        "note": {"type": "string"},
    },
    "required": ["status", "verdict", "sha256", "log"],
}

TRANSLATOR_SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "enum": ["PASS", "REOPEN_STAGE1", "FAIL", "HOLD"]},
        "sha256": {"type": "string"},
        "t_items": {"type": "integer"},
        "log": {"type": "string"},
        "note": {"type": "string"},
    },
    "required": ["status", "sha256", "log"],
}

RECAP_SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "enum": ["PASS", "OPEN_ISSUES"]},
        "open_issues": {"type": "integer"},
        "log": {"type": "string"},
        "modified_files": {"type": "array", "items": {"type": "string"}},
        "summary": {"type": "string"},
    },
    "required": ["status", "open_issues", "log"],
}

BATCH_HEADER_RE = re.compile(
    r"^BATCH:\s+(\d+)\s+\(mode=([^,]+),\s*count=(\d+),\s*concurrency=(\d+),\s*remaining_after=(\d+)\)"
)
BATCH_ITEM_RE = re.compile(
    r"^\d+\.\s+(\S+)\s+\|\s+part=([^|]+)\|\s+source=([^|]+)\|\s+related=(.*)$"
)
RECORDED_RE = re.compile(
    r"BATCH_RECORDED:\s+batch=(\d+)\s+delta=(\d+)\s+no_delta=(\d+)\s+remaining=(\d+)\s+commit=(\S+)\s+log=(\S+)"
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tail_output(proc: subprocess.CompletedProcess[str], limit: int = 1200) -> str:
    combined = "\n".join(part for part in (proc.stdout.strip(), proc.stderr.strip()) if part)
    return combined[-limit:] if len(combined) > limit else combined


def summarize_gate_error(err: str, limit: int = 280) -> str:
    lines = [ln.strip() for ln in err.splitlines() if ln.strip()]
    if not lines:
        return "unknown error"
    header = lines[0].rstrip(":")
    focus = [
        ln for ln in lines[1:]
        if ln.startswith(("ERROR:", "✗", "ValueError:", "FileNotFoundError:"))
    ]
    body_lines = focus if focus else lines[1:]
    summary = f"{header}: {' | '.join(body_lines)}" if body_lines else header
    summary = re.sub(r"\s+", " ", summary).strip()
    if len(summary) > limit:
        return summary[: limit - 1].rstrip() + "…"
    return summary


async def run_cmd(
    cmd: list[str],
    *,
    cwd: Path | None = None,
    check: bool = False,
) -> subprocess.CompletedProcess[str]:
    proc = await asyncio.to_thread(
        subprocess.run,
        cmd,
        cwd=str(cwd or ROOT),
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        check=False,
    )
    if check and proc.returncode != 0:
        detail = tail_output(proc) or f"exit code {proc.returncode}"
        raise RuntimeError(f"Command failed ({' '.join(cmd)}): {detail}")
    return proc


def normalize_repo_commit_paths(
    raw_paths: list[str] | None,
    *,
    root: Path = ROOT,
) -> tuple[list[str], list[str]]:
    """Filter candidate paths to unique repo-relative non-ignored file paths inside `root`."""
    root_norm = Path(os.path.normpath(str(root.expanduser())))
    if not root_norm.is_absolute():
        root_norm = Path(os.path.normpath(str(Path.cwd() / root_norm)))
    root_resolved = root.resolve()
    candidates: list[str] = []
    skipped: list[str] = []
    seen: set[str] = set()

    for raw in raw_paths or []:
        raw_str = str(raw).strip()
        if not raw_str:
            continue
        expanded = Path(raw_str).expanduser()
        cand_lex = expanded if expanded.is_absolute() else (root_norm / expanded)
        cand_norm = Path(os.path.normpath(str(cand_lex)))
        if cand_norm.is_relative_to(root_norm):
            rel = cand_norm.relative_to(root_norm).as_posix()
        elif cand_norm.is_relative_to(root_resolved):
            rel = cand_norm.relative_to(root_resolved).as_posix()
        else:
            skipped.append(raw_str)
            continue
        if not cand_norm.resolve().is_relative_to(root_resolved):
            skipped.append(raw_str)
            continue
        if rel in ("", ".") or any(
            rel == pref or rel.startswith(f"{pref}/") for pref in IGNORED_REPO_PREFIXES
        ):
            skipped.append(raw_str)
            continue
        if cand_norm.is_dir():
            skipped.append(raw_str)
            continue
        if rel not in seen:
            seen.add(rel)
            candidates.append(rel)

    return candidates, skipped


def _repo_rel_variants(raw_path: str, *, root: Path = ROOT) -> list[str]:
    """Return unique normalized repo-relative POSIX path(s) (lexical and resolved) inside `root`."""
    raw_str = str(raw_path).strip().replace("\\", "/")
    if not raw_str:
        return []
    root_norm = Path(os.path.normpath(str(root.expanduser())))
    if not root_norm.is_absolute():
        root_norm = Path(os.path.normpath(str(Path.cwd() / root_norm)))
    root_resolved = root.resolve()

    expanded = Path(raw_str).expanduser()
    cand_lex = expanded if expanded.is_absolute() else (root_norm / expanded)
    cand_norm = Path(os.path.normpath(str(cand_lex)))

    variants: list[str] = []
    for base in (root_norm, root_resolved):
        if cand_norm.is_relative_to(base):
            rel = cand_norm.relative_to(base).as_posix()
            if rel not in ("", ".") and rel not in variants:
                variants.append(rel)
            break
    try:
        cand_resolved = cand_norm.resolve()
        if cand_resolved.is_relative_to(root_resolved):
            rel_res = cand_resolved.relative_to(root_resolved).as_posix()
            if rel_res not in ("", ".") and rel_res not in variants:
                variants.append(rel_res)
    except OSError:
        pass
    return variants


def match_protected_outer_anchor(raw_path: str, *, root: Path = ROOT) -> str | None:
    """Return canonical repo-relative path if `raw_path` targets a protected outer anchor, else None."""
    exact_set = set(PROTECTED_OUTER_ANCHOR_PATHS)
    exact_lower = {p.lower(): p for p in PROTECTED_OUTER_ANCHOR_PATHS}
    clean_prefixes = [p.rstrip("/") for p in PROTECTED_OUTER_ANCHOR_PREFIXES]
    clean_prefixes_lower = [p.lower() for p in clean_prefixes]

    for rel in _repo_rel_variants(raw_path, root=root):
        if rel in exact_set:
            return rel
        rel_lower = rel.lower()
        if rel_lower in exact_lower:
            return exact_lower[rel_lower]
        for pref, pref_lower in zip(clean_prefixes, clean_prefixes_lower):
            if rel == pref or rel.startswith(f"{pref}/"):
                return rel
            if rel_lower == pref_lower or rel_lower.startswith(f"{pref_lower}/"):
                return rel
    return None


def is_protected_outer_anchor(raw_path: str, *, root: Path = ROOT) -> bool:
    """Return True iff `raw_path` matches a protected outer-anchor path or prefix."""
    return match_protected_outer_anchor(raw_path, root=root) is not None


def find_protected_outer_anchors(
    paths: list[str] | tuple[str, ...] | set[str] | None,
    *,
    root: Path = ROOT,
) -> list[str]:
    """Return sorted unique protected outer-anchor paths present in `paths`."""
    hits: set[str] = set()
    for raw in paths or ():
        matched = match_protected_outer_anchor(raw, root=root)
        if matched is not None:
            hits.add(matched)
    return sorted(hits)


def snapshot_protected_prefixes(
    *,
    root: Path = ROOT,
    prefixes: tuple[str, ...] = PROTECTED_OUTER_ANCHOR_PREFIXES,
) -> dict[str, str]:
    """Hash files under protected prefixes so edits to gitignored anchors are detected too."""
    snap: dict[str, str] = {}
    for pref in prefixes:
        base = root / pref.rstrip("/")
        if not base.exists():
            continue
        if base.is_file():
            snap[base.relative_to(root).as_posix()] = sha256_file(base)
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = sorted(d for d in dirnames if d != "__pycache__")
            for fname in sorted(filenames):
                if fname == ".DS_Store" or fname.endswith(".pyc"):
                    continue
                fpath = Path(dirpath) / fname
                if fpath.is_file():
                    snap[fpath.relative_to(root).as_posix()] = sha256_file(fpath)
    return snap


def diff_snapshots(before: dict[str, str], after: dict[str, str]) -> list[str]:
    """Return sorted repo-relative paths added, removed, or modified between two snapshots."""
    return [
        rel
        for rel in sorted(set(before) | set(after))
        if before.get(rel) != after.get(rel)
    ]


def parse_porcelain_z_paths(stdout: str) -> list[str]:
    """Parse NUL-delimited `git status --porcelain -z` output into unique repo-relative paths.

    For rename (`R`) and copy (`C`) entries (`XY dest\\0orig\\0`), both destination
    and original paths are returned so guards catch moves touching protected anchors.
    """
    tokens = stdout.split("\0")
    paths: list[str] = []
    seen: set[str] = set()
    i = 0
    while i < len(tokens):
        entry = tokens[i]
        i += 1
        if not entry or len(entry) < 4 or entry[2] != " ":
            continue
        xy = entry[:2]
        dest = entry[3:]
        if dest and dest not in seen:
            seen.add(dest)
            paths.append(dest)
        if xy[0] in ("R", "C") or xy[1] in ("R", "C"):
            if i < len(tokens):
                orig = tokens[i]
                i += 1
                if orig and orig not in seen:
                    seen.add(orig)
                    paths.append(orig)
    return paths


async def detect_protected_outer_anchor_changes(
    reported_paths: list[str] | None = None,
    *,
    root: Path = ROOT,
    prefix_snapshot_before: dict[str, str] | None = None,
) -> list[str]:
    """Inspect full-repo `git status --porcelain -z -uall`, reported paths, and protected prefix snapshots."""
    status_proc = await run_cmd(
        ["git", "status", "--porcelain", "-z", "-uall"],
        cwd=root,
        check=True,
    )
    candidates: list[str] = parse_porcelain_z_paths(status_proc.stdout)
    if reported_paths:
        candidates.extend(reported_paths)
    if prefix_snapshot_before is not None:
        prefix_snapshot_after = snapshot_protected_prefixes(root=root)
        candidates.extend(diff_snapshots(prefix_snapshot_before, prefix_snapshot_after))
    return find_protected_outer_anchors(candidates, root=root)


def append_outer_anchor_guard_note(
    batch_num: int,
    protected_paths: list[str],
    open_issues: int,
    *,
    log_path: str | None = None,
    recap_log: str | None = None,
    root: Path = ROOT,
) -> None:
    """Record an Outer-Anchor Guard halt in the batch log and recap log."""
    block = "\n".join(
        [
            "",
            "## Outer-Anchor Guard Halt (`STATUS: OPEN_ISSUES`)",
            "",
            f"- **Status:** `STATUS: OPEN_ISSUES` (`open_issues={open_issues}`, Batch `{batch_num}`)",
            "- **Action:** Refused silent auto-commit/push; halted for Outer-Loop Operator ratification.",
            "- **Protected Outer-Anchor Path(s):** " + ", ".join(f"`{p}`" for p in protected_paths),
            "",
        ]
    )
    if log_path:
        batch_log_file = root / log_path
        if batch_log_file.is_file():
            with batch_log_file.open("a", encoding="utf-8") as fh:
                fh.write(block)
    if recap_log:
        recap_log_file = root / recap_log
        recap_log_file.parent.mkdir(parents=True, exist_ok=True)
        mode = "a" if recap_log_file.is_file() else "w"
        with recap_log_file.open(mode, encoding="utf-8") as fh:
            if mode == "w":
                fh.write(f"# Batch {batch_num} Recap — Outer-Anchor Guard Halt\n")
            fh.write(block)


async def finalize_batch_recap(
    batch_num: int,
    recap_res: dict,
    *,
    log_path: str | None = None,
    recap_log: str | None = None,
    prefix_snapshot_before: dict[str, str] | None = None,
    root: Path = ROOT,
    push: bool = True,
) -> tuple[int, list[str], str | None]:
    """Enforce the Outer-Anchor Guard on batch Recap outputs and commit allowed tracked edits."""
    open_issues = int(recap_res["open_issues"])
    reported_files = recap_res.get("modified_files")
    protected_outer_anchors = await detect_protected_outer_anchor_changes(
        reported_files,
        root=root,
        prefix_snapshot_before=prefix_snapshot_before,
    )
    if protected_outer_anchors:
        open_issues = max(open_issues, 1)
        guard_note = (
            f"Outer-Anchor Guard refused silent auto-commit/push for Batch {batch_num} recap: "
            f"protected outer-anchor path(s) touched: {', '.join(protected_outer_anchors)} "
            f"(forced open_issues={open_issues}; awaiting Outer-Loop Operator ratification)."
        )
        if "log" in globals() and callable(globals()["log"]):
            log(f"Batch {batch_num} recap: {guard_note}")
        append_outer_anchor_guard_note(
            batch_num,
            protected_outer_anchors,
            open_issues,
            log_path=log_path,
            recap_log=recap_log,
            root=root,
        )
        return open_issues, protected_outer_anchors, guard_note

    dirty_recap_files, skipped_recap_files = await filter_dirty_repo_commit_paths(
        reported_files,
        root=root,
    )
    if skipped_recap_files and "log" in globals() and callable(globals()["log"]):
        log(f"Batch {batch_num} recap: skipped non-repo/excluded path(s): {', '.join(skipped_recap_files)}")
    if open_issues == 0 and dirty_recap_files:
        await run_cmd(["git", "add", "--", *dirty_recap_files], cwd=root, check=True)
        await run_cmd(["git", "commit", "-m", f"Apply Deep Sleep Batch {batch_num} recap"], cwd=root, check=True)
        if push:
            await run_cmd(["git", "push", "origin", "main"], cwd=root, check=True)
    return open_issues, [], None


async def filter_dirty_repo_commit_paths(
    raw_paths: list[str] | None,
    *,
    root: Path = ROOT,
) -> tuple[list[str], list[str]]:
    """Return (dirty_repo_relative_paths, skipped_paths) safe to pass to `git add`."""
    candidates, skipped = normalize_repo_commit_paths(raw_paths, root=root)
    if not candidates:
        return [], skipped

    status_proc = await run_cmd(
        ["git", "status", "--porcelain", "-z", "-uall", "--", *candidates],
        cwd=root,
        check=True,
    )
    dirty_set = set(parse_porcelain_z_paths(status_proc.stdout))
    dirty_paths = [rel for rel in candidates if rel in dirty_set]
    return dirty_paths, skipped


def check_charter_hashes(
    drafter_type: str, translator_type: str, recap_type: str
) -> list[tuple[str, str, str]]:
    checks = [
        ("drafter", drafter_type, ROOT / "docs" / "charters" / "drafter.md"),
        ("translator", translator_type, ROOT / "docs" / "charters" / "translator.md"),
        ("recap", recap_type, ROOT / "docs" / "charters" / "recap.md"),
    ]
    mismatches: list[tuple[str, str, str]] = []
    for role, type_name, path in checks:
        sha8 = sha256_file(path)[:8]
        if not type_name.endswith(f"-{sha8}"):
            mismatches.append((role, type_name, sha8))
    return mismatches


async def select_next_batch(batch_size: int, part_filter: str | None) -> dict:
    cmd = ["node", "scripts/project-posts-graph.mjs", "--next-batch", str(batch_size)]
    if part_filter:
        cmd.extend(["--part", part_filter])
    proc = await run_cmd(cmd, check=True)
    lines = [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
    header_match = None
    items: list[dict[str, str]] = []
    for ln in lines:
        if header_match is None:
            m = BATCH_HEADER_RE.match(ln)
            if m:
                header_match = m
                continue
        im = BATCH_ITEM_RE.match(ln)
        if im:
            items.append(
                {
                    "slug": im.group(1).strip(),
                    "part": im.group(2).strip(),
                    "source": im.group(3).strip(),
                    "related": im.group(4).strip(),
                }
            )
    if header_match is None:
        raise RuntimeError(f"Unable to parse --next-batch output: {proc.stdout!r}")
    return {
        "batch_num": int(header_match.group(1)),
        "mode": header_match.group(2).strip(),
        "count": int(header_match.group(3)),
        "concurrency": int(header_match.group(4)),
        "remaining_after": int(header_match.group(5)),
        "items": items,
    }


def target_path_for(slug: str, *, root: Path = ROOT) -> tuple[bool, Path]:
    if slug.startswith("_book:"):
        return True, root / "content" / "book" / f"{slug[6:]}.md"
    return False, root / "content" / "posts" / f"{slug}.md"


def live_url_for(slug: str) -> str:
    if slug == "_book:preface":
        return f"{SITE_BASE}/"
    if slug.startswith("_book:"):
        return f"{SITE_BASE}/book/{slug[6:]}/"
    return f"{SITE_BASE}/posts/{slug}/"


def build_drafter_prompt(
    item: dict[str, str],
    *,
    today: str,
    repair_error: str | None = None,
    reopen_t_items: bool = False,
) -> str:
    slug = item["slug"]
    is_book, target_rel_path = target_path_for(slug)
    target_rel = target_rel_path.relative_to(ROOT).as_posix()
    if item["source"] == "work/todo.md":
        todo_note = f"- Triggering `work/todo.md` items: read all unchecked `- [ ]` items mentioning `{slug}` in `work/todo.md` and evaluate/resolve every valid one.\n"
    elif item["source"].startswith("work/todo.md"):
        todo_note = f"- Triggering `work/todo.md` item: `{item['source']}` — inspect that exact line in `work/todo.md` and evaluate its cited prior/claim.\n"
    else:
        todo_note = ""
    related_note = (
        f"- Related material / prior cited: `{item['related']}`.\n"
        if item["related"] and item["related"] != "none"
        else ""
    )
    audit_cmd = (
        "verify `AGENTS.md` book prose invariants manually (do NOT run `audit-post.py` on `_book:` surfaces)"
        if is_book
        else f"run `python3 scripts/audit-post.py work/{slug}/en.md`"
    )
    interfaces_step = (
        f"record your causal trace and `VERDICT: DELTA (terminal) | RESTATERS: none` in `work/{slug}/notes.md` (skip `--interfaces` for `_book:` surfaces)"
        if is_book
        else f"inspect `node scripts/project-posts-graph.mjs --interfaces {slug}`, document moved wording & restaters in `work/{slug}/notes.md`"
    )
    repair_block = ""
    if repair_error:
        repair_block = (
            "\n**REPAIR PASS (previous Stage 1 verification failed — fix this exact defect and re-verify):**\n"
            f"```text\n{repair_error}\n```\n"
        )
    elif reopen_t_items:
        repair_block = (
            "\n**REOPENED STAGE 1 (Translator logged T-item(s) in `work/{slug}/notes.md`):**\n"
            f"Read `work/{slug}/notes.md`, resolve every logged T-item cleanly in `work/{slug}/en.md`, "
            f"re-verify ({audit_cmd}) and `python3 scripts/check-signoffs.py --stage1 {slug}`, and update `DRAFTER: confirmed` with the new 64-hex `sha256`.\n"
        ).format(slug=slug, audit_cmd=audit_cmd)

    return (
        f"Stage 1 `/deep-sleep` fresh first-time logical evaluation for `{slug}` in `{ROOT}`.\n"
        f"- Mode: `/deep-sleep` (evaluate `{target_rel}` as if for the first time under `/ontological-clarity` and `\"非必要不变更，防止无意识漂移\"`).\n"
        f"- Target file: `{target_rel}` (book part context: `{item['part']}`)\n"
        f"- Workspace: `work/{slug}/` (`work/{slug}/notes.md`, plus `work/{slug}/en.md` if `DELTA`)\n"
        f"- Today's sign-off date: `{today}`\n"
        f"{todo_note}{related_note}"
        "- Read `/Users/jingliang/.gemini/config/plugins/ontological-clarity/skills/ontological-clarity/SKILL.md`, `AGENTS.md`, `content/posts/README.md`, `work/carry-over.md` (if present), and related materials across the Living Book as deemed necessary (`content/book/index-of-premises.md`, `content/book/<part>.md`, linked neighbors, and conceptually related posts). NEVER read `work/wave.md`.\n"
        "- Open `DELTA` **strictly** for an obvious contradiction, logical inconsistency, missing causally required cross-link, or broken repository / 1:1 `信` invariant — never for minor improvements, optional polish, or out-of-file Index observations.\n"
        f"- If `NO_DELTA`: write your per-section first-time trace in `work/{slug}/notes.md` (plus any 1-line `### For work/todo.md` observation if an out-of-file Index or cross-node note applies), append `VERDICT: NO_DELTA | RESTATERS: none`, `SUMMARY: <1-line>`, and `DRAFTER: confirmed_no_delta (file: {target_rel}, sha256: <64-hex>, date: {today})`, and run `python3 scripts/check-signoffs.py --stage1 {slug}`.\n"
        f"- If `DELTA`: run `python3 scripts/interleave-post.py --split {slug}`, edit pure English Markdown in `work/{slug}/en.md`, {interfaces_step}, {audit_cmd}, append `VERDICT: DELTA (terminal|propagates) | RESTATERS: ...`, `SUMMARY: <1-line>`, and `DRAFTER: confirmed (file: work/{slug}/en.md, sha256: <64-hex>, date: {today})`, and verify with `python3 scripts/check-signoffs.py --stage1 {slug}`.\n"
        f"{repair_block}"
        f"**Mandatory completion rule:** When done, call the `finish` tool with JSON matching the schema (`status`: `\"PASS\"` or `\"HOLD\"`, `verdict`: `\"DELTA\"`, `\"NO_DELTA\"`, or `\"HOLD\"`, `sha256`: the exact 64-hex hash you signed in `notes.md`, `log`: `\"work/{slug}/notes.md\"`). Do NOT call `send_message`."
    )


def build_translator_prompt(
    item: dict[str, str],
    *,
    en_sha: str,
    today: str,
    repair_error: str | None = None,
) -> str:
    slug = item["slug"]
    is_book, _ = target_path_for(slug)
    audit_step = (
        "verify pure-Chinese `AGENTS.md` book prose invariants manually (do NOT run `audit-post.py` on `_book:` surfaces)"
        if is_book
        else f"run `python3 scripts/audit-post.py work/{slug}/zh.md`"
    )
    repair_block = ""
    if repair_error:
        repair_block = (
            "\n**REPAIR PASS (previous Stage 2 verification failed — fix this exact error and re-verify):**\n"
            f"```text\n{repair_error}\n```\n"
        )
    return (
        f"Stage 2 translation and 1:1 `信 / 达 / 雅` verification for `{slug}` in `{ROOT}`.\n"
        f"- Locked source: `work/{slug}/en.md` (expected `sha256`: `{en_sha}`)\n"
        f"- Baseline Chinese file: `work/{slug}/zh.md` (produced by `--split`)\n"
        f"- Notes / handoff file: `work/{slug}/notes.md`\n"
        f"- Today's sign-off date: `{today}`\n"
        "- Follow `docs/charters/translator.md`: recompute `sha256(work/<slug>/en.md)`, verify it matches `DRAFTER: confirmed`, and write `HANDOFF_CONFIRMED: work/<slug>/en.md (sha256: <hash>)` on its own line in `work/{slug}/notes.md`.\n"
        "- Read `AGENTS.md` and the linked posts/Index entries in context. Audit the entire `work/<slug>/zh.md` line-by-line against `work/<slug>/en.md` for 1:1 `信` fidelity, native Chinese `达/雅` cadence, and pure-Chinese headers/anchors/diagrams.\n"
        "- If `en.md` has a source flaw or ambiguity, log T-items (`T1..Tn`) in `work/<slug>/notes.md` and call `finish` with `status=\"REOPEN_STAGE1\"`.\n"
        f"- Otherwise run `python3 scripts/interleave-post.py --check {slug}` and {audit_step}, then append `TRANSLATOR: confirmed (file: work/{slug}/zh.md, sha256: <64-hex>, source_sha256: {en_sha}, date: {today})` to `work/{slug}/notes.md`.\n"
        f"{repair_block}"
        f"**Mandatory completion rule:** Call `finish` with JSON matching the schema (`status`: `\"PASS\"`, `\"REOPEN_STAGE1\"`, `\"FAIL\"`, or `\"HOLD\"`, `sha256`: exact 64-hex hash of `work/{slug}/zh.md` if `PASS`, `t_items`: integer count if `REOPEN_STAGE1`, `log`: `\"work/{slug}/notes.md\"`). Do NOT call `send_message`."
    )


async def verify_stage1(
    slug: str, is_book: bool, expected_sha: str
) -> tuple[bool, str | None, str | None, str]:
    proc = await run_cmd(["python3", "scripts/check-signoffs.py", "--stage1", slug])
    if proc.returncode != 0:
        return False, None, None, f"check-signoffs --stage1 failed:\n{tail_output(proc)}"
    m = re.search(r"\(verdict=([^)]+)\)", proc.stdout)
    verdict = m.group(1).strip() if m else None
    if not verdict:
        return False, None, None, f"Could not parse verdict from --stage1 output: {proc.stdout!r}"
    if verdict == "NO_DELTA":
        _, target_path = target_path_for(slug)
        disk_sha = sha256_file(target_path)
        if expected_sha and expected_sha != disk_sha:
            log(f"[{slug}] note: NO_DELTA finish sha256 {expected_sha[:8]} != disk {disk_sha[:8]}; using --stage1 verified disk hash")
        return True, "NO_DELTA", disk_sha, ""
    en_path = ROOT / "work" / slug / "en.md"
    if not en_path.is_file():
        return False, None, None, f"Missing work/{slug}/en.md after Stage 1 DELTA sign-off"
    en_sha = sha256_file(en_path)
    if expected_sha != en_sha:
        return (
            False,
            None,
            None,
            f"Stage 1 DELTA sha256 mismatch: finish reported {expected_sha}, disk en.md is {en_sha}",
        )
    if not is_book:
        audit = await run_cmd(["python3", "scripts/audit-post.py", f"work/{slug}/en.md"])
        if audit.returncode != 0:
            return False, None, None, f"audit-post.py work/{slug}/en.md failed:\n{tail_output(audit)}"
    return True, verdict, en_sha, ""


async def verify_stage2(
    slug: str, is_book: bool, expected_zh_sha: str
) -> tuple[bool, str | None, str | None, str]:
    chk = await run_cmd(["python3", "scripts/interleave-post.py", "--check", slug])
    if chk.returncode != 0:
        return False, None, None, f"interleave-post --check failed:\n{tail_output(chk)}"
    if not is_book:
        audit = await run_cmd(["python3", "scripts/audit-post.py", f"work/{slug}/zh.md"])
        if audit.returncode != 0:
            return False, None, None, f"audit-post.py work/{slug}/zh.md failed:\n{tail_output(audit)}"
    zh_path = ROOT / "work" / slug / "zh.md"
    if not zh_path.is_file():
        return False, None, None, f"Missing work/{slug}/zh.md after Stage 2"
    zh_sha = sha256_file(zh_path)
    if expected_zh_sha != zh_sha:
        return (
            False,
            None,
            None,
            f"Stage 2 zh.md sha256 mismatch: finish reported {expected_zh_sha}, disk zh.md is {zh_sha}",
        )
    signoff = await run_cmd(["python3", "scripts/check-signoffs.py", slug])
    if signoff.returncode != 0:
        return False, None, None, f"check-signoffs {slug} failed:\n{tail_output(signoff)}"
    m = re.search(r"\(verdict=([^)]+)\)", signoff.stdout)
    verdict = m.group(1).strip() if m else None
    if not verdict:
        return False, None, None, f"Could not parse verdict from check-signoffs output: {signoff.stdout!r}"
    return True, verdict, zh_sha, ""


async def run_node_pipeline(
    item: dict[str, str],
    sem: asyncio.Semaphore,
    *,
    drafter_type: str,
    translator_type: str,
    agent_model: str,
) -> dict:
    slug = item["slug"]
    is_book, _ = target_path_for(slug)
    today = datetime.now().strftime("%Y-%m-%d")

    async with sem:
        if (ROOT / "work" / "_wake" / "interrupt").exists():
            return {"slug": slug, "state": "SKIPPED_FOR_WAKE"}

        # Stage 1: Drafter (+ at most 1 repair pass)
        repairs = 0
        repair_notes: list[str] = []
        dres = await agent(
            prompt=build_drafter_prompt(item, today=today),
            schema=DRAFTER_SCHEMA,
            role=f"Drafter: {slug}",
            type_name=drafter_type,
            workspace="inherit",
            model=agent_model,
        )
        if dres["status"] == "FAIL":
            return {"slug": slug, "state": "FAIL", "error": dres.get("note") or "Drafter returned FAIL", "repair_notes": repair_notes}
        if dres["status"] == "HOLD" or dres["verdict"] == "HOLD":
            return {"slug": slug, "state": "HOLD", "note": dres.get("note", ""), "repair_notes": repair_notes}

        ok1, verdict1, sha1, err1 = await verify_stage1(slug, is_book, dres["sha256"])
        if not ok1:
            repairs += 1
            repair_notes.append(f"Stage 1 ({summarize_gate_error(err1)})")
            dres = await agent(
                prompt=build_drafter_prompt(item, today=today, repair_error=err1),
                schema=DRAFTER_SCHEMA,
                role=f"Drafter Repair: {slug}",
                type_name=drafter_type,
                workspace="inherit",
                model=agent_model,
            )
            if dres["status"] == "FAIL":
                return {"slug": slug, "state": "FAIL", "error": dres.get("note") or "Drafter repair returned FAIL", "repair_notes": repair_notes}
            if dres["status"] == "HOLD" or dres["verdict"] == "HOLD":
                return {"slug": slug, "state": "HOLD", "note": dres.get("note", ""), "repair_notes": repair_notes}
            ok1, verdict1, sha1, err1 = await verify_stage1(slug, is_book, dres["sha256"])
            if not ok1:
                return {"slug": slug, "state": "FAIL", "error": err1, "repair_notes": repair_notes}

        if verdict1 == "NO_DELTA":
            return {
                "slug": slug,
                "state": "DONE",
                "verdict": "NO_DELTA",
                "sha256": sha1,
                "repairs": repairs,
                "repair_notes": repair_notes,
            }

        # Stage 2: Translator (DELTA nodes only, up to 2 REOPEN_STAGE1 cycles)
        en_sha = sha1
        for round_idx in range(3):
            tres = await agent(
                prompt=build_translator_prompt(item, en_sha=en_sha, today=today),
                schema=TRANSLATOR_SCHEMA,
                role=f"Translator: {slug}",
                type_name=translator_type,
                workspace="inherit",
                model=agent_model,
            )
            if tres["status"] == "REOPEN_STAGE1":
                if round_idx >= 2:
                    return {
                        "slug": slug,
                        "state": "FAIL",
                        "error": f"Exceeded max REOPEN_STAGE1 cycles (t_items={tres.get('t_items')})",
                        "repair_notes": repair_notes,
                    }
                dres = await agent(
                    prompt=build_drafter_prompt(item, today=today, reopen_t_items=True),
                    schema=DRAFTER_SCHEMA,
                    role=f"Drafter Reopen: {slug}",
                    type_name=drafter_type,
                    workspace="inherit",
                    model=agent_model,
                )
                if dres["status"] == "FAIL":
                    return {"slug": slug, "state": "FAIL", "error": dres.get("note") or "Reopened Drafter returned FAIL", "repair_notes": repair_notes}
                if dres["status"] == "HOLD" or dres["verdict"] == "HOLD":
                    return {"slug": slug, "state": "HOLD", "note": dres.get("note", ""), "repair_notes": repair_notes}
                ok1, verdict1, en_sha_new, err1 = await verify_stage1(slug, is_book, dres["sha256"])
                if not ok1:
                    return {"slug": slug, "state": "FAIL", "error": f"Reopened Stage 1 failed: {err1}", "repair_notes": repair_notes}
                if verdict1 == "NO_DELTA":
                    return {
                        "slug": slug,
                        "state": "DONE",
                        "verdict": "NO_DELTA",
                        "sha256": en_sha_new,
                        "repairs": repairs,
                        "repair_notes": repair_notes,
                    }
                en_sha = en_sha_new
                continue

            if tres["status"] == "HOLD":
                return {"slug": slug, "state": "HOLD", "note": tres.get("note", ""), "repair_notes": repair_notes}
            if tres["status"] == "FAIL":
                return {"slug": slug, "state": "FAIL", "error": tres.get("note") or "Translator returned FAIL", "repair_notes": repair_notes}

            ok2, verdict2, zh_sha, err2 = await verify_stage2(slug, is_book, tres["sha256"])
            if not ok2:
                repairs += 1
                repair_notes.append(f"Stage 2 ({summarize_gate_error(err2)})")
                tres = await agent(
                    prompt=build_translator_prompt(item, en_sha=en_sha, today=today, repair_error=err2),
                    schema=TRANSLATOR_SCHEMA,
                    role=f"Translator Repair: {slug}",
                    type_name=translator_type,
                    workspace="inherit",
                    model=agent_model,
                )
                if tres["status"] == "HOLD":
                    return {"slug": slug, "state": "HOLD", "note": tres.get("note", ""), "repair_notes": repair_notes}
                if tres["status"] != "PASS":
                    return {
                        "slug": slug,
                        "state": "FAIL",
                        "error": f"Translator repair returned {tres['status']}: {tres.get('note', '')}",
                        "repair_notes": repair_notes,
                    }
                ok2, verdict2, zh_sha, err2 = await verify_stage2(slug, is_book, tres["sha256"])
                if not ok2:
                    return {"slug": slug, "state": "FAIL", "error": err2, "repair_notes": repair_notes}

            return {
                "slug": slug,
                "state": "DONE",
                "verdict": verdict2,
                "en_sha256": en_sha,
                "zh_sha256": zh_sha,
                "repairs": repairs,
                "repair_notes": repair_notes,
            }

        return {"slug": slug, "state": "FAIL", "error": "Unexpected Stage 2 loop exit"}


async def safe_run_node(
    item: dict[str, str],
    sem: asyncio.Semaphore,
    *,
    drafter_type: str,
    translator_type: str,
    agent_model: str,
) -> dict:
    try:
        return await run_node_pipeline(
            item,
            sem,
            drafter_type=drafter_type,
            translator_type=translator_type,
            agent_model=agent_model,
        )
    except Exception as exc:
        return {
            "slug": item["slug"],
            "state": "FAIL",
            "error": f"{type(exc).__name__}: {exc}",
        }


def mark_hold_in_wave(batch_num: int, hold_slugs: list[str]) -> None:
    if not hold_slugs:
        return
    wave_path = ROOT / "work" / "wave.md"
    if not wave_path.is_file():
        return
    lines = wave_path.read_text(encoding="utf-8").splitlines()
    hold_set = set(hold_slugs)
    in_batch = False
    batch_header = re.compile(rf"^##\s+Deep Sleep Batch {batch_num}\b")
    for idx, line in enumerate(lines):
        if batch_header.match(line):
            in_batch = True
            continue
        if in_batch and line.startswith("## "):
            break
        if in_batch:
            m = re.match(r"^-\s+\[\s\]\s+`([^`]+)`(.*)$", line)
            if m and m.group(1) in hold_set:
                lines[idx] = f"- [HOLD — awaiting Operator] `{m.group(1)}`{m.group(2)}"
    wave_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


async def verify_live_urls(delta_slugs: list[str]) -> list[str]:
    bad: list[str] = []
    for slug in delta_slugs:
        url = live_url_for(slug)
        code = "000"
        for attempt in range(8):
            proc = await run_cmd(
                ["curl", "-sS", "-L", "-o", "/dev/null", "-w", "%{http_code}", url]
            )
            code = proc.stdout.strip()
            if code == "200":
                break
            if attempt < 7:
                await asyncio.sleep(5)
        if code != "200":
            bad.append(f"{url} -> HTTP {code}")
    return bad


def is_in_stage3_scope(rel_path: str) -> bool:
    """Return True iff repo-relative POSIX path falls inside strict Stage 3 scope."""
    rel = str(rel_path).strip().replace("\\", "/")
    if not rel or rel.startswith("/"):
        return False
    parts = Path(rel).parts
    if any(part in ("", ".", "..") for part in parts):
        return False
    norm = os.path.normpath(rel).replace("\\", "/")
    if norm != rel:
        return False
    for entry in TRACKED_STAGE3_PATHS:
        if entry.endswith("/"):
            if rel.startswith(entry) and len(rel) > len(entry):
                return True
        elif rel == entry:
            return True
    return False


def parse_nul_paths(stdout: str) -> list[str]:
    """Parse NUL-delimited path output (e.g. `git diff --cached --name-only -z`)."""
    paths: list[str] = []
    seen: set[str] = set()
    for token in stdout.split("\0"):
        if token and token not in seen:
            seen.add(token)
            paths.append(token)
    return paths


async def list_staged_paths(*, root: Path = ROOT) -> list[str]:
    """Return sorted repo-relative paths currently staged in the git index."""
    proc = await run_cmd(
        ["git", "diff", "--cached", "--name-only", "-z"],
        cwd=root,
        check=True,
    )
    return sorted(parse_nul_paths(proc.stdout))


async def snapshot_dirty_paths(*, root: Path = ROOT) -> set[str]:
    """Return the set of repo-relative dirty/untracked paths from `git status --porcelain -z -uall`."""
    proc = await run_cmd(
        ["git", "status", "--porcelain", "-z", "-uall"],
        cwd=root,
        check=True,
    )
    return set(parse_porcelain_z_paths(proc.stdout))


async def prepare_stage3_git_snapshot(*, root: Path = ROOT) -> set[str]:
    """Fail closed if the git index has pre-staged entries, then snapshot working-tree dirty paths."""
    staged = await list_staged_paths(root=root)
    if staged:
        raise RuntimeError(
            "Refusing Stage 3 assembly with pre-staged git index entries: "
            + ", ".join(staged)
        )
    return await snapshot_dirty_paths(root=root)


def compute_stage3_paths(
    delta_slugs: list[str],
    pre_dirty: set[str],
    post_dirty: set[str],
    *,
    root: Path = ROOT,
) -> list[str]:
    """Compute exact sorted repo-relative paths belonging to this Stage 3 batch."""
    batch_targets = {
        target_path_for(slug, root=root)[1].relative_to(root).as_posix()
        for slug in delta_slugs
    } | {"docs/posts.graph.json"}
    out_of_scope_targets = sorted(p for p in batch_targets if not is_in_stage3_scope(p))
    if out_of_scope_targets:
        raise RuntimeError(
            "Stage 3 batch target(s) outside strict scope: "
            + ", ".join(out_of_scope_targets)
        )
    newly_dirty_in_scope = {
        p for p in (post_dirty - pre_dirty) if is_in_stage3_scope(p)
    }
    return sorted(p for p in (batch_targets | newly_dirty_in_scope) if p in post_dirty)


async def stage_stage3_paths(
    delta_slugs: list[str],
    pre_dirty: set[str],
    *,
    root: Path = ROOT,
) -> list[str]:
    """Stage strictly this batch's Stage 3 paths and assert exact cached-index parity."""
    post_dirty = await snapshot_dirty_paths(root=root)
    stage_paths = compute_stage3_paths(delta_slugs, pre_dirty, post_dirty, root=root)

    pre_add_staged = await list_staged_paths(root=root)
    if pre_add_staged:
        raise RuntimeError(
            "Refusing Stage 3 git add: index has unexpected staged entries: "
            + ", ".join(pre_add_staged)
        )
    if not stage_paths:
        return []

    await run_cmd(["git", "add", "--", *stage_paths], cwd=root, check=True)
    actual_staged = await list_staged_paths(root=root)
    out_of_scope = [p for p in actual_staged if not is_in_stage3_scope(p)]
    if actual_staged != stage_paths or out_of_scope:
        await run_cmd(["git", "reset", "--quiet", "--", *stage_paths], cwd=root, check=False)
        raise RuntimeError(
            f"Stage 3 staged index mismatch: expected={stage_paths}, "
            f"actual={actual_staged}, out_of_scope={out_of_scope}"
        )
    return stage_paths


async def run_batch_stage3(
    batch_num: int,
    completed_nodes: list[dict],
    hold_nodes: list[dict],
    failed_nodes: list[dict],
    *,
    recap_type: str,
    agent_model: str,
) -> dict:
    mark_hold_in_wave(batch_num, [r["slug"] for r in hold_nodes])
    problems: list[str] = []
    for r in failed_nodes:
        notes = r.get("repair_notes") or []
        prefix = f"[{'; '.join(notes)}] " if notes else ""
        problems.append(f"{r['slug']}: {prefix}{summarize_gate_error(r['error'])}")
    for r in hold_nodes:
        notes = r.get("repair_notes") or []
        if notes:
            problems.append(f"{r['slug']}: {'; '.join(notes)} before HOLD")
    for r in completed_nodes:
        if r.get("repairs", 0) > 0:
            notes = r.get("repair_notes") or []
            detail = "; ".join(notes) if notes else f"required {r['repairs']} Stage 1/2 repair pass(es)"
            problems.append(f"{r['slug']}: {detail}")

    completed_slugs = [r["slug"] for r in completed_nodes]
    commit_sha = "none"
    deploy_run_id: str | None = None
    delta_count = 0
    no_delta_count = 0
    remaining = None
    log_path = f"work/_logs/batch-{batch_num}.md"

    if completed_slugs:
        await run_cmd(["python3", "scripts/check-signoffs.py", *completed_slugs], check=True)
        delta_slugs = [r["slug"] for r in completed_nodes if r["verdict"] != "NO_DELTA"]
        if delta_slugs:
            pre_dirty = await prepare_stage3_git_snapshot(root=ROOT)
            await run_cmd(["python3", "scripts/interleave-post.py", *delta_slugs], check=True)
            essay_deltas = [s for s in delta_slugs if not s.startswith("_book:")]
            if essay_deltas:
                await run_cmd(["python3", "scripts/audit-post.py", *essay_deltas], check=True)
            await run_cmd(["python3", "scripts/audit-book.py"], check=True)
            await run_cmd(["node", "build.mjs"], check=True)
            await run_cmd(["node", "scripts/project-posts-graph.mjs"], check=True)

            stage_paths = await stage_stage3_paths(delta_slugs, pre_dirty, root=ROOT)
            if stage_paths:
                slug_summary = ", ".join(delta_slugs[:3])
                if len(delta_slugs) > 3:
                    slug_summary = f"refine {len(delta_slugs)} nodes ({slug_summary}, ...)"
                await run_cmd(
                    ["git", "commit", "-m", f"Consolidate Deep Sleep Batch {batch_num}: {slug_summary}"],
                    check=True,
                )
                commit_sha = (await run_cmd(["git", "rev-parse", "--short", "HEAD"], check=True)).stdout.strip()
                await run_cmd(["git", "push", "origin", "main"], check=True)
                watch = await run_cmd(["bash", "scripts/watch-deploy.sh"], check=True)
                rm = re.search(r"Watching GitHub Actions run (\d+)", watch.stdout)
                deploy_run_id = rm.group(1) if rm else "verified"
                bad_urls = await verify_live_urls(delta_slugs)
                if bad_urls:
                    problems.append(f"Live HTTP != 200 after deploy: {', '.join(bad_urls)}")

        rec_cmd = [
            "python3",
            "scripts/check-signoffs.py",
            "--record-batch",
            str(batch_num),
            "--commit",
            commit_sha,
        ]
        if deploy_run_id:
            rec_cmd.extend(["--deploy-run", deploy_run_id])
        if problems:
            rec_cmd.extend(["--problem", "; ".join(problems)])
        rec_cmd.extend(completed_slugs)
        rec = await run_cmd(rec_cmd, check=True)
        rm = RECORDED_RE.search(rec.stdout)
        if not rm:
            raise RuntimeError(f"Unable to parse --record-batch output: {rec.stdout!r}")
        delta_count = int(rm.group(2))
        no_delta_count = int(rm.group(3))
        remaining = int(rm.group(4))
        commit_sha = rm.group(5)
        log_path = rm.group(6)

    open_issues = 0
    recap_log = None
    protected_outer_anchors: list[str] = []
    guard_note: str | None = None
    if problems:
        recap_log = f"work/_logs/batch-{batch_num}-recap.md"
        protected_prefix_before = snapshot_protected_prefixes()
        recap_res = await agent(
            prompt=(
                f"Batch {batch_num} `/recap` in `{ROOT}` per `docs/charters/recap.md` and `docs/wave-refinement-plan.md` §4.5.\n"
                f"- Confirmed problem(s): {'; '.join(problems)}\n"
                f"- Inspect `{log_path}` (if present) and affected `work/<slug>/` directories strictly on a need-to-know basis against `/Users/jingliang/.gemini/config/plugins/ontological-clarity/skills/ontological-clarity/SKILL.md`.\n"
                f"- Write the concise report, sha256 table of any modified files, open_issues count, and `RECAP: confirmed (log: {recap_log}, files: <N>, date: {datetime.now().strftime('%Y-%m-%d')})` to `{recap_log}`.\n"
                "- Do NOT run `git commit` or `git push` (the workflow commits verified tracked files).\n"
                "**Mandatory completion rule:** Call `finish` matching the schema (`status`: `\"PASS\"` or `\"OPEN_ISSUES\"`, `open_issues`, `log`, `modified_files`, `summary`). Do NOT call `send_message`."
            ),
            schema=RECAP_SCHEMA,
            role=f"Recap: Batch {batch_num}",
            type_name=recap_type,
            workspace="inherit",
            model=agent_model,
        )
        open_issues, protected_outer_anchors, guard_note = await finalize_batch_recap(
            batch_num,
            recap_res,
            log_path=log_path,
            recap_log=recap_log,
            prefix_snapshot_before=protected_prefix_before,
        )

    if open_issues == 0:
        for slug in completed_slugs:
            shutil.rmtree(ROOT / "work" / slug, ignore_errors=True)

    return {
        "batch": batch_num,
        "delta": delta_count,
        "no_delta": no_delta_count,
        "hold": len(hold_nodes),
        "failed": len(failed_nodes),
        "open_issues": open_issues,
        "remaining": remaining,
        "commit": commit_sha,
        "log": log_path,
        "recap_log": recap_log,
        "protected_outer_anchors": protected_outer_anchors,
        "guard_note": guard_note,
        "hold_nodes": hold_nodes,
        "failed_nodes": failed_nodes,
    }


async def main() -> dict:
    batch_size = int(args.get("batch_size", 12))
    concurrency_override = args.get("concurrency")
    part_filter = args.get("part")
    max_batches = int(args.get("max_batches", 0))
    drafter_type = args["drafter_type"]
    translator_type = args["translator_type"]
    recap_type = args["recap_type"]
    agent_model = args.get("model", "inherit")

    batches_summary: list[dict] = []
    batches_run = 0
    stop_reason = "DONE"

    while True:
        if max_batches > 0 and batches_run >= max_batches:
            stop_reason = "MAX_BATCHES_REACHED"
            break
        if (ROOT / "work" / "_wake" / "interrupt").exists():
            stop_reason = "PAUSED_FOR_WAKE"
            break
        mismatches = check_charter_hashes(drafter_type, translator_type, recap_type)
        if mismatches:
            stop_reason = f"CHARTER_CHANGED:{mismatches}"
            break

        batch = await select_next_batch(batch_size, part_filter)
        batch_num = batch["batch_num"]
        items = batch["items"]
        if batch["count"] == 0 or not items:
            stop_reason = "DONE"
            break

        w = (
            max(1, int(concurrency_override))
            if concurrency_override is not None and str(concurrency_override).strip() != ""
            else max(1, batch["concurrency"])
        )
        phase(f"Batch {batch_num} ({batch['count']} nodes, W={w}, rem_after={batch['remaining_after']})")
        sem = asyncio.Semaphore(w)
        node_results = await parallel(
            items,
            lambda it: safe_run_node(
                it,
                sem,
                drafter_type=drafter_type,
                translator_type=translator_type,
                agent_model=agent_model,
            ),
        )

        completed_nodes = [r for r in node_results if r["state"] == "DONE"]
        hold_nodes = [r for r in node_results if r["state"] == "HOLD"]
        failed_nodes = [r for r in node_results if r["state"] == "FAIL"]
        skipped_nodes = [r for r in node_results if r["state"] == "SKIPPED_FOR_WAKE"]

        s3 = await run_batch_stage3(
            batch_num,
            completed_nodes,
            hold_nodes,
            failed_nodes,
            recap_type=recap_type,
            agent_model=agent_model,
        )
        batches_summary.append(s3)
        batches_run += 1

        batch_status = (
            "OPEN_ISSUES" if s3.get("protected_outer_anchors")
            else "HOLD" if hold_nodes
            else "OPEN_ISSUES" if s3["open_issues"] > 0
            else "FAIL" if failed_nodes
            else "PAUSED_FOR_WAKE" if skipped_nodes
            else "PASS"
        )
        rem_display = s3["remaining"] if s3["remaining"] is not None else batch["remaining_after"]
        log(
            f"Batch {batch_num}: {batch_status} (delta={s3['delta']}, no_delta={s3['no_delta']}, "
            f"hold={s3['hold']}, failed={s3['failed']}, open_issues={s3['open_issues']}, "
            f"remaining={rem_display}, commit={s3['commit']})"
        )

        if s3.get("protected_outer_anchors"):
            stop_reason = "OPEN_ISSUES"
            break
        if hold_nodes:
            stop_reason = "HOLD"
            break
        if s3["open_issues"] > 0:
            stop_reason = "OPEN_ISSUES"
            break
        if failed_nodes:
            stop_reason = "NODE_FAILURE"
            break
        if skipped_nodes or (ROOT / "work" / "_wake" / "interrupt").exists():
            stop_reason = "PAUSED_FOR_WAKE"
            break

    return {
        "stop_reason": stop_reason,
        "batches_run": batches_run,
        "batches": batches_summary,
    }


result = await main()
print(json.dumps(result, indent=2))
