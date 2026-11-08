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
  4. Every backtick `path:line` / `slug:line` locator in `work/<slug>/notes.md`
     (when present) resolves to an existing file whose line count covers the cited
     line numbers. Can also be run standalone on any notes file via `--locators`.
  5. For `NO_DELTA` nodes (no `work/<slug>/en.md`), verifies `CRITIC: confirmed_no_delta`
     in `work/<slug>/debate-en.md` against `sha256(content/posts/<slug>.md)` (or
     `content/book/<name>.md`) and verifies `work/<slug>/notes.md` locators.
  6. With `--record-batch <m> --commit <sha> <slug1> ...`, deterministically updates
     `work/wave.md` checkboxes, prunes completed items and appends `DELTA (propagates)`
     and `### For work/todo.md` items in `work/todo.md`, and writes `work/_logs/batch-<m>.md`.
  7. With `--clean-sleep [--dry-run]`, deterministically harvests any unrecorded
     `### For work/todo.md` items from the directories to be deleted into `work/todo.md`
     and deletes ONLY the completed `[x]` `/sleep` node and sweep directories recorded
     in `work/wave.md` (`_plan-consolidation`, `_reverse-link-sweep`, `_post-wave-sweep`,
     `_logs`, and `[x]` node slugs in `work/wave.md` whose post exists in
     `content/posts/<slug>.md` and that have no pending `work/_wake/<slug>/handoff.md`),
     explicitly preserving `work/_wake/`, `work/plan/`, and any concurrent `/first-draft`
     or `/scout` handoff directory.

Usage:
  python3 scripts/check-signoffs.py <slug> [<slug2> ...]
  python3 scripts/check-signoffs.py --locators <notes.md> [<notes2.md> ...]
  python3 scripts/check-signoffs.py --record-batch <m> --commit <sha> [--deploy-run <id>] [--problem <note>] <slug1> [<slug2> ...]
  python3 scripts/check-signoffs.py --clean-sleep [--dry-run]
"""

from __future__ import annotations

import hashlib
import pathlib
import re
import shutil
import sys


ROOT = pathlib.Path(__file__).resolve().parent.parent
HEX64 = r"([0-9a-f]{64})"
LOCATOR_RE = re.compile(
    r"`([A-Za-z0-9_./-]+:(?:\d+(?:\s*[-–]\s*\d+)?)(?:\s*,\s*\d+(?:\s*[-–]\s*\d+)?)*)`"
)
BARE_LOCATOR_RE = re.compile(
    r"^([A-Za-z0-9_./-]+:(?:\d+(?:\s*[-–]\s*\d+)?)(?:\s*,\s*\d+(?:\s*[-–]\s*\d+)?)*)$"
)
VERDICT_LINE_RE = re.compile(
    r"^VERDICT:\s*(DELTA\s*\(\s*(?:terminal|propagates)\s*\)|NO_DELTA)\s*\|\s*RESTATERS:\s*([^\n]+)$",
    flags=re.MULTILINE,
)
SUMMARY_LINE_RE = re.compile(
    r"^SUMMARY:\s*(.+)$",
    flags=re.MULTILINE,
)


def sha256_file(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_single_locator(
    tok: str,
    label: str,
    source_label: str,
    base_dir: pathlib.Path | None = None,
    line_count_cache: dict[pathlib.Path, int] | None = None,
) -> list[str]:
    errors: list[str] = []
    if ":" not in tok:
        return [f"[{label}] Invalid locator `{tok}` in {source_label} (expected slug:line)"]
    head, tail = tok.split(":", 1)
    cand = ROOT / head
    if not cand.is_file() and base_dir is not None:
        cand = base_dir / head
    if not cand.is_file():
        slug = head.removesuffix(".md")
        cand = ROOT / "content" / "posts" / f"{slug}.md"
    if not cand.is_file():
        return [f"[{label}] Unresolved locator `{tok}` in {source_label} (file not found)"]
    resolved = cand.resolve()
    if line_count_cache is not None:
        if resolved not in line_count_cache:
            line_count_cache[resolved] = len(resolved.read_text(encoding="utf-8").split("\n"))
        max_line = line_count_cache[resolved]
    else:
        max_line = len(resolved.read_text(encoding="utf-8").split("\n"))
    nums = [int(n) for n in re.findall(r"\d+", tail)]
    if not nums:
        return [f"[{label}] Locator `{tok}` in {source_label} has no line numbers"]
    bad = [n for n in nums if n < 1 or n > max_line]
    if bad:
        errors.append(
            f"[{label}] Locator `{tok}` in {source_label} exceeds file length (line {bad[0]} > {max_line})"
        )
    return errors


def check_locators(notes_path: pathlib.Path, label: str) -> list[str]:
    if not notes_path.is_file():
        return [f"[{label}] Missing {notes_path}"]
    errors: list[str] = []
    text = notes_path.read_text(encoding="utf-8")
    line_count_cache: dict[pathlib.Path, int] = {}
    for tok in LOCATOR_RE.findall(text):
        errors.extend(
            validate_single_locator(
                tok,
                label,
                notes_path.name,
                base_dir=notes_path.parent,
                line_count_cache=line_count_cache,
            )
        )
    return errors


def parse_critic_verdict_and_summary(
    slug: str,
    deb_en: str,
    is_no_delta: bool,
    require_lines: bool = False,
) -> tuple[str, list[tuple[str, bool]], str, list[str]]:
    """
    Deterministically parses the Critic's `VERDICT: ... | RESTATERS: ...` and `SUMMARY: ...`
    lines from `work/<slug>/debate-en.md`.
    Returns (verdict, restaters_with_new_claim_flag, summary, errors).
    """
    errors: list[str] = []
    m_verdict = last_match(VERDICT_LINE_RE.pattern, deb_en)
    m_summary = last_match(SUMMARY_LINE_RE.pattern, deb_en)

    restaters: list[tuple[str, bool]] = []
    if m_verdict:
        raw_v = re.sub(r"\s+", " ", m_verdict.group(1).strip())
        raw_v = raw_v.replace("( ", "(").replace(" )", ")")
        if is_no_delta and raw_v != "NO_DELTA":
            errors.append(
                f"[{slug}] VERDICT line '{raw_v}' in debate-en.md contradicts CRITIC: confirmed_no_delta"
            )
        elif not is_no_delta and raw_v == "NO_DELTA":
            errors.append(
                f"[{slug}] VERDICT line 'NO_DELTA' in debate-en.md contradicts CRITIC: confirmed"
            )
        verdict = raw_v

        restaters_field = m_verdict.group(2).strip()
        if restaters_field.lower() not in ("none", "`none`"):
            if verdict != "DELTA (propagates)":
                errors.append(
                    f"[{slug}] RESTATERS must be 'none' when VERDICT is {verdict} (got '{restaters_field}')"
                )
            else:
                line_count_cache: dict[pathlib.Path, int] = {}
                # Split by semicolon or comma outside line-number lists, or extract locator tokens
                tokens = re.findall(
                    r"`?([a-z0-9][a-z0-9-]*:(?:\d+(?:\s*[-–]\s*\d+)?)(?:\s*,\s*\d+(?:\s*[-–]\s*\d+)?)*)`?(\s*\(\s*new_claim\s*\))?",
                    restaters_field,
                )
                if not tokens:
                    errors.append(
                        f"[{slug}] Could not parse RESTATERS field '{restaters_field}' in debate-en.md "
                        "(expected 'none' or '<slug>:<line>[, <slug2>:<line>...]')"
                    )
                for loc_tok, new_claim_group in tokens:
                    loc_clean = re.sub(r"\s+", "", loc_tok)
                    r_slug = loc_clean.split(":", 1)[0].removesuffix(".md")
                    if r_slug == slug:
                        errors.append(
                            f"[{slug}] Self-locator `{loc_clean}` listed in RESTATERS in debate-en.md"
                        )
                        continue
                    loc_errs = validate_single_locator(
                        loc_clean,
                        slug,
                        "debate-en.md (RESTATERS)",
                        line_count_cache=line_count_cache,
                    )
                    if loc_errs:
                        errors.extend(loc_errs)
                    else:
                        is_new_claim = bool(new_claim_group)
                        if all(existing_loc != loc_clean for existing_loc, _ in restaters):
                            restaters.append((loc_clean, is_new_claim))
    else:
        verdict = "NO_DELTA" if is_no_delta else "DELTA (terminal)"
        if require_lines:
            errors.append(
                f"[{slug}] Missing 'VERDICT: <DELTA (terminal)|DELTA (propagates)|NO_DELTA> | RESTATERS: <...|none>' line in debate-en.md"
            )

    if m_summary:
        summary = m_summary.group(1).strip().replace("|", "\\|")
        if not summary:
            errors.append(f"[{slug}] Empty 'SUMMARY:' line in debate-en.md")
    else:
        summary = verdict
        if require_lines:
            errors.append(f"[{slug}] Missing 'SUMMARY: <1-line summary>' line in debate-en.md")

    return (verdict, restaters, summary, errors)


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


def classify_node(
    slug: str,
    require_verdict_summary: bool = False,
) -> tuple[str, str, str, list[tuple[str, bool]], str, list[str]]:
    """
    Returns (verdict, en_or_post_sha, zh_sha, restaters, summary, errors) where verdict is one of:
      'NO_DELTA', 'DELTA (terminal)', 'DELTA (propagates)'
    """
    errors: list[str] = []
    work_dir = ROOT / "work" / slug
    en_path = work_dir / "en.md"
    zh_path = work_dir / "zh.md"
    deb_en_path = work_dir / "debate-en.md"
    deb_zh_path = work_dir / "debate-zh.md"
    notes_path = work_dir / "notes.md"

    if not deb_en_path.is_file():
        return ("UNKNOWN", "", "", [], "", [f"[{slug}] Missing {deb_en_path.relative_to(ROOT)}"])

    deb_en = deb_en_path.read_text(encoding="utf-8")

    # Check if this is a NO_DELTA node (no work/<slug>/en.md and confirmed_no_delta at end of debate-en.md)
    no_delta_body = r"CRITIC:\s*confirmed_no_delta\b[^\n]*?" + HEX64
    m_no_delta = last_match(r"^" + no_delta_body, deb_en)
    if m_no_delta and not en_path.is_file():
        if slug.startswith("_book:"):
            post_or_book = ROOT / "content" / "book" / f"{slug[6:]}.md"
        else:
            post_or_book = ROOT / "content" / "posts" / f"{slug}.md"
        # P6: Only fall back to notes.md when no post or book file exists (Node 0 and sweeps)
        target_path = post_or_book if post_or_book.is_file() else notes_path
        if not target_path.is_file():
            errors.append(f"[{slug}] Missing target file for confirmed_no_delta")
            return ("NO_DELTA", "", "", [], "NO_DELTA", errors)
        expected_sha = sha256_file(target_path)
        if m_no_delta.group(1) != expected_sha:
            errors.append(
                f"[{slug}] CRITIC confirmed_no_delta sha256 ({m_no_delta.group(1)[:12]}...) "
                f"!= {target_path.name} ({expected_sha[:12]}...)"
            )
        if notes_path.is_file():
            errors.extend(check_locators(notes_path, slug))
        else:
            errors.append(f"[{slug}] Missing work/{slug}/notes.md for NO_DELTA node")
        verdict, restaters, summary, v_errs = parse_critic_verdict_and_summary(
            slug, deb_en, is_no_delta=True, require_lines=require_verdict_summary
        )
        errors.extend(v_errs)
        return (verdict, expected_sha, "", restaters, summary, errors)

    for p in (en_path, zh_path, deb_en_path, deb_zh_path):
        if not p.is_file():
            errors.append(f"[{slug}] Missing {p.relative_to(ROOT)}")
    if errors:
        return ("DELTA (terminal)", "", "", [], "DELTA (terminal)", errors)

    en_sha = sha256_file(en_path)
    zh_sha = sha256_file(zh_path)
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

    if notes_path.is_file():
        errors.extend(check_locators(notes_path, slug))

    verdict, restaters, summary, v_errs = parse_critic_verdict_and_summary(
        slug, deb_en, is_no_delta=False, require_lines=require_verdict_summary
    )
    errors.extend(v_errs)
    return (verdict, en_sha, zh_sha, restaters, summary, errors)


def check_slug(slug: str) -> list[str]:
    _, _, _, _, _, errors = classify_node(slug)
    return errors


def extract_todo_blocks(slug: str) -> list[str]:
    work_dir = ROOT / "work" / slug
    items: list[str] = []
    heading_re = re.compile(r"^#{2,4}\s+For\s+`?work/todo\.md`?\b[^\n]*$", flags=re.IGNORECASE | re.MULTILINE)
    stop_re = re.compile(
        r"\n(?:#{1,4}\s+|(?:VERDICT|SUMMARY|CRITIC|STYLIST|HANDOFF_CONFIRMED):|---+\s*$)",
        flags=re.MULTILINE,
    )
    for fname in ("notes.md", "debate-en.md", "debate-zh.md"):
        fpath = work_dir / fname
        if not fpath.is_file():
            continue
        text = fpath.read_text(encoding="utf-8")
        for m in heading_re.finditer(text):
            tail = text[m.end() :]
            next_stop = stop_re.search(tail)
            block = tail[: next_stop.start()] if next_stop else tail
            for raw_line in block.splitlines():
                line = raw_line.strip()
                if not line or line.lower() in ("none", "none.", "- none", "- (none)", "(none)", "n/a", "- n/a"):
                    continue
                if re.match(r"^-\s*\(?none\)?\.?$", line, flags=re.IGNORECASE):
                    continue
                if re.match(r"^(?:VERDICT|SUMMARY|CRITIC|STYLIST|HANDOFF_CONFIRMED):", line):
                    continue
                if not line.startswith("- "):
                    line = f"- {line}"
                if line not in items:
                    items.append(line)
    return items


def compute_remaining_unvisited() -> int:
    wave_path = ROOT / "work" / "wave.md"
    visited: set[str] = set()
    if wave_path.is_file():
        for m in re.finditer(r"^-\s+(?:\[[^\]]*\]\s+)?`([^`]+)`", wave_path.read_text(encoding="utf-8"), flags=re.MULTILINE):
            visited.add(m.group(1).strip())
    all_posts = {
        p.stem
        for p in (ROOT / "content" / "posts").glob("*.md")
        if p.name != "README.md"
    }
    book_surfaces = {
        f"_book:{p.stem}"
        for p in (ROOT / "content" / "book").glob("*.md")
    }
    unvisited_posts = len(all_posts - visited)
    unvisited_book = len(book_surfaces - visited)
    return unvisited_posts + unvisited_book


def record_batch(
    batch_num: int,
    commit_sha: str,
    deploy_run: str,
    problem_note: str,
    slugs: list[str],
) -> int:
    all_errors: list[str] = []
    node_records: list[tuple[str, str, str, str, list[tuple[str, bool]], str]] = []
    for slug in slugs:
        verdict, en_sha, zh_sha, restaters, summary, errs = classify_node(
            slug, require_verdict_summary=True
        )
        if errs:
            all_errors.extend(errs)
        node_records.append((slug, verdict, en_sha, zh_sha, restaters, summary))

    if all_errors:
        for e in all_errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1

    short_sha = commit_sha[:8] if commit_sha and commit_sha != "none" else "none"
    delta_count = sum(1 for _, v, _, _, _, _ in node_records if v.startswith("DELTA"))
    no_delta_count = sum(1 for _, v, _, _, _, _ in node_records if v == "NO_DELTA")
    delta_slugs_in_batch = {s for s, v, _, _, _, _ in node_records if v.startswith("DELTA")}

    # 1. Update work/wave.md checkboxes
    wave_path = ROOT / "work" / "wave.md"
    if wave_path.is_file():
        wave_text = wave_path.read_text(encoding="utf-8")
        for slug, verdict, _, _, _, _ in node_records:
            tag = "NO_DELTA" if verdict == "NO_DELTA" else f"DELTA {short_sha}"
            pattern = rf"^-\s+\[[ xX]\]\s+`{re.escape(slug)}`[^\n]*$"
            replacement = f"- [x] `{slug}` ({tag})"
            if re.search(pattern, wave_text, flags=re.MULTILINE):
                wave_text = re.sub(pattern, replacement, wave_text, flags=re.MULTILINE)
            else:
                wave_text = wave_text.rstrip() + f"\n{replacement}\n"
        wave_path.write_text(wave_text, encoding="utf-8")

    # 2. Update work/todo.md: prune completed [x] items, strike evaluated post-evaluation slugs per slug, and append new items
    todo_path = ROOT / "work" / "todo.md"
    batch_slug_set = set(slugs)
    todo_trigger_by_slug: dict[str, str] = {}
    kept_todo_lines: list[str] = []
    if todo_path.is_file():
        existing_todo_text = todo_path.read_text(encoding="utf-8")
        for line in existing_todo_text.splitlines():
            if re.match(r"^-\s+\[[xX]\]\s+", line):
                continue
            if re.match(r"^-\s+\[\s\]\s+", line) and "Evaluate fresh in `/deep-sleep`" in line and "(`_book:" not in line:
                head_part, eval_part = line.split("Evaluate fresh in `/deep-sleep`", 1)
                colon_idx = eval_part.find(":")
                if colon_idx != -1:
                    prefix_with_colon = head_part + "Evaluate fresh in `/deep-sleep`" + eval_part[: colon_idx + 1]
                    targets_tail = eval_part[colon_idx + 1 :]
                    entry_matches = [
                        m
                        for m in re.finditer(r"`([a-z0-9][a-z0-9-]*)`(?:\s*\([^)]*\))?", targets_tail)
                        if (ROOT / "content" / "posts" / f"{m.group(1)}.md").is_file()
                    ]
                    for m in entry_matches:
                        todo_trigger_by_slug[m.group(1)] = line
                    if entry_matches:
                        remaining_entries = [
                            m.group(0) for m in entry_matches if m.group(1) not in batch_slug_set
                        ]
                        if not remaining_entries:
                            continue
                        if len(remaining_entries) < len(entry_matches):
                            kept_todo_lines.append(
                                f"{prefix_with_colon} {', '.join(remaining_entries)}."
                            )
                            continue
            kept_todo_lines.append(line)

    new_todo_lines: list[str] = []
    for slug, verdict, _, _, restaters, summary in node_records:
        if verdict == "DELTA (propagates)" and restaters:
            # P2(b): Apply same-batch co-movement exception
            queued_restaters: list[str] = []
            for loc, is_new_claim in restaters:
                r_slug = loc.split(":", 1)[0].removesuffix(".md")
                if (
                    r_slug in delta_slugs_in_batch
                    and slug in todo_trigger_by_slug
                    and todo_trigger_by_slug.get(r_slug) == todo_trigger_by_slug.get(slug)
                    and not is_new_claim
                ):
                    continue
                queued_restaters.append(loc)
            if queued_restaters:
                restater_str = " and ".join(
                    f"`{r.split(':', 1)[0]}` (`{r}`, Critic-verified `links_in` restater)"
                    for r in queued_restaters
                )
                prop_line = (
                    f"- [ ] **`{slug}@{short_sha}` restating neighbor(s) (`/deep-sleep` Batch {batch_num} "
                    f"`DELTA (propagates)`)**: {summary} Evaluate fresh in `/deep-sleep` "
                    f"(with `{slug}@{short_sha}` as related material): {restater_str}."
                )
                if prop_line not in kept_todo_lines and prop_line not in new_todo_lines:
                    new_todo_lines.append(prop_line)
        for item in extract_todo_blocks(slug):
            if item not in kept_todo_lines and item not in new_todo_lines:
                new_todo_lines.append(item)

    while kept_todo_lines and not kept_todo_lines[-1].strip():
        kept_todo_lines.pop()
    updated_todo = "\n".join(kept_todo_lines + new_todo_lines) + "\n"
    todo_path.write_text(updated_todo, encoding="utf-8")

    # 3. Write work/_logs/batch-<m>.md
    logs_dir = ROOT / "work" / "_logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = logs_dir / f"batch-{batch_num}.md"
    rem = compute_remaining_unvisited()

    table_rows: list[str] = []
    for slug, verdict, en_sha, zh_sha, _, summary in node_records:
        s1_info = f"`CONFIRMED_NO_DELTA` (`{en_sha[:8]}…`)" if verdict == "NO_DELTA" else f"`CONFIRMED` (`{en_sha[:8]}…`)"
        s2_info = "—" if verdict == "NO_DELTA" else f"`CONFIRMED` (`{zh_sha[:8]}…`)"
        v_cell = "`NO_DELTA`" if verdict == "NO_DELTA" else f"`{verdict}` (`{short_sha}`)"
        table_rows.append(f"| `{slug}` | {v_cell} | {s1_info} | {s2_info} | {summary} |")

    log_lines = [
        f"# Deep Sleep Batch {batch_num} Execution Log (`work/_logs/batch-{batch_num}.md`)",
        "",
        f"- **Batch**: `{batch_num}` (`count = {len(slugs)}`, `delta = {delta_count}`, `no_delta = {no_delta_count}`)",
        f"- **Commit**: `{short_sha}`",
        f"- **CI Deploy**: `{deploy_run or 'verified'}`",
        f"- **Remaining Unvisited Corpus Nodes**: `{rem}`",
        "",
        "## Node Execution Table",
        "",
        "| Node (`slug`) | Verdict | Stage 1 (`drafter` ⇄ `critic`) | Stage 2 (`translator` ⇄ `stylist`) | 1-Line Summary |",
        "| :--- | :--- | :--- | :--- | :--- |",
        *table_rows,
        "",
        "## Stage 3 Verification & Confirmed Problems / Surprises",
        "",
        f"- Sign-offs verified via `python3 scripts/check-signoffs.py`: `{len(slugs)}/{len(slugs)}`.",
        f"- Confirmed channel/process problems or surprises: {problem_note or 'none'}.",
        "",
    ]
    log_path.write_text("\n".join(log_lines), encoding="utf-8")

    print(
        f"BATCH_RECORDED: batch={batch_num} delta={delta_count} no_delta={no_delta_count} "
        f"remaining={rem} commit={short_sha} log=work/_logs/batch-{batch_num}.md"
    )
    return 0


def clean_sleep(dry_run: bool = False) -> int:
    wave_path = ROOT / "work" / "wave.md"
    if not wave_path.is_file():
        print("ERROR: work/wave.md not found", file=sys.stderr)
        return 1

    wave_text = wave_path.read_text(encoding="utf-8")
    special_sweeps = ("_plan-consolidation", "_reverse-link-sweep", "_post-wave-sweep")
    checked_specials: list[str] = []
    checked_slugs: list[str] = []

    for m in re.finditer(r"^-\s+\[[xX]\]\s+(.+)$", wave_text, flags=re.MULTILINE):
        tail = m.group(1)
        matched_special = False
        for sp in special_sweeps:
            if sp in tail:
                if sp not in checked_specials:
                    checked_specials.append(sp)
                matched_special = True
        if matched_special:
            continue
        m_slug = re.match(r"^`([a-z0-9][a-z0-9-]*)`", tail.strip())
        if m_slug:
            slug = m_slug.group(1)
            if slug not in checked_slugs:
                checked_slugs.append(slug)

    work_root = ROOT / "work"
    eligible_names: list[str] = []
    skipped_wave_slugs: list[str] = []

    for sp in checked_specials:
        eligible_names.append(sp)

    for slug in checked_slugs:
        post_exists = (ROOT / "content" / "posts" / f"{slug}.md").is_file()
        handoff_exists = (work_root / "_wake" / slug / "handoff.md").exists()
        if post_exists and not handoff_exists:
            eligible_names.append(slug)
            for layer_dir in sorted(work_root.glob(f"_l*-{slug}")):
                if layer_dir.is_dir() and layer_dir.name not in eligible_names:
                    eligible_names.append(layer_dir.name)
        else:
            skipped_wave_slugs.append(slug)

    if "_logs" not in eligible_names:
        eligible_names.append("_logs")

    protected_names = {"_wake", "plan"}
    dirs_to_delete: list[pathlib.Path] = []
    for name in eligible_names:
        if name in protected_names:
            continue
        if not name.startswith("_"):
            if not (ROOT / "content" / "posts" / f"{name}.md").is_file():
                continue
            if (work_root / "_wake" / name / "handoff.md").exists():
                continue
        cand = work_root / name
        if cand.is_dir() and not cand.is_symlink():
            dirs_to_delete.append(cand)

    delete_set = {d.resolve() for d in dirs_to_delete}
    preserved_dirs: list[pathlib.Path] = []
    if work_root.is_dir():
        for entry in sorted(work_root.iterdir()):
            if entry.is_dir() and not entry.is_symlink():
                if entry.resolve() not in delete_set:
                    preserved_dirs.append(entry)

    del_rel = [str(d.relative_to(ROOT)) for d in dirs_to_delete]
    pres_rel = [str(d.relative_to(ROOT)) for d in preserved_dirs]

    todo_path = ROOT / "work" / "todo.md"
    kept_todo_lines: list[str] = []
    if todo_path.is_file():
        kept_todo_lines = todo_path.read_text(encoding="utf-8").splitlines()
    new_todo_lines: list[str] = []
    for d in dirs_to_delete:
        for item in extract_todo_blocks(d.name):
            if item not in kept_todo_lines and item not in new_todo_lines:
                new_todo_lines.append(item)

    if dry_run:
        print(
            f"CLEAN_SLEEP_DRY_RUN: wave_checked_nodes={len(checked_slugs)} "
            f"wave_checked_sweeps={len(checked_specials)} "
            f"existing_to_delete={len(dirs_to_delete)} "
            f"preserved={len(preserved_dirs)} "
            f"todo_to_harvest={len(new_todo_lines)}"
        )
        print(f"WOULD_DELETE: {', '.join(del_rel) if del_rel else 'none'}")
        print(f"PRESERVED: {', '.join(pres_rel) if pres_rel else 'none'}")
        if new_todo_lines:
            print("WOULD_HARVEST_TODO:")
            for item in new_todo_lines:
                print(f"  {item}")
        else:
            print("WOULD_HARVEST_TODO: none")
        if skipped_wave_slugs:
            print(f"SKIPPED_WAVE_SLUGS: {', '.join(skipped_wave_slugs)}")
        return 0

    if new_todo_lines:
        while kept_todo_lines and not kept_todo_lines[-1].strip():
            kept_todo_lines.pop()
        updated_todo = "\n".join(kept_todo_lines + new_todo_lines) + "\n"
        todo_path.write_text(updated_todo, encoding="utf-8")

    for d in dirs_to_delete:
        shutil.rmtree(d)

    print(
        f"CLEAN_SLEEP_DONE: deleted={len(dirs_to_delete)} "
        f"preserved={len(preserved_dirs)} "
        f"todo_harvested={len(new_todo_lines)} "
        f"deleted_dirs=[{', '.join(del_rel)}] "
        f"preserved_dirs=[{', '.join(pres_rel)}]"
    )
    return 0


def main(argv: list[str]) -> int:
    if "--clean-sleep" in argv[1:]:
        dry_run = "--dry-run" in argv[1:]
        extra = [a for a in argv[1:] if a not in ("--clean-sleep", "--dry-run")]
        if extra:
            print("Usage: python3 scripts/check-signoffs.py --clean-sleep [--dry-run]", file=sys.stderr)
            return 2
        return clean_sleep(dry_run=dry_run)

    if "--locators" in argv[1:]:
        targets = [arg for arg in argv[1:] if arg != "--locators"]
        if not targets:
            print("Usage: python3 scripts/check-signoffs.py --locators <notes.md> [<notes2.md> ...]", file=sys.stderr)
            return 2
        all_errors: list[str] = []
        for raw in targets:
            p = pathlib.Path(raw)
            if not p.is_file() and (ROOT / "work" / raw.removesuffix(".md") / "notes.md").is_file():
                p = ROOT / "work" / raw.removesuffix(".md") / "notes.md"
            label = p.parent.name if p.name == "notes.md" else str(p)
            errs = check_locators(p, label)
            if errs:
                all_errors.extend(errs)
            else:
                print(f"Locators verified: {p.relative_to(ROOT) if p.is_relative_to(ROOT) else p}")
        if all_errors:
            for e in all_errors:
                print(f"ERROR: {e}", file=sys.stderr)
            return 1
        return 0

    if "--record-batch" in argv[1:]:
        batch_num = 0
        commit_sha = "none"
        deploy_run = "verified"
        problem_note = "none"
        slugs: list[str] = []
        i = 1
        while i < len(argv):
            arg = argv[i]
            if arg == "--record-batch" and i + 1 < len(argv):
                batch_num = int(argv[i + 1])
                i += 2
            elif arg == "--commit" and i + 1 < len(argv):
                commit_sha = argv[i + 1]
                i += 2
            elif arg == "--deploy-run" and i + 1 < len(argv):
                deploy_run = argv[i + 1]
                i += 2
            elif arg == "--problem" and i + 1 < len(argv):
                problem_note = argv[i + 1]
                i += 2
            elif not arg.startswith("-"):
                slugs.append(arg.removesuffix(".md"))
                i += 1
            else:
                i += 1
        if batch_num <= 0 or not slugs:
            print(
                "Usage: python3 scripts/check-signoffs.py --record-batch <m> --commit <sha> [--deploy-run <id>] [--problem <note>] <slug1> [<slug2> ...]",
                file=sys.stderr,
            )
            return 2
        return record_batch(batch_num, commit_sha, deploy_run, problem_note, slugs)

    slugs = [arg.removesuffix(".md") for arg in argv[1:] if not arg.startswith("-")]
    if not slugs:
        print("Usage: python3 scripts/check-signoffs.py <slug> [<slug2> ...]", file=sys.stderr)
        return 2

    all_errors = []
    for slug in slugs:
        verdict, _, _, _, _, errs = classify_node(slug)
        if errs:
            all_errors.extend(errs)
        else:
            print(f"Sign-offs verified: work/{slug}/ (verdict={verdict})")

    if all_errors:
        for e in all_errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
