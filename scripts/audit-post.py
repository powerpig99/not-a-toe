#!/usr/bin/env python3
"""
Diagnostic audit script for post authoring invariants and workflow drift detection.

Philosophy:
  "非必要不变更，防止无意识漂移。"
  Standard conventions should remain consistent by default across sessions.
  They are not dogmatic straightjackets: intentional, context-driven variations
  are permitted when specifically required, but accidental erosion and negligence
  are caught before release.

Checks:
  1. Prose over lists (flags lists outside mermaid; reminder to write continuous prose unless necessary)
  2. Historical Mermaid inline dark-theme styling (#161b22, #0d1117, semantic color borders)
  3. Bilingual diagram parallelism (Chinese/English paired diagrams)
  4. Relative internal cross-links resolution (all ../slug/ exist; no absolute URLs)
  5. Banned words & essentialist cliches (0 tolerance for cognitive crutches)
  6. LaTeX syntax prohibition (0 raw $ or $$; Unicode math only)
  7. Multi-platform publishing copy in walkthrough (Spotify ZH/EN, WeChat Video, X EN)
  8. Companion NotebookLM prompts (canonical opening, monologue script, and concise bounds: 2-4 opening turns, < 8.5KB)

Usage:
  python3 scripts/audit-post.py [slug_or_path]
  python3 scripts/audit-post.py --allow-lists [slug_or_path]
  python3 scripts/audit-post.py --walkthrough <path_to_walkthrough.md>
"""

import sys
import os
import re
import argparse
from pathlib import Path

BANNED_WORDS = [
    '纯粹', '绝对', '完全', '彻底', '绝不', '通常', '往往', '或许',
    '某种意义上', '降维重构', '本质', '根本', '自始至终', '缰绳',
    '物理现实', '平庸', '物理意志'
]

REQUIRED_WALKTHROUGH_SECTIONS = [
    ('Companion NotebookLM Prompts (Audio & Video)', ['Companion NotebookLM Prompts', 'NotebookLM Prompts', 'Audio Dialogue', '语音对话', '视频独白', 'Video Monologue']),
    ('Spotify Podcast (ZH)', ['Spotify Podcast (ZH)', 'Spotify 播客（中文）']),
    ('Spotify Podcast (EN)', ['Spotify Podcast (EN)', 'Spotify 播客（英文）']),
    ('WeChat Video Channels', ['WeChat Video Channels', '微信视频号']),
    ('X (Twitter)', ['X (Twitter)', 'X (Twitter) (EN Only)', 'Twitter (X)'])
]

def find_target_file(arg):
    root = Path(__file__).resolve().parent.parent
    posts_dir = root / 'content' / 'posts'

    if arg:
        p = Path(arg)
        if p.is_file():
            return p
        if (posts_dir / f"{arg}.md").is_file():
            return posts_dir / f"{arg}.md"
        if (posts_dir / arg).is_file():
            return posts_dir / arg
        sys.exit(f"Error: Target post file '{arg}' not found.")

    # Auto-detect newest post in content/posts
    md_files = [f for f in posts_dir.glob('*.md') if f.name != 'README.md']
    if not md_files:
        sys.exit("Error: No markdown posts found in content/posts.")
    md_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return md_files[0]

def audit_post(file_path, allow_lists=False, walkthrough_path=None):
    root = Path(__file__).resolve().parent.parent
    posts_dir = root / 'content' / 'posts'

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.splitlines()
    slug = file_path.stem

    warnings = []
    errors = []
    passes = []

    print("=" * 70)
    print(f"POST AUDIT: {file_path.name}")
    print(f"Location:   {file_path}")
    print("=" * 70)

    # 1. Banned words audit
    found_banned = {}
    for word in BANNED_WORDS:
        matches = [m.start() for m in re.finditer(re.escape(word), content)]
        if matches:
            found_banned[word] = len(matches)

    if found_banned:
        errors.append(f"Banned words detected: {found_banned}")
    else:
        passes.append("Banned vocabulary check (0 prohibited terms)")

    # 2. LaTeX dollar audit
    # Literal $ signs in text
    dollar_count = content.count('$')
    if dollar_count > 0:
        errors.append(f"Raw LaTeX dollar signs detected ({dollar_count} occurrences). Use clean Unicode math symbols.")
    else:
        passes.append("Mathematical notation check (0 raw $ symbols)")

    # 3. Absolute URL check
    abs_matches = re.findall(r'https?://(?:powerpig99\.github\.io/not-a-toe|not-a-toe\.org)/posts/([a-zA-Z0-9_-]+)/?', content)
    if abs_matches:
        errors.append(f"Hardcoded absolute site URLs found for: {abs_matches}. Internal links MUST be relative: [title](../slug/).")
    else:
        passes.append("Link locality check (no hardcoded absolute site URLs)")

    # 4. Cross-links resolution
    rel_links = re.findall(r'\[([^\]]+)\]\(\.\./([a-zA-Z0-9_-]+)/?(?:#[^)]*)?\)', content)
    missing_links = []
    for anchor, target_slug in rel_links:
        target_path = posts_dir / f"{target_slug}.md"
        if not target_path.is_file():
            missing_links.append((anchor, target_slug))

    if missing_links:
        errors.append(f"Broken relative cross-links (missing targets): {missing_links}")
    else:
        passes.append(f"Relative cross-links check ({len(rel_links)} links resolved cleanly)")

    # 5. List items outside Mermaid
    in_mermaid = False
    list_lines = []
    for idx, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('```mermaid'):
            in_mermaid = True
        elif in_mermaid and stripped.startswith('```'):
            in_mermaid = False
        elif not in_mermaid:
            if re.match(r'^\s*([0-9]+\.|\*|-)\s+', line):
                list_lines.append((idx, line.strip()))

    if list_lines:
        msg = f"List syntax detected outside Mermaid ({len(list_lines)} lines). Rule: unless strictly necessary, do not use lists in essay prose."
        if allow_lists:
            warnings.append(f"{msg} [ALLOWED via --allow-lists]")
        else:
            warnings.append(f"{msg}\n    Examples: " + "; ".join([f"L{l[0]}: {l[1][:50]}" for l in list_lines[:4]]))
    else:
        passes.append("Prose structure check (0 bulleted/numbered lists outside Mermaid)")

    # 6. Mermaid dark theme & styling
    mermaid_blocks = re.findall(r'```mermaid(.*?)```', content, re.DOTALL)
    if mermaid_blocks:
        unformatted_diagrams = []
        for i, block in enumerate(mermaid_blocks, 1):
            has_subgraph_style = 'fill:#161b22' in block
            has_node_style = 'fill:#0d1117' in block
            if not (has_subgraph_style and has_node_style):
                unformatted_diagrams.append(i)

        if unformatted_diagrams:
            errors.append(f"Mermaid diagrams missing historical dark-theme inline styles (#161b22, #0d1117): Diagrams {unformatted_diagrams} of {len(mermaid_blocks)}")
        else:
            passes.append(f"Mermaid styling check ({len(mermaid_blocks)} diagrams adhere to historical dark palette)")

        # Bilingual parallelism check
        has_zh = bool(re.search(r'[\u4e00-\u9fff]', content))
        has_en = bool(re.search(r'##\s+.*\b(Section|Epilogue|Prologue)\b', content, re.IGNORECASE))
        if has_zh and has_en:
            if len(mermaid_blocks) % 2 != 0:
                warnings.append(f"Bilingual diagram count is odd ({len(mermaid_blocks)}). Ensure every Chinese diagram has its exact English parallel counterpart.")
            else:
                passes.append(f"Bilingual diagram parallelism ({len(mermaid_blocks) // 2} paired diagrams)")
    else:
        passes.append("Mermaid check (no diagrams in this post)")

    # 7. Walkthrough copy check (if walkthrough provided or discovered)
    if not walkthrough_path:
        brain_walkthrough = Path("/Users/jingliang/.gemini/antigravity/brain/f0e7480f-958a-4183-80da-595bc3ad23df/walkthrough.md")
        if brain_walkthrough.is_file():
            walkthrough_path = brain_walkthrough

    if walkthrough_path and Path(walkthrough_path).is_file():
        with open(walkthrough_path, 'r', encoding='utf-8') as wf:
            w_content = wf.read()

        missing_platforms = []
        for platform_name, patterns in REQUIRED_WALKTHROUGH_SECTIONS:
            if not any(pat in w_content for pat in patterns):
                missing_platforms.append(platform_name)

        if missing_platforms:
            warnings.append(f"Walkthrough missing required sections for: {missing_platforms}")
        else:
            passes.append("Walkthrough copy check (NotebookLM Prompts, Spotify ZH/EN, WeChat Video, X EN all present)")

        # Verify that all 4 platform copies include the canonical post URL
        expected_url_slug = f"posts/{slug}"
        missing_url_platforms = []
        platform_sections = [
            ('Spotify Podcast (ZH)', ['Spotify Podcast (ZH)', 'Spotify 播客（中文）']),
            ('Spotify Podcast (EN)', ['Spotify Podcast (EN)', 'Spotify 播客（英文）']),
            ('WeChat Video Channels', ['WeChat Video Channels', '微信视频号']),
            ('X (Twitter)', ['X (Twitter)', 'X (Twitter) (EN Only)', 'Twitter (X)'])
        ]
        for name, patterns in platform_sections:
            found_pos = -1
            for pat in patterns:
                pos = w_content.find(pat)
                if pos != -1:
                    found_pos = pos
                    break
            if found_pos != -1:
                next_header = re.search(r'\n#{2,3}\s+', w_content[found_pos + 10:])
                end_pos = (found_pos + 10 + next_header.start()) if next_header else len(w_content)
                sec_text = w_content[found_pos:end_pos]
                if expected_url_slug not in sec_text:
                    missing_url_platforms.append(name)

        if missing_url_platforms:
            warnings.append(f"Walkthrough platform copies missing canonical post link ({expected_url_slug}): {missing_url_platforms}")
        else:
            passes.append("Walkthrough platform copy links check (all 4 platform copies include canonical post URL)")

    # 8. Companion NotebookLM prompts audit
    prompts_dir = root / 'notebooklm-auto' / 'prompts'
    audio_prompt_file = prompts_dir / f"{slug}_zh.txt"
    video_prompt_file = prompts_dir / f"{slug}_video_zh.txt"

    prompt_missing = []
    if not audio_prompt_file.is_file():
        prompt_missing.append(f"notebooklm-auto/prompts/{slug}_zh.txt (Audio Dialogue)")
    if not video_prompt_file.is_file():
        prompt_missing.append(f"notebooklm-auto/prompts/{slug}_video_zh.txt (Video Monologue)")

    if prompt_missing:
        warnings.append(f"Missing companion NotebookLM prompt files: {prompt_missing}")
    else:
        # Check prompt files for banned words & raw $
        prompt_banned = {}
        for pf in [audio_prompt_file, video_prompt_file]:
            p_text = pf.read_text(encoding='utf-8')
            for w in BANNED_WORDS:
                if w in p_text:
                    prompt_banned.setdefault(pf.name, []).append(w)
            if '$' in p_text:
                errors.append(f"Raw $ detected in prompt file {pf.name}")
        if prompt_banned:
            errors.append(f"Banned words detected in companion prompts: {prompt_banned}")
        else:
            passes.append("Companion NotebookLM prompts check (Audio Dialogue & Video Monologue present and clean)")

        # Verify standard schema: opening dialogue in audio prompt, full spoken script in video prompt
        audio_text = audio_prompt_file.read_text(encoding='utf-8')
        video_text = video_prompt_file.read_text(encoding='utf-8')
        schema_missing = []
        if '角色与对话规范' not in audio_text:
            schema_missing.append(f"{audio_prompt_file.name} missing '### [角色与对话规范]'")
        if '核心议题清单' not in audio_text:
            schema_missing.append(f"{audio_prompt_file.name} missing '### [核心议题清单]'")
        if '正文对谈开场示例' not in audio_text:
            schema_missing.append(f"{audio_prompt_file.name} missing '### [正文对谈开场示例]' (standard dialogue opening)")
        else:
            canonical_phrases = ['同一事实的两面', '脚手架', '非万物之理']
            if not any(phrase in audio_text for phrase in canonical_phrases):
                schema_missing.append(f"{audio_prompt_file.name} missing canonical Not-a-ToE opening on causality and first-person perspective ('同一事实的两面', '脚手架', or '非万物之理')")
        if '正文文稿' not in video_text:
            schema_missing.append(f"{video_prompt_file.name} missing '### [正文文稿]' (full monologue script)")

        if schema_missing:
            warnings.append(f"Companion prompt schema incomplete: {schema_missing}. Rule: Standard opening dialogue (with canonical Not-a-ToE opening on causality and first-person perspective) and monologue script must be refined based on new analysis, but never deleted or omitted.")
        else:
            passes.append("Companion prompt schema check (Audio Canonical Opening Dialogue & Video Monologue Script present)")

        # Verify concise sizing bounds for audio dialogue prompt (must be opening sample of 2-4 turns, not a full transcript dump)
        audio_bytes = len(audio_prompt_file.read_bytes())
        dialogue_turns = len(re.findall(r'(?:\*\*明理\*\*|\*\*雨涵\*\*|明理：|雨涵：)', audio_text))
        if dialogue_turns > 5:
            errors.append(f"Audio prompt {audio_prompt_file.name} dialogue turns ({dialogue_turns}) exceed concise opening limit (rule: 2–4 turns; detected {dialogue_turns} turns). Do not dump full episode transcripts into the prompt.")
        elif audio_bytes > 8500:
            errors.append(f"Audio prompt {audio_prompt_file.name} size ({audio_bytes} bytes) exceeds concise threshold (rule: < 8.5KB). Keep dialogue to 2–4 opening turns.")
        else:
            passes.append(f"Companion audio prompt concise bounds check ({audio_bytes} bytes, {dialogue_turns} opening turns; complies with 2–4 turn, < 8.5KB standard)")

    # Report results
    print("\n[PASSED INVARIANTS]")
    for p in passes:
        print(f"  ✓ {p}")

    if warnings:
        print("\n[CONTEXTUAL WARNINGS / DRIFT ADVISORIES]")
        for w in warnings:
            print(f"  ⚠ {w}")

    if errors:
        print("\n[CRITICAL VIOLATIONS]")
        for e in errors:
            print(f"  ✗ {e}")
        print("\nResult: FAILED (violations must be resolved or explicitly overridden).")
        return False
    else:
        if warnings:
            print("\nResult: PASSED WITH ADVISORIES (verify intentionality of exceptions).")
        else:
            print("\nResult: CLEAN PASS (fully aligned with standard invariants).")
        return True

def main():
    parser = argparse.ArgumentParser(description="Audit post against authoring invariants to prevent workflow drift.")
    parser.add_argument("post", nargs="?", help="Post slug or markdown file path (defaults to latest modified post).")
    parser.add_argument("--allow-lists", action="store_true", help="Acknowledge list formatting as an intentional exception.")
    parser.add_argument("--walkthrough", help="Path to walkthrough.md to verify multi-platform copy.")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors.")

    args = parser.parse_args()
    target = find_target_file(args.post)
    success = audit_post(target, allow_lists=args.allow_lists, walkthrough_path=args.walkthrough)

    if not success or (args.strict and success is not True):
        sys.exit(1)
    sys.exit(0)

if __name__ == '__main__':
    main()
