#!/usr/bin/env python3
"""
Deterministic Stage 1 / Stage 3 sign-off and sha256 handoff verifier (`scripts/check-signoffs.py`).

Checks for each `work/<slug>/` node:
  1. Stage 1 (`--stage1 <slug>`): `work/<slug>/notes.md` records `VERDICT:`, `SUMMARY:`,
     and `DRAFTER: confirmed` (with valid 64-hex `sha256` matching `work/<slug>/en.md`,
     or `draft.md` for `_plan-consolidation`) or `DRAFTER: confirmed_no_delta` (with valid
     64-hex `sha256` matching `content/posts/<slug>.md` or `content/book/<name>.md`, or
     `notes.md` for sweep nodes), plus valid `notes.md` and `RESTATERS` locators.
  2. Stage 3 (`<slug>`): verifies all Stage 1 checks above, plus `HANDOFF_CONFIRMED` with
     the same `en.md` `sha256` and `TRANSLATOR: confirmed` (or `STYLIST: confirmed`) whose
     `sha256` matches `sha256(work/<slug>/zh.md)` and `source_sha256` matches `sha256(en.md)`.
  3. `--locators <notes.md>`: verifies every backtick `path:line` / `slug:line` locator
     in `notes.md` (against the working tree pre-consolidation, and across `<commit>~1`
     when `--commit <sha>` is supplied), AND validates any Stage 1 / Stage 2 sign-off
     or `VERDICT:` lines already present in `notes.md`.
  4. With `--record-batch <m> --commit <sha> <slug1> ...`, deterministically updates
     `work/wave.md` checkboxes, prunes completed items and appends `DELTA (propagates)`
     and `### For work/todo.md` items in `work/todo.md`, and writes `work/_logs/batch-<m>.md`.
  5. With `--clean-sleep [--dry-run]`, deterministically harvests any unrecorded
     open `### For work/todo.md` items (skipping `- [x]` resolved items) from the
     directories to be deleted into `work/todo.md` and deletes ONLY the completed `[x]` `/sleep` node and sweep directories recorded
     in `work/wave.md` (`_plan-consolidation`, `_reverse-link-sweep`, `_post-wave-sweep`,
     `_logs`, and `[x]` node slugs in `work/wave.md` whose post exists in
     `content/posts/<slug>.md` and that have no pending `work/_wake/<slug>/handoff.md`),
     explicitly preserving `work/_wake/`, `work/plan/`, and any concurrent `/first-draft`
     or `/scout` handoff directory.

Usage:
  python3 scripts/check-signoffs.py [--commit <sha>] <slug> [<slug2> ...]
  python3 scripts/check-signoffs.py --stage1 [--commit <sha>] <slug> [<slug2> ...]
  python3 scripts/check-signoffs.py --locators [--commit <sha>] <notes.md> [<notes2.md> ...]
  python3 scripts/check-signoffs.py --record-batch <m> --commit <sha> [--deploy-run <id>] [--problem <note>] <slug1> [<slug2> ...]
  python3 scripts/check-signoffs.py --clean-sleep [--dry-run]
"""

from __future__ import annotations

import hashlib
import pathlib
import re
import shutil
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parent.parent
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
SWEEP_SLUGS = {"_plan-consolidation", "_reverse-link-sweep", "_post-wave-sweep"}
POST_SLUG_PAT = r"[A-Za-z0-9][A-Za-z0-9_-]*"
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
SIGNOFF_META_PREFIX_PAT = (
    r"(?:VERDICT|SUMMARY|DRAFTER|TRANSLATOR|CRITIC|STYLIST|"
    r"HANDOFF_CONFIRMED|S_PRE|S_POST|HOLD|RECAP|OPERATOR|PLANNER|SCOUTER|STATUS):"
)


_GIT_BLOB_CACHE: dict[tuple[str, str], bytes | None] = {}
_SAFE_REV_RE = re.compile(r"^[0-9A-Za-z._~^/-]+$")


def sha256_file(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_commit_sha(commit_sha: str | None) -> str | None:
    if not commit_sha:
        return None
    cleaned = commit_sha.strip()
    if not cleaned or cleaned.lower() == "none" or cleaned.startswith("-") or not _SAFE_REV_RE.match(cleaned):
        return None
    return cleaned


def git_blob_bytes(rev: str, rel_posix: str) -> bytes | None:
    if not rev or rev.startswith("-") or not _SAFE_REV_RE.match(rev):
        return None
    key = (rev, rel_posix)
    if key in _GIT_BLOB_CACHE:
        return _GIT_BLOB_CACHE[key]
    try:
        proc = subprocess.run(
            ["git", "-C", str(ROOT), "show", f"{rev}:{rel_posix}"],
            capture_output=True,
            check=False,
        )
    except OSError:
        _GIT_BLOB_CACHE[key] = None
        return None
    blob = proc.stdout if proc.returncode == 0 else None
    _GIT_BLOB_CACHE[key] = blob
    return blob


def validate_single_locator(
    tok: str,
    label: str,
    source_label: str,
    base_dir: pathlib.Path | None = None,
    line_count_cache: dict[pathlib.Path, int] | None = None,
    commit_sha: str | None = None,
) -> list[str]:
    errors: list[str] = []
    if ":" not in tok:
        return [f"[{label}] Invalid locator `{tok}` in {source_label} (expected slug:line)"]
    head, tail = tok.split(":", 1)
    sha = normalize_commit_sha(commit_sha)
    cand = ROOT / head
    if not cand.is_file() and base_dir is not None:
        cand = base_dir / head
    if not cand.is_file():
        slug = head.removesuffix(".md")
        cand = ROOT / "content" / "posts" / f"{slug}.md"

    resolved: pathlib.Path | None = None
    max_line: int | None = None
    if cand.is_file():
        resolved = cand.resolve()
        if line_count_cache is not None:
            if resolved not in line_count_cache:
                line_count_cache[resolved] = len(resolved.read_text(encoding="utf-8").split("\n"))
            max_line = line_count_cache[resolved]
        else:
            max_line = len(resolved.read_text(encoding="utf-8").split("\n"))
    elif sha:
        for raw_rel in (head, f"content/posts/{head.removesuffix('.md')}.md"):
            cand_rel = (ROOT / raw_rel).resolve()
            if not cand_rel.is_relative_to(ROOT):
                continue
            blob = git_blob_bytes(f"{sha}~1", cand_rel.relative_to(ROOT).as_posix())
            if blob is not None:
                max_line = len(blob.decode("utf-8", errors="replace").split("\n"))
                break

    if max_line is None:
        return [f"[{label}] Unresolved locator `{tok}` in {source_label} (file not found)"]

    nums = [int(n) for n in re.findall(r"\d+", tail)]
    if not nums:
        return [f"[{label}] Locator `{tok}` in {source_label} has no line numbers"]
    bad = [n for n in nums if n < 1 or n > max_line]
    if bad and sha and resolved is not None and resolved.is_relative_to(ROOT):
        rel_posix = resolved.relative_to(ROOT).as_posix()
        blob = git_blob_bytes(f"{sha}~1", rel_posix)
        if blob is not None:
            baseline_max = len(blob.decode("utf-8", errors="replace").split("\n"))
            if baseline_max > max_line:
                max_line = baseline_max
                bad = [n for n in nums if n < 1 or n > max_line]
        elif rel_posix == "work/todo.md":
            # work/todo.md is gitignored and pruned in-place by --record-batch
            bad = [n for n in nums if n < 1]
    if bad:
        errors.append(
            f"[{label}] Locator `{tok}` in {source_label} exceeds file length (line {bad[0]} > {max_line})"
        )
    return errors


def check_locators_only(
    notes_path: pathlib.Path,
    label: str,
    commit_sha: str | None = None,
) -> list[str]:
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
                commit_sha=commit_sha,
            )
        )
    return errors


def check_locators(
    notes_path: pathlib.Path,
    label: str,
    commit_sha: str | None = None,
) -> list[str]:
    errors = check_locators_only(notes_path, label, commit_sha=commit_sha)
    if not notes_path.is_file():
        return errors

    resolved_notes = notes_path.resolve()
    work_dir = resolved_notes.parent
    is_work_slug_dir = (
        resolved_notes.name == "notes.md"
        and work_dir.parent == (ROOT / "work").resolve()
    )
    slug = work_dir.name if is_work_slug_dir else label
    notes_text = notes_path.read_text(encoding="utf-8")

    is_no_delta, _, _, _, _, s1_errs = verify_stage1_signoffs(
        slug,
        work_dir,
        notes_path,
        notes_text,
        require_signoff=False,
        require_verdict_summary=False,
        commit_sha=commit_sha,
        is_work_slug_dir=is_work_slug_dir,
    )
    errors.extend(s1_errs)

    en_path, _ = resolve_delta_primary_path(slug, work_dir)
    zh_path = work_dir / "zh.md"
    en_sha = "" if is_no_delta else (sha256_file(en_path) if en_path.is_file() else "")
    _, s2_errs = verify_stage2_signoffs(
        slug,
        en_path,
        en_sha,
        zh_path,
        notes_text,
        notes_text,
        require_signoffs=False,
    )
    errors.extend(s2_errs)
    return errors


def parse_critic_verdict_and_summary(
    slug: str,
    deb_en: str,
    is_no_delta: bool | None,
    require_lines: bool = False,
    commit_sha: str | None = None,
) -> tuple[str, list[tuple[str, bool]], str, list[str]]:
    """
    Deterministically parses `VERDICT: ... | RESTATERS: ...` and `SUMMARY: ...`
    lines from `work/<slug>/notes.md` (or legacy `debate-en.md`).
    Returns (verdict, restaters_with_new_claim_flag, summary, errors).
    """
    errors: list[str] = []
    m_verdict = last_match(VERDICT_LINE_RE.pattern, deb_en)
    m_summary = last_match(SUMMARY_LINE_RE.pattern, deb_en)

    restaters: list[tuple[str, bool]] = []
    if m_verdict:
        raw_v = re.sub(r"\s+", " ", m_verdict.group(1).strip())
        raw_v = raw_v.replace("( ", "(").replace(" )", ")")
        if is_no_delta is True and raw_v != "NO_DELTA":
            errors.append(
                f"[{slug}] VERDICT line '{raw_v}' in notes.md contradicts confirmed_no_delta"
            )
        elif is_no_delta is False and raw_v == "NO_DELTA":
            errors.append(
                f"[{slug}] VERDICT line 'NO_DELTA' in notes.md contradicts confirmed DELTA"
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
                    rf"(?<![A-Za-z0-9_-])`?({POST_SLUG_PAT}:(?:\d+(?:\s*[-–]\s*\d+)?)(?:\s*,\s*\d+(?:\s*[-–]\s*\d+)?)*)`?(\s*\(\s*new_claim\s*\))?",
                    restaters_field,
                )
                if not tokens:
                    errors.append(
                        f"[{slug}] Could not parse RESTATERS field '{restaters_field}' in notes.md "
                        "(expected 'none' or '<slug>:<line>[, <slug2>:<line>...]')"
                    )
                for loc_tok, new_claim_group in tokens:
                    loc_clean = re.sub(r"\s+", "", loc_tok)
                    r_slug = loc_clean.split(":", 1)[0].removesuffix(".md")
                    if r_slug == slug:
                        errors.append(
                            f"[{slug}] Self-locator `{loc_clean}` listed in RESTATERS in notes.md"
                        )
                        continue
                    loc_errs = validate_single_locator(
                        loc_clean,
                        slug,
                        "notes.md (RESTATERS)",
                        line_count_cache=line_count_cache,
                        commit_sha=commit_sha,
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
                f"[{slug}] Missing 'VERDICT: <DELTA (terminal)|DELTA (propagates)|NO_DELTA> | RESTATERS: <...|none>' line in notes.md"
            )

    if m_summary:
        summary = m_summary.group(1).strip().replace("|", "\\|")
        if not summary:
            errors.append(f"[{slug}] Empty 'SUMMARY:' line in notes.md")
    else:
        summary = verdict
        if require_lines:
            errors.append(f"[{slug}] Missing 'SUMMARY: <1-line summary>' line in notes.md")

    return (verdict, restaters, summary, errors)


def last_match(pattern: str, text: str) -> re.Match[str] | None:
    matches = list(re.finditer(pattern, text, flags=re.MULTILINE))
    return matches[-1] if matches else None


def decorated_signoff_error(
    slug: str,
    token: str,
    decorated_body_pattern: str,
    file_label: str,
    text: str,
) -> str | None:
    if re.search(r"^[^\S\n]*\S[^\n]*?" + decorated_body_pattern, text, flags=re.MULTILINE):
        return (
            f"[{slug}] Found '{token}' in {file_label} but not at a line start "
            "(list marker, quote or backtick before it); write it as its own line"
        )
    return None


def parse_digest_token(tail: str, key: str = "sha256") -> tuple[str | None, str | None]:
    m_key = re.search(rf"\b{re.escape(key)}:\s*[`\"']?([^\s,)\]`\"']+)[`\"']?", tail)
    if m_key:
        tok = m_key.group(1)
        if HEX64_RE.fullmatch(tok):
            return tok, None
        return None, f"invalid {key} '{tok}' (expected 64 lowercase hex chars, got {len(tok)})"
    if key == "sha256":
        m_bare = re.search(r"\b([0-9a-f]{64})\b", tail)
        if m_bare:
            return m_bare.group(1), None
    return None, f"missing '{key}: <64-hex>'"


def resolve_delta_primary_path(slug: str, work_dir: pathlib.Path) -> tuple[pathlib.Path, bool]:
    en_path = work_dir / "en.md"
    draft_path = work_dir / "draft.md"
    if slug == "_plan-consolidation" and draft_path.is_file() and not en_path.is_file():
        return draft_path, True
    return en_path, False


def _display_rel(path: pathlib.Path) -> str:
    resolved = path.resolve()
    root_resolved = ROOT.resolve()
    if resolved.is_relative_to(root_resolved):
        return resolved.relative_to(root_resolved).as_posix()
    return str(path)


def verify_stage1_signoffs(
    slug: str,
    work_dir: pathlib.Path,
    notes_path: pathlib.Path,
    stage1_log: str,
    *,
    require_signoff: bool,
    require_verdict_summary: bool,
    commit_sha: str | None = None,
    is_work_slug_dir: bool = True,
) -> tuple[bool, str, str, list[tuple[str, bool]], str, list[str]]:
    errors: list[str] = []
    primary_path, _ = resolve_delta_primary_path(slug, work_dir)
    m_drafter = last_match(
        r"^(?:DRAFTER|CRITIC):\s*(confirmed_no_delta|confirmed)\b([^\n]*)$",
        stage1_log,
    )
    decorated_pat = (
        r"(?:DRAFTER|CRITIC):\s*(?:confirmed_no_delta|confirmed)\b[^\n]*?(?:\bsha256:|\(file:)"
    )

    if not m_drafter:
        dec_err = decorated_signoff_error(
            slug,
            "DRAFTER: confirmed",
            decorated_pat,
            "notes.md",
            stage1_log,
        )
        if dec_err:
            errors.append(dec_err)
        elif require_signoff:
            expected_tok = "DRAFTER: confirmed" if primary_path.is_file() else "DRAFTER: confirmed / confirmed_no_delta"
            errors.append(f"[{slug}] Missing '{expected_tok}' with sha256 in notes.md")

        if errors or require_signoff:
            verdict, restaters, summary, v_errs = parse_critic_verdict_and_summary(
                slug,
                stage1_log,
                is_no_delta=(not primary_path.is_file()),
                require_lines=require_verdict_summary,
                commit_sha=commit_sha,
            )
            errors.extend(v_errs)
            return (not primary_path.is_file(), "", verdict, restaters, summary, errors)

        # --locators mode with no DRAFTER signoff yet: still validate VERDICT/RESTATERS if written
        verdict, restaters, summary, v_errs = parse_critic_verdict_and_summary(
            slug,
            stage1_log,
            is_no_delta=None,
            require_lines=False,
            commit_sha=commit_sha,
        )
        errors.extend(v_errs)
        return (False, "", verdict, restaters, summary, errors)

    kind = m_drafter.group(1)
    tail = m_drafter.group(2)
    is_no_delta = kind == "confirmed_no_delta"
    m_file = re.search(r"\bfile:\s*[`\"']?([^\s,)\]`\"']+)[`\"']?", tail)
    file_tok = m_file.group(1) if m_file else None

    target_path: pathlib.Path | None = None
    if is_no_delta:
        if primary_path.is_file():
            errors.append(
                f"[{slug}] DRAFTER: confirmed_no_delta contradicts existing {_display_rel(primary_path)}"
            )
        if is_work_slug_dir:
            if slug.startswith("_book:"):
                post_or_book = ROOT / "content" / "book" / f"{slug[6:]}.md"
            else:
                post_or_book = ROOT / "content" / "posts" / f"{slug}.md"
            if post_or_book.is_file():
                target_path = post_or_book
            elif slug in SWEEP_SLUGS:
                target_path = notes_path
            else:
                errors.append(f"[{slug}] Missing target file for confirmed_no_delta")
        elif file_tok:
            cand = ROOT / file_tok
            if not cand.is_file() and (work_dir / file_tok).is_file():
                cand = work_dir / file_tok
            if cand.is_file():
                target_path = cand
            else:
                errors.append(f"[{slug}] Missing DRAFTER file target '{file_tok}'")
    else:
        if is_work_slug_dir:
            if slug in ("_reverse-link-sweep", "_post-wave-sweep") and not primary_path.is_file():
                target_path = notes_path
            else:
                target_path = primary_path
                if not target_path.is_file():
                    errors.append(f"[{slug}] Missing {_display_rel(target_path)}")
        elif file_tok:
            cand = ROOT / file_tok
            if not cand.is_file() and (work_dir / file_tok).is_file():
                cand = work_dir / file_tok
            if cand.is_file():
                target_path = cand
            else:
                errors.append(f"[{slug}] Missing DRAFTER file target '{file_tok}'")
        elif primary_path.is_file():
            target_path = primary_path

    if file_tok and target_path is not None and is_work_slug_dir:
        cand_file = ROOT / file_tok
        if cand_file.resolve() != target_path.resolve():
            errors.append(
                f"[{slug}] DRAFTER: {kind} file '{file_tok}' != expected '{_display_rel(target_path)}'"
            )

    recorded_sha, sha_err = parse_digest_token(tail, "sha256")
    matched_sha = ""
    if sha_err:
        errors.append(f"[{slug}] DRAFTER: {kind} {sha_err} in notes.md")
    elif target_path is not None and target_path.is_file():
        if target_path.resolve() == notes_path.resolve():
            matched_sha = recorded_sha or ""
        else:
            expected_sha = sha256_file(target_path)
            matched_sha = expected_sha
            if recorded_sha != expected_sha:
                baseline_matched = False
                if is_no_delta:
                    sha = normalize_commit_sha(commit_sha)
                    resolved_target = target_path.resolve()
                    if sha and resolved_target.is_relative_to(ROOT.resolve()):
                        blob = git_blob_bytes(
                            f"{sha}~1",
                            resolved_target.relative_to(ROOT.resolve()).as_posix(),
                        )
                        if blob is not None and hashlib.sha256(blob).hexdigest() == recorded_sha:
                            baseline_matched = True
                            matched_sha = recorded_sha or ""
                if not baseline_matched:
                    tag = "confirmed_no_delta " if is_no_delta else ""
                    errors.append(
                        f"[{slug}] DRAFTER {tag}sha256 ({recorded_sha[:12]}...) "
                        f"!= {target_path.name} ({expected_sha[:12]}...)"
                    )

    verdict, restaters, summary, v_errs = parse_critic_verdict_and_summary(
        slug,
        stage1_log,
        is_no_delta=is_no_delta,
        require_lines=require_verdict_summary,
        commit_sha=commit_sha,
    )
    errors.extend(v_errs)
    return (is_no_delta, matched_sha, verdict, restaters, summary, errors)


def verify_stage2_signoffs(
    slug: str,
    en_path: pathlib.Path,
    en_sha: str,
    zh_path: pathlib.Path,
    stage1_log: str,
    stage2_log: str,
    *,
    require_signoffs: bool,
) -> tuple[str, list[str]]:
    errors: list[str] = []
    zh_sha = sha256_file(zh_path) if zh_path.is_file() else ""

    combined_handoff_log = (stage2_log + "\n" + stage1_log).strip()
    m_handoff = last_match(r"^HANDOFF_CONFIRMED:([^\n]*)$", stage2_log) or last_match(
        r"^HANDOFF_CONFIRMED:([^\n]*)$", stage1_log
    )
    if not m_handoff:
        dec_err = decorated_signoff_error(
            slug,
            "HANDOFF_CONFIRMED",
            r"HANDOFF_CONFIRMED:[^\n]*?(?:\bsha256:|work/)",
            "notes.md",
            combined_handoff_log,
        )
        if dec_err:
            errors.append(dec_err)
        elif require_signoffs:
            errors.append(f"[{slug}] Missing 'HANDOFF_CONFIRMED' with sha256 in notes.md")
    else:
        recorded_h, h_err = parse_digest_token(m_handoff.group(1), "sha256")
        if h_err:
            errors.append(f"[{slug}] HANDOFF_CONFIRMED {h_err} in notes.md")
        elif not en_sha:
            errors.append(f"[{slug}] HANDOFF_CONFIRMED present but {_display_rel(en_path)} missing")
        elif recorded_h != en_sha:
            errors.append(
                f"[{slug}] HANDOFF_CONFIRMED sha256 ({recorded_h[:12]}...) != {en_path.name} ({en_sha[:12]}...)"
            )

    m_translator = last_match(r"^(?:TRANSLATOR|STYLIST):\s*confirmed\b([^\n]*)$", stage2_log)
    if not m_translator:
        dec_err = decorated_signoff_error(
            slug,
            "TRANSLATOR: confirmed",
            r"(?:TRANSLATOR|STYLIST):\s*confirmed\b[^\n]*?(?:\bsha256:|\(file:)",
            "notes.md",
            stage2_log,
        )
        if dec_err:
            errors.append(dec_err)
        elif require_signoffs:
            errors.append(f"[{slug}] Missing 'TRANSLATOR: confirmed' in notes.md")
    else:
        tail = m_translator.group(1)
        recorded_zh, zh_err = parse_digest_token(tail, "sha256")
        recorded_src, src_err = parse_digest_token(tail, "source_sha256")
        if zh_err:
            errors.append(f"[{slug}] TRANSLATOR: confirmed {zh_err}")
        elif not zh_sha:
            errors.append(f"[{slug}] TRANSLATOR: confirmed present but {_display_rel(zh_path)} missing")
        elif recorded_zh != zh_sha:
            errors.append(
                f"[{slug}] TRANSLATOR sha256 ({recorded_zh[:12]}...) != {zh_path.name} ({zh_sha[:12]}...)"
            )
        if src_err:
            errors.append(f"[{slug}] TRANSLATOR: confirmed {src_err}")
        elif not en_sha:
            errors.append(f"[{slug}] TRANSLATOR: confirmed present but {_display_rel(en_path)} missing")
        elif recorded_src != en_sha:
            errors.append(
                f"[{slug}] TRANSLATOR source_sha256 ({recorded_src[:12]}...) != {en_path.name} ({en_sha[:12]}...)"
            )

    return zh_sha, errors


def verify_stage1_node(
    slug: str,
    commit_sha: str | None = None,
) -> tuple[str, str, list[str]]:
    work_dir = ROOT / "work" / slug
    notes_path = work_dir / "notes.md"
    if not notes_path.is_file():
        return ("UNKNOWN", "", [f"[{slug}] Missing {_display_rel(notes_path)}"])
    notes_text = notes_path.read_text(encoding="utf-8")
    require_vs = not (slug in SWEEP_SLUGS)
    _, stage1_sha, verdict, _, _, errors = verify_stage1_signoffs(
        slug,
        work_dir,
        notes_path,
        notes_text,
        require_signoff=True,
        require_verdict_summary=require_vs,
        commit_sha=commit_sha,
        is_work_slug_dir=True,
    )
    errors.extend(check_locators_only(notes_path, slug, commit_sha=commit_sha))
    return (verdict, stage1_sha, errors)


def classify_node(
    slug: str,
    require_verdict_summary: bool = False,
    commit_sha: str | None = None,
) -> tuple[str, str, str, list[tuple[str, bool]], str, list[str]]:
    """
    Returns (verdict, en_or_post_sha, zh_sha, restaters, summary, errors) where verdict is one of:
      'NO_DELTA', 'DELTA (terminal)', 'DELTA (propagates)'
    """
    errors: list[str] = []
    work_dir = ROOT / "work" / slug
    en_path, _ = resolve_delta_primary_path(slug, work_dir)
    zh_path = work_dir / "zh.md"
    deb_en_path = work_dir / "debate-en.md"
    deb_zh_path = work_dir / "debate-zh.md"
    notes_path = work_dir / "notes.md"

    if not notes_path.is_file() and not deb_en_path.is_file():
        return ("UNKNOWN", "", "", [], "", [f"[{slug}] Missing {_display_rel(notes_path)}"])

    notes_text = notes_path.read_text(encoding="utf-8") if notes_path.is_file() else ""
    deb_en_text = deb_en_path.read_text(encoding="utf-8") if deb_en_path.is_file() else ""
    deb_zh_text = deb_zh_path.read_text(encoding="utf-8") if deb_zh_path.is_file() else ""
    stage1_log = (notes_text + "\n" + deb_en_text).strip()
    stage2_log = (notes_text + "\n" + deb_zh_text).strip()

    is_no_delta, stage1_sha, verdict, restaters, summary, s1_errs = verify_stage1_signoffs(
        slug,
        work_dir,
        notes_path,
        stage1_log,
        require_signoff=True,
        require_verdict_summary=require_verdict_summary,
        commit_sha=commit_sha,
        is_work_slug_dir=True,
    )
    errors.extend(s1_errs)

    if notes_path.is_file():
        errors.extend(check_locators_only(notes_path, slug, commit_sha=commit_sha))
    elif is_no_delta:
        errors.append(f"[{slug}] Missing work/{slug}/notes.md for NO_DELTA node")

    zh_sha = ""
    if not is_no_delta:
        if not notes_path.is_file():
            errors.append(f"[{slug}] Missing {_display_rel(notes_path)}")
        if slug not in SWEEP_SLUGS:
            if not zh_path.is_file():
                errors.append(f"[{slug}] Missing {_display_rel(zh_path)}")
            zh_sha, s2_errs = verify_stage2_signoffs(
                slug,
                en_path,
                stage1_sha,
                zh_path,
                stage1_log,
                stage2_log,
                require_signoffs=True,
            )
            errors.extend(s2_errs)

    return (verdict, stage1_sha, zh_sha, restaters, summary, errors)


def check_slug(slug: str, commit_sha: str | None = None) -> list[str]:
    _, _, _, _, _, errors = classify_node(slug, commit_sha=commit_sha)
    return errors


def valid_corpus_targets() -> tuple[set[str], set[str]]:
    posts = {
        p.stem
        for p in (ROOT / "content" / "posts").glob("*.md")
        if p.name != "README.md"
    }
    books = {
        f"_book:{p.stem}"
        for p in (ROOT / "content" / "book").glob("*.md")
    }
    return posts, books


def is_noop_todo_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return True
    if re.match(r"^(?:[-*]\s+)?\[[xX]\](?:\s+|$)", stripped):
        return True
    if re.match(rf"^{SIGNOFF_META_PREFIX_PAT}", stripped):
        return True
    body = re.sub(r"^(?:[-*]\s+)?(?:\[\s*\]\s+)?", "", stripped)
    body = body.strip("*_`() \t")
    if not body:
        return True
    return bool(
        re.match(
            r"^(?:none|n/?a|no\s+(?:new\s+|cross-node\s+|out-of-file\s+)?items?(?:\s+to\s+(?:add|report|record))?|nothing(?:\s+to\s+(?:add|report|record))?)(?:\s*[.:—–\-;(].*)?$",
            body,
            flags=re.IGNORECASE,
        )
    )


def extract_todo_blocks(slug: str) -> list[str]:
    work_dir = ROOT / "work" / slug
    items: list[str] = []
    heading_re = re.compile(r"^#{2,4}\s+For\s+`?work/todo\.md`?\b[^\n]*$", flags=re.IGNORECASE | re.MULTILINE)
    stop_re = re.compile(
        rf"\n(?:#{{1,6}}\s+|{SIGNOFF_META_PREFIX_PAT}|---+\s*$)",
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
                if is_noop_todo_line(line):
                    continue
                if line.startswith("* "):
                    line = "- " + line[2:].lstrip()
                elif line.startswith("[ ] "):
                    line = "- " + line
                elif not line.startswith("- "):
                    line = f"- {line}"
                if line not in items:
                    items.append(line)
    return items


def parse_line_numbers(tail: str) -> set[int]:
    nums: set[int] = set()
    for part in tail.split(","):
        part = part.strip()
        m_range = re.match(r"^(\d+)\s*[-–]\s*(\d+)$", part)
        if m_range:
            a, b = int(m_range.group(1)), int(m_range.group(2))
            if 0 <= b - a <= 50:
                nums.update(range(a, b + 1))
            else:
                nums.add(a)
                nums.add(b)
        else:
            for d in re.findall(r"\d+", part):
                nums.add(int(d))
    return nums


def split_header_body(work: str) -> tuple[str, str]:
    in_bt = False
    paren_depth = 0
    for idx, ch in enumerate(work):
        if ch == "`":
            in_bt = not in_bt
        elif not in_bt:
            if ch == "(":
                paren_depth += 1
            elif ch == ")" and paren_depth > 0:
                paren_depth -= 1
            elif ch == ":" and paren_depth == 0:
                nxt = work[idx + 1 : idx + 2]
                if not nxt or nxt.isspace():
                    return work[:idx], work[idx + 1 :]
    return work, ""


_CONTEXT_PREFIX_HEAD_NO_LINES_RE = re.compile(
    r"(?:noticed\s+from|from|citing|against|with|contradicting|vs\.?|gloss(?:es)?\s+on|(?<!\w)on)\s+(?:\*+|`+)?$",
    flags=re.IGNORECASE,
)
_CONTEXT_PREFIX_HEAD_WITH_LINES_RE = re.compile(
    r"(?:noticed\s+from|from|citing|against|with|contradicting|vs\.?|gloss(?:es)?\s+on)\s+(?:\*+|`+)?$",
    flags=re.IGNORECASE,
)
_CONTEXT_PREFIX_BODY_RE = re.compile(
    r"(?:noticed\s+from|from|citing|against|with|contradicting|vs\.?|gloss(?:es)?\s+on|(?<!\w)on|(?<!\w)in|corrected\s+in|fixed\s+in)\s+(?:the\s+)?(?:\*+|`+)?$",
    flags=re.IGNORECASE,
)


def strip_head_context_clauses(head: str) -> str:
    def _clean_paren(m: re.Match[str]) -> str:
        inner = m.group(1)
        if re.search(rf"`?{POST_SLUG_PAT}`?\s*`?/deep-sleep`?\s+observation", inner, flags=re.IGNORECASE):
            return ""
        inner = re.sub(
            r"(?:,\s*|;\s*)?\b(?:noticed\s+from|from|via|supplementing|if\s+not\s+already|corrected\s+in|fixed\s+in|already\s+|with\s+)\b.*$",
            "",
            inner,
            flags=re.IGNORECASE,
        ).strip()
        return f"({inner})" if inner else ""

    return re.sub(r"\(([^)]*)\)", _clean_paren, head)


def extract_context_slugs(line: str, valid_posts: set[str], targets: list[str]) -> set[str]:
    target_set = set(targets)
    ctx: set[str] = set()
    for m in re.finditer(rf"\.\./({POST_SLUG_PAT})(?:/|\.md)?", line):
        s = m.group(1)
        if s in valid_posts and s not in target_set:
            ctx.add(s)
    for m in re.finditer(rf"(?<![A-Za-z0-9_/-])`?(?:content/posts/)?({POST_SLUG_PAT})(?:\.md)?(?::[\d,\s–-]+)?`?(?![A-Za-z0-9_/-])", line):
        s = m.group(1)
        if s in valid_posts and s not in target_set:
            ctx.add(s)
    return ctx


def normalize_todo_text(line: str) -> str:
    s = re.sub(r"^(?:[-*]\s+)?(?:\[\s*[xX ]?\s*\]\s+)?", "", line.strip())
    s = s.replace("`", "").replace("*", "")
    return re.sub(r"\s+", " ", s).strip().lower()


def parse_todo_item(
    line: str,
    valid_posts: set[str],
    valid_books: set[str],
) -> dict[str, object]:
    is_non_gating = bool(
        re.search(
            r"\b(?:non-gating|not\s+a\s+logical\s+DELTA|Operator\s+fact-check|when\s+reached|unless\s+the\s+Operator\s+elects)\b",
            line,
            flags=re.IGNORECASE,
        )
    )
    norm_text = normalize_todo_text(line)
    if re.search(r"\bUnevaluated\s+`?\(u,\s*p@sha\)`?\s+neighbor\s+pairs\s+from\s+#", line, flags=re.IGNORECASE) or re.search(
        r"\bunless\s+the\s+Operator\s+elects\s+to\s+run\s+them\s+immediately\b",
        line,
        flags=re.IGNORECASE,
    ):
        return {
            "kind": "other",
            "targets": [],
            "lines_by_target": {},
            "context_slugs": set(),
            "is_non_gating": True,
            "norm_text": norm_text,
        }

    # 1. Book surfaces (_book:<name>)
    book_matches = [
        m.group(1)
        for m in re.finditer(r"(?<![A-Za-z0-9_/-])`?(_book:[a-z0-9-]+)`?(?![A-Za-z0-9_/@-])", line)
        if m.group(1) in valid_books
    ]
    if book_matches:
        targets = list(dict.fromkeys(book_matches))
        lines_by_target: dict[str, set[int]] = {}
        for b in targets:
            bname = b[6:]
            nums: set[int] = set()
            for m in re.finditer(rf"(?:content/book/)?{re.escape(bname)}\.md:(\d+(?:\s*[-–]\s*\d+)?(?:\s*,\s*\d+(?:\s*[-–]\s*\d+)?)*)", line):
                nums.update(parse_line_numbers(m.group(1)))
            if nums:
                lines_by_target[b] = nums
        return {
            "kind": "book",
            "targets": targets,
            "lines_by_target": lines_by_target,
            "context_slugs": extract_context_slugs(line, valid_posts, targets),
            "is_non_gating": is_non_gating,
            "norm_text": norm_text,
        }

    # 2. Explicit Evaluate fresh in `/deep-sleep`...: <targets>
    m_eval = re.search(r"Evaluate\s+fresh\s+in\s+`?/deep-sleep`?[^:\n]*:", line, flags=re.IGNORECASE)
    if m_eval:
        tail = line[m_eval.end() :]
        targets: list[str] = []
        lines_by_target = {}
        for m in re.finditer(rf"(?<![A-Za-z0-9_/-])`?({POST_SLUG_PAT})`?(?![A-Za-z0-9_/@-])(?:\s*\(([^)]*)\))?", tail):
            slug = m.group(1)
            if slug not in valid_posts:
                continue
            if slug not in targets:
                targets.append(slug)
            paren_txt = m.group(2) or ""
            nums: set[int] = set()
            for m_loc in re.finditer(rf"(?:{re.escape(slug)}(?:\.md)?|content/posts/{re.escape(slug)}\.md):(\d+(?:\s*[-–]\s*\d+)?(?:\s*,\s*\d+(?:\s*[-–]\s*\d+)?)*)", paren_txt + " " + line):
                nums.update(parse_line_numbers(m_loc.group(1)))
            if nums:
                lines_by_target[slug] = nums
        if targets:
            return {
                "kind": "eval_post",
                "targets": targets,
                "lines_by_target": lines_by_target,
                "context_slugs": extract_context_slugs(line, valid_posts, targets),
                "is_non_gating": is_non_gating,
                "norm_text": norm_text,
            }

    # 3. General post observation lines
    # Strip markdown link URLs so [Title](../other-slug/) inside prose doesn't leak as a target
    work = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"[\1]", line)
    head, body = split_header_body(work)
    cleaned_head = strip_head_context_clauses(head)

    targets = []
    lines_by_target = {}
    head_pat = re.compile(
        rf"(?<![A-Za-z0-9_/-])`?(?:content/posts/)?({POST_SLUG_PAT})(?:\.md)?(?::(\d+(?:\s*[-–]\s*\d+)?(?:\s*,\s*\d+(?:\s*[-–]\s*\d+)?)*))?`?(?![A-Za-z0-9_/@-])"
    )
    for m in head_pat.finditer(cleaned_head):
        slug = m.group(1)
        if slug not in valid_posts:
            continue
        prefix = cleaned_head[max(0, m.start() - 40) : m.start()]
        prefix_re = _CONTEXT_PREFIX_HEAD_WITH_LINES_RE if m.group(2) else _CONTEXT_PREFIX_HEAD_NO_LINES_RE
        if prefix_re.search(prefix):
            continue
        if slug not in targets:
            targets.append(slug)
        if m.group(2):
            lines_by_target.setdefault(slug, set()).update(parse_line_numbers(m.group(2)))

    if not targets and body:
        # Remove `(vs. ...)` explanations before scanning body for explicit `<slug>:<lines>` targets
        cleaned_body = re.sub(r"\(\s*vs\.?\s+[^)]*\)", "", body, flags=re.IGNORECASE)
        body_pat = re.compile(
            rf"(?<![A-Za-z0-9_/-])`?(?:content/posts/)?({POST_SLUG_PAT})(?:\.md)?:(\d+(?:\s*[-–]\s*\d+)?(?:\s*,\s*\d+(?:\s*[-–]\s*\d+)?)*)`?(?![A-Za-z0-9_/@-])"
        )
        for m in body_pat.finditer(cleaned_body):
            slug = m.group(1)
            if slug not in valid_posts:
                continue
            prefix = cleaned_body[max(0, m.start() - 40) : m.start()]
            if _CONTEXT_PREFIX_BODY_RE.search(prefix):
                continue
            if slug not in targets:
                targets.append(slug)
            lines_by_target.setdefault(slug, set()).update(parse_line_numbers(m.group(2)))

    if targets:
        # Also pick up `<target>:<lines>` from the full line for each discovered target
        for slug in targets:
            for m_loc in re.finditer(
                rf"(?<![A-Za-z0-9_/-])`?(?:content/posts/)?{re.escape(slug)}(?:\.md)?:(\d+(?:\s*[-–]\s*\d+)?(?:\s*,\s*\d+(?:\s*[-–]\s*\d+)?)*)`?(?![A-Za-z0-9_/@-])",
                work,
            ):
                lines_by_target.setdefault(slug, set()).update(parse_line_numbers(m_loc.group(1)))
        return {
            "kind": "general_post",
            "targets": targets,
            "lines_by_target": lines_by_target,
            "context_slugs": extract_context_slugs(line, valid_posts, targets),
            "is_non_gating": is_non_gating,
            "norm_text": norm_text,
        }

    return {
        "kind": "other",
        "targets": [],
        "lines_by_target": {},
        "context_slugs": set(),
        "is_non_gating": is_non_gating,
        "norm_text": norm_text,
    }


def is_target_duplicated(
    target: str,
    cand_spec: dict[str, object],
    existing_specs: list[dict[str, object]],
) -> bool:
    cand_lines_map: dict[str, set[int]] = cand_spec["lines_by_target"]  # type: ignore[assignment]
    cand_lines = cand_lines_map.get(target, set())
    cand_ctx: set[str] = cand_spec["context_slugs"]  # type: ignore[assignment]
    if not cand_lines:
        return False
    for ex in existing_specs:
        ex_targets: list[str] = ex["targets"]  # type: ignore[assignment]
        if target not in ex_targets:
            continue
        ex_lines_map: dict[str, set[int]] = ex["lines_by_target"]  # type: ignore[assignment]
        ex_lines = ex_lines_map.get(target, set())
        if not ex_lines or not (cand_lines & ex_lines):
            continue
        ex_ctx: set[str] = ex["context_slugs"]  # type: ignore[assignment]
        if not cand_ctx or not ex_ctx or (cand_ctx & ex_ctx):
            return True
    return False


def is_duplicate_todo(
    cand_spec: dict[str, object],
    existing_specs: list[dict[str, object]],
) -> bool:
    cand_norm = cand_spec["norm_text"]
    for ex in existing_specs:
        if cand_norm and cand_norm == ex["norm_text"]:
            return True
    targets: list[str] = cand_spec["targets"]  # type: ignore[assignment]
    if not targets:
        return False
    return all(is_target_duplicated(t, cand_spec, existing_specs) for t in targets)


def format_line_set(nums: set[int]) -> str:
    return ",".join(str(n) for n in sorted(nums))


def strip_targets_from_line(
    line: str,
    kind: str,
    drop_targets: set[str],
    keep_targets: list[str],
    valid_posts: set[str],
) -> str:
    if kind == "eval_post":
        m_eval = re.search(r"Evaluate\s+fresh\s+in\s+`?/deep-sleep`?[^:\n]*:", line, flags=re.IGNORECASE)
        if m_eval:
            prefix = line[: m_eval.end()]
            tail = line[m_eval.end() :]
            entry_matches = [
                m
                for m in re.finditer(
                    rf"(?<![A-Za-z0-9_/-])`?({POST_SLUG_PAT})`?(?![A-Za-z0-9_/@-])(?:\s*\([^)]*\))?",
                    tail,
                )
                if m.group(1) in valid_posts
            ]
            remaining_entries = [m.group(0) for m in entry_matches if m.group(1) not in drop_targets]
            if remaining_entries:
                return f"{prefix} {', '.join(remaining_entries)}."
    updated = line
    for t in drop_targets:
        if t.startswith("_book:"):
            updated = re.sub(
                rf"(?<![A-Za-z0-9_/-])`?({re.escape(t)})`?(?![A-Za-z0-9_/@-])",
                r"\1 [evaluated]",
                updated,
            )
        else:
            updated = re.sub(
                rf"(?<![A-Za-z0-9_/-])`?(?:content/posts/)?{re.escape(t)}(?:\.md)?(?::[\d,\s–-]+)?`?(?![A-Za-z0-9_/@-])",
                f"{t} [evaluated]",
                updated,
            )
    return updated


def normalize_new_todo_item(
    line: str,
    spec: dict[str, object],
) -> str:
    kind = spec["kind"]
    targets: list[str] = spec["targets"]  # type: ignore[assignment]
    is_non_gating = bool(spec["is_non_gating"])
    out = line
    if not is_non_gating and kind in ("book", "general_post", "eval_post"):
        if re.match(r"^-\s+(?!\[\s?[xX ]\])", out):
            out = re.sub(r"^-\s+", "- [ ] ", out, count=1)
    if kind == "general_post" and targets and not is_non_gating:
        # Replace trailing `; evaluate fresh in /deep-sleep.` (missing `:`/targets) with canonical suffix
        out = re.sub(
            r"(?:[;.]\s*|\s+)evaluate\s+fresh\s+in\s+`?/deep-sleep`?(?:\s+if\s+not\s+yet\s+audited[^.]*)?\.?$",
            "",
            out,
            flags=re.IGNORECASE,
        ).rstrip(" .;")
        lines_by_target: dict[str, set[int]] = spec["lines_by_target"]  # type: ignore[assignment]
        formatted_targets = []
        for t in targets:
            nums = lines_by_target.get(t)
            if nums:
                formatted_targets.append(f"`{t}` (`{t}:{format_line_set(nums)}`)")
            else:
                formatted_targets.append(f"`{t}`")
        out = f"{out}; Evaluate fresh in `/deep-sleep`: {', '.join(formatted_targets)}."
    return out


def filter_and_dedup_todo_items(
    raw_items: list[str],
    resolved_slugs: set[str],
    existing_todo_lines: list[str],
    valid_posts: set[str],
    valid_books: set[str],
    normalize_actionable: bool = True,
) -> list[str]:
    existing_specs = [
        parse_todo_item(l, valid_posts, valid_books)
        for l in existing_todo_lines
        if l.lstrip().startswith("- ")
    ]
    accepted_lines: list[str] = []
    accepted_specs: list[dict[str, object]] = []

    for raw in raw_items:
        spec = parse_todo_item(raw, valid_posts, valid_books)
        targets: list[str] = spec["targets"]  # type: ignore[assignment]
        kind = str(spec["kind"])
        all_specs = existing_specs + accepted_specs

        if targets:
            drop_targets: set[str] = set()
            keep_targets: list[str] = []
            for t in targets:
                if t in resolved_slugs or is_target_duplicated(t, spec, all_specs):
                    drop_targets.add(t)
                else:
                    keep_targets.append(t)
            if not keep_targets:
                continue
            item = raw if not drop_targets else strip_targets_from_line(raw, kind, drop_targets, keep_targets, valid_posts)
            spec = parse_todo_item(item, valid_posts, valid_books)
        else:
            item = raw
            if is_duplicate_todo(spec, all_specs):
                continue

        if normalize_actionable:
            item = normalize_new_todo_item(item, spec)
            spec = parse_todo_item(item, valid_posts, valid_books)

        if item not in existing_todo_lines and item not in accepted_lines:
            accepted_lines.append(item)
            accepted_specs.append(spec)
    return accepted_lines


def compute_remaining_unvisited() -> int:
    wave_path = ROOT / "work" / "wave.md"
    visited: set[str] = set()
    if wave_path.is_file():
        for m in re.finditer(r"^-\s+(?:\[[^\]]*\]\s+)?`([^`]+)`", wave_path.read_text(encoding="utf-8"), flags=re.MULTILINE):
            visited.add(m.group(1).strip())
    all_posts, book_surfaces = valid_corpus_targets()
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
            slug,
            require_verdict_summary=True,
            commit_sha=commit_sha,
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

    # 2. Update work/todo.md: prune completed [x] items, strike evaluated post/book slugs, and append filtered/deduped items
    todo_path = ROOT / "work" / "todo.md"
    batch_slug_set = set(slugs)
    valid_posts, valid_books = valid_corpus_targets()
    todo_trigger_by_slug: dict[str, str] = {}
    kept_todo_lines: list[str] = []
    if todo_path.is_file():
        existing_todo_text = todo_path.read_text(encoding="utf-8")
        for line in existing_todo_text.splitlines():
            if re.match(r"^-\s+\[[xX]\]\s+", line):
                continue
            if re.match(r"^-\s+\[\s\]\s+", line):
                spec = parse_todo_item(line, valid_posts, valid_books)
                kind = str(spec["kind"])
                targets: list[str] = spec["targets"]  # type: ignore[assignment]
                if kind in ("book", "eval_post", "general_post") and targets:
                    if kind in ("eval_post", "general_post"):
                        for t in targets:
                            todo_trigger_by_slug[t] = line
                    remaining = [t for t in targets if t not in batch_slug_set]
                    if not remaining:
                        continue
                    if len(remaining) < len(targets):
                        kept_todo_lines.append(
                            strip_targets_from_line(line, kind, batch_slug_set, remaining, valid_posts)
                        )
                        continue
            kept_todo_lines.append(line)

    new_todo_lines: list[str] = []
    raw_batch_todo_items: list[str] = []
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
                    f"`{r.split(':', 1)[0]}` (`{r}`, `links_in` restater)"
                    for r in queued_restaters
                )
                prop_line = (
                    f"- [ ] **`{slug}@{short_sha}` restating neighbor(s) (`/deep-sleep` Batch {batch_num} "
                    f"`DELTA (propagates)`)**: {summary} Evaluate fresh in `/deep-sleep` "
                    f"(with `{slug}@{short_sha}` as related material): {restater_str}."
                )
                if prop_line not in kept_todo_lines and prop_line not in new_todo_lines:
                    new_todo_lines.append(prop_line)
        raw_batch_todo_items.extend(extract_todo_blocks(slug))

    new_todo_lines.extend(
        filter_and_dedup_todo_items(
            raw_batch_todo_items,
            resolved_slugs=batch_slug_set,
            existing_todo_lines=kept_todo_lines + new_todo_lines,
            valid_posts=valid_posts,
            valid_books=valid_books,
            normalize_actionable=True,
        )
    )

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
        "| Node (`slug`) | Verdict | Stage 1 (`drafter`) | Stage 2 (`translator`) | 1-Line Summary |",
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
    checked_book_surfaces: set[str] = set()

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
        m_book = re.match(r"^`?(_book:[a-z0-9-]+)`?(?=\s|$)", tail.strip())
        if m_book:
            checked_book_surfaces.add(m_book.group(1))
            continue
        m_slug = re.match(
            rf"^(?:`({POST_SLUG_PAT})`|({POST_SLUG_PAT})(?=\s|$))",
            tail.strip(),
        )
        if m_slug:
            slug = m_slug.group(1) or m_slug.group(2)
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
    valid_posts, valid_books = valid_corpus_targets()
    raw_clean_items: list[str] = []
    for d in dirs_to_delete:
        raw_clean_items.extend(extract_todo_blocks(d.name))
    new_todo_lines = filter_and_dedup_todo_items(
        raw_clean_items,
        resolved_slugs=set(checked_slugs) | checked_book_surfaces,
        existing_todo_lines=kept_todo_lines,
        valid_posts=valid_posts,
        valid_books=valid_books,
        normalize_actionable=True,
    )

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


def parse_commit_and_targets(
    args: list[str],
    skip_flag: str | None = None,
) -> tuple[str | None, list[str]] | None:
    commit_sha: str | None = None
    targets: list[str] = []
    i = 0
    while i < len(args):
        arg = args[i]
        if skip_flag and arg == skip_flag:
            i += 1
        elif arg == "--commit" and i + 1 < len(args):
            commit_sha = args[i + 1]
            i += 2
        elif arg.startswith("--commit="):
            commit_sha = arg.split("=", 1)[1]
            i += 1
        elif not arg.startswith("-"):
            targets.append(arg)
            i += 1
        else:
            return None
    if not targets:
        return None
    return commit_sha, targets


def normalize_slug_arg(raw: str) -> str:
    p = pathlib.Path(raw)
    if p.name == "notes.md" and p.parent.name and p.parent.parent.name == "work":
        return p.parent.name
    return raw.removesuffix(".md")


def main(argv: list[str]) -> int:
    if "--clean-sleep" in argv[1:]:
        dry_run = "--dry-run" in argv[1:]
        extra = [a for a in argv[1:] if a not in ("--clean-sleep", "--dry-run")]
        if extra:
            print("Usage: python3 scripts/check-signoffs.py --clean-sleep [--dry-run]", file=sys.stderr)
            return 2
        return clean_sleep(dry_run=dry_run)

    if "--locators" in argv[1:]:
        usage = "Usage: python3 scripts/check-signoffs.py --locators [--commit <sha>] <notes.md> [<notes2.md> ...]"
        parsed = parse_commit_and_targets(argv[1:], skip_flag="--locators")
        if parsed is None:
            print(usage, file=sys.stderr)
            return 2
        commit_sha, targets = parsed
        all_errors: list[str] = []
        for raw in targets:
            p = pathlib.Path(raw)
            if not p.is_file() and (ROOT / "work" / raw.removesuffix(".md") / "notes.md").is_file():
                p = ROOT / "work" / raw.removesuffix(".md") / "notes.md"
            label = p.parent.name if p.name == "notes.md" else str(p)
            errs = check_locators(p, label, commit_sha=commit_sha)
            if errs:
                all_errors.extend(errs)
            else:
                print(f"Locators verified: {_display_rel(p)}")
        if all_errors:
            for e in all_errors:
                print(f"ERROR: {e}", file=sys.stderr)
            return 1
        return 0

    if "--stage1" in argv[1:]:
        usage = "Usage: python3 scripts/check-signoffs.py --stage1 [--commit <sha>] <slug> [<slug2> ...]"
        parsed = parse_commit_and_targets(argv[1:], skip_flag="--stage1")
        if parsed is None:
            print(usage, file=sys.stderr)
            return 2
        commit_sha, raw_targets = parsed
        slugs = [normalize_slug_arg(raw) for raw in raw_targets]
        all_errors = []
        for slug in slugs:
            verdict, _, errs = verify_stage1_node(slug, commit_sha=commit_sha)
            if errs:
                all_errors.extend(errs)
            else:
                print(f"Stage 1 verified: work/{slug}/ (verdict={verdict})")
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
            elif arg.startswith("--commit="):
                commit_sha = arg.split("=", 1)[1]
                i += 1
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

    usage = "Usage: python3 scripts/check-signoffs.py [--commit <sha>] <slug> [<slug2> ...]"
    parsed = parse_commit_and_targets(argv[1:])
    if parsed is None:
        print(usage, file=sys.stderr)
        return 2
    commit_sha, raw_targets = parsed
    slugs = [normalize_slug_arg(raw) for raw in raw_targets]

    all_errors = []
    for slug in slugs:
        verdict, _, _, _, _, errs = classify_node(slug, commit_sha=commit_sha)
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
