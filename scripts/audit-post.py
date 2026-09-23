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
  1. Title and subtitle separation (clean `# Title` without compound delimiters, single-sentence `*Subtitle*` on Line 3, narrative lead on Line 5+)
  2. Prose over lists (flags lists outside mermaid; reminder to write continuous prose unless necessary)
  3. Historical Mermaid inline dark-theme styling (#161b22, #0d1117, semantic color borders)
  4. Bilingual diagram parallelism (Chinese/English paired diagrams)
  5. Relative internal cross-links resolution (all ../slug/ exist; no absolute URLs)
  6. Banned words & essentialist cliches (0 tolerance for cognitive crutches)
  7. LaTeX syntax prohibition (0 raw $ or $$; Unicode math only)
  8. Multi-platform publishing copy in walkthrough (Spotify ZH/EN, WeChat Video, X EN)
  9. Companion NotebookLM prompts (canonical opening, monologue script, and concise bounds: 2-4 opening turns, < 8.5KB)
  10. Mandatory companion cover art (assets/covers/<slug>.(jpg|png|webp) present, non-empty, and registered in STYLES.md)

Usage:
  python3 scripts/audit-post.py [slug_or_path]
  python3 scripts/audit-post.py --allow-lists [slug_or_path]
  python3 scripts/audit-post.py --walkthrough <path_to_walkthrough.md>
"""

import sys
import os
import re
import struct
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

def get_image_size(file_path):
    """Pure-Python image dimension extraction for JPEG and PNG without external dependencies."""
    try:
        from PIL import Image
        with Image.open(file_path) as img:
            return img.size
    except Exception:
        pass

    try:
        with open(file_path, 'rb') as f:
            data = f.read(24)
            if data.startswith(b'\x89PNG\r\n\x1a\n') and len(data) >= 24:
                w, h = struct.unpack('>II', data[16:24])
                return w, h
            elif data.startswith(b'\xff\xd8'):
                f.seek(2)
                while True:
                    marker_prefix = f.read(1)
                    while marker_prefix and marker_prefix != b'\xff':
                        marker_prefix = f.read(1)
                    if not marker_prefix:
                        return None
                    marker = f.read(1)
                    while marker == b'\xff':
                        marker = f.read(1)
                    if not marker:
                        return None
                    m = marker[0]
                    if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                        f.read(3)  # len (2) + precision (1)
                        h, w = struct.unpack('>HH', f.read(4))
                        return w, h
                    elif m in (0xD9, 0xDA):
                        return None
                    else:
                        len_bytes = f.read(2)
                        if len(len_bytes) < 2:
                            return None
                        l = struct.unpack('>H', len_bytes)[0]
                        f.seek(l - 2, 1)
    except Exception:
        pass
    return None

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

    # 1. Title and subtitle separation audit
    title_sub_clean = True
    if lines:
        first_line = lines[0].strip()
        if not first_line.startswith('# '):
            errors.append(f"Post must start with '# <Title>' on line 1. Found: '{first_line[:50]}'")
            title_sub_clean = False
        else:
            title_text = first_line[2:].strip()
            # Flag compound subtitle delimiters in the title
            delim_match = re.search(r'[：:]|\s+[-—–—]{1,2}\s+', title_text)
            if delim_match:
                errors.append(
                    f"Compound subtitle delimiter '{delim_match.group().strip() or delim_match.group()}' found in title: '{title_text}'. "
                    f"Rule: Main title must be concise and punchy without compound colons or dashes. Move explanatory clauses to Line 3 subtitle."
                )
                title_sub_clean = False

            # Check bilingual title symmetry if bilingual prose is present
            has_zh_title = bool(re.search(r'[\u4e00-\u9fff]', title_text))
            has_en_title = bool(re.search(r'[a-zA-Z]{3,}', title_text))
            if has_zh_title and has_en_title and '/' not in title_text:
                errors.append(f"Bilingual title must separate Chinese and English titles with ' / ': '{title_text}'")
                title_sub_clean = False

        # Subtitle check (Line 3 or first non-empty line after title)
        sub_line_idx = -1
        for idx in range(1, min(len(lines), 10)):
            if lines[idx].strip():
                sub_line_idx = idx
                break

        if sub_line_idx == -1:
            errors.append("Missing subtitle. Expected single-line italic subtitle on Line 3.")
            title_sub_clean = False
        else:
            sub_line = lines[sub_line_idx].strip()
            if sub_line_idx != 2:
                warnings.append(f"Subtitle is on Line {sub_line_idx + 1}; expected Line 3 immediately after an empty Line 2.")

            # Must be explicit single-line italic
            is_italic = bool(re.match(r'^(\*|_)[^*_]+(\*|_)$', sub_line))
            if not is_italic:
                errors.append(
                    f"Subtitle must be an explicit single-line italic string (`*<Subtitle>*`). Found: '{sub_line[:60]}...'"
                )
                title_sub_clean = False
            else:
                clean_sub = re.sub(r'^[*_]+|[*_]+$', '', sub_line).strip()
                # Check for bloated wall-of-text synopsis in subtitle
                if len(clean_sub) > 160:
                    errors.append(
                        f"Subtitle length ({len(clean_sub)} chars) exceeds concise single-sentence standard (<= 160 chars). "
                        f"Rule: Subtitle is strictly one concise sentence of essence. Move extended synopsis into lead prose."
                    )
                    title_sub_clean = False

                # Check for multi-sentence synopsis in subtitle
                parts = clean_sub.split('/')
                has_multi_sentence = False
                for part in parts:
                    p_text = part.strip()
                    # If Chinese part has internal period '。'
                    if re.search(r'。[^$]', p_text):
                        has_multi_sentence = True
                    # If English part has internal period followed by space and capital letter (ignoring abbreviations)
                    clean_en = re.sub(r'\b(?:vs|e\.g|i\.e|etc|dr|mr|ms)\.', '', p_text, flags=re.IGNORECASE)
                    if re.search(r'\.\s+[A-Z]', clean_en):
                        has_multi_sentence = True
                if has_multi_sentence:
                    errors.append(
                        f"Subtitle contains multiple sentences: '{clean_sub}'. "
                        f"Rule: Subtitle must be a single concise sentence; narrative arguments belong in the lead prose."
                    )
                    title_sub_clean = False

            # Check lead prose starts after subtitle
            lead_idx = -1
            for idx in range(sub_line_idx + 1, min(len(lines), sub_line_idx + 5)):
                if lines[idx].strip():
                    lead_idx = idx
                    break
            if lead_idx != -1:
                lead_line = lines[lead_idx].strip()
                if lead_line.startswith('#'):
                    errors.append("Missing lead prose: Heading encountered immediately after subtitle. Expected 2–4 sentences of narrative lead.")
                    title_sub_clean = False
                elif lead_line.startswith(('```', '-', '*', '>')):
                    warnings.append(f"Lead starts with non-prose line: '{lead_line[:40]}'. Lead should be narrative prose.")

        if title_sub_clean:
            passes.append("Title and subtitle separation check (clean `# Title` without delimiters, single-sentence `*Subtitle*` on Line 3)")

    # 2. Banned words audit
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
    abs_matches = re.findall(r'https?://(?:powerpig99\.github\.io/not-a-toe)/posts/([a-zA-Z0-9_-]+)/?', content)
    if abs_matches:
        errors.append(f"Hardcoded absolute site URLs found for: {abs_matches}. Internal links MUST be relative: [title](../slug/).")
    else:
        passes.append("Link locality check (no hardcoded absolute site URLs)")

    # Prohibit any fake/hallucinated domain in post content
    fake_domains = re.findall(r'https?://(?:www\.)?not-?a-?toe\.(?:org|com|net|io|ai|xyz)', content, re.IGNORECASE)
    if fake_domains:
        errors.append(f"Prohibited fake/hallucinated site domain detected ({fake_domains}). Canonical site is https://powerpig99.github.io/not-a-toe/; internal links MUST be relative: [title](../slug/).")

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

        # Bilingual parallelism & strict language separation check
        first_line = lines[0] if lines else ""
        is_bilingual_title = bool(re.search(r'[\u4e00-\u9fff]', first_line) and '/' in first_line and re.search(r'[a-zA-Z]{3,}', first_line))
        has_zh = bool(re.search(r'[\u4e00-\u9fff]', content))
        # Detect presence of substantive English prose paragraphs
        en_paragraphs = [p for p in content.split('\n\n') if len(p.strip()) > 80 and not p.strip().startswith(('```', '#', '|', '*', '-')) and len(re.findall(r'[a-zA-Z]', p)) > 0.7 * len(p.strip())]
        has_en_prose = len(en_paragraphs) >= 3
        
        if is_bilingual_title or (has_zh and has_en_prose):
            if len(mermaid_blocks) % 2 != 0:
                warnings.append(f"Bilingual diagram count is odd ({len(mermaid_blocks)}). Ensure every Chinese diagram has its exact English parallel counterpart.")
            else:
                passes.append(f"Bilingual diagram parallelism ({len(mermaid_blocks) // 2} paired diagrams)")

            if not has_en_prose:
                errors.append("Bilingual post has bilingual title/headings but lacks English prose paragraphs.")
            else:
                passes.append("Bilingual prose check (both Chinese and English prose present)")

            # Check strict language separation in diagrams ("中文的归中文，英文的归英文")
            allowed_acronyms = {'DNA', 'API', 'AI', 'LLM', 'CPU', 'GPU', 'TOE', 'VR'}
            diagram_lang_issues = []
            for idx, block in enumerate(mermaid_blocks, 1):
                block_has_zh = bool(re.search(r'[\u4e00-\u9fff]', block))
                if block_has_zh:
                    # In Chinese diagram, flag residual English subtitles like <br/>English Words
                    en_subs = re.findall(r'<br/>\s*([A-Za-z][A-Za-z0-9\s\-_/\'\.,:;]{3,})', block)
                    disallowed = [s.strip() for s in en_subs if s.strip().upper() not in allowed_acronyms]
                    if disallowed:
                        diagram_lang_issues.append(f"Diagram {idx} (Chinese) has residual English subtitles: {disallowed[:3]}")
                else:
                    # In English diagram, must have no Chinese
                    if re.search(r'[\u4e00-\u9fff]', block):
                        diagram_lang_issues.append(f"Diagram {idx} (English) contains Chinese characters")

            if diagram_lang_issues:
                warnings.append(f"Strict language separation in diagrams ('中文的归中文，英文的归英文'): {'; '.join(diagram_lang_issues)}")
            else:
                passes.append("Strict language separation in diagrams (pure Chinese in Chinese diagrams, pure English in English diagrams)")

        # Strictly vertical layout check (prevent horizontal side-by-side subgraphs)
        horizontal_layout_issues = []
        for idx, block in enumerate(mermaid_blocks, 1):
            if re.search(r'\bgraph\s+LR\b', block, re.IGNORECASE):
                horizontal_layout_issues.append(f"Diagram {idx} uses horizontal flow ('graph LR'). Rule: use strictly vertical 'graph TD' / 'flowchart TD'.")
            
            subgraphs = re.findall(r'\bsubgraph\s+([A-Za-z0-9_-]+)', block)
            if len(subgraphs) >= 2:
                # Check for direction TB
                if 'direction TB' not in block and 'direction TD' not in block:
                    horizontal_layout_issues.append(f"Diagram {idx} has {len(subgraphs)} subgraphs but lacks 'direction TB'. Subgraphs must enforce vertical node flow.")
                
                # Check for inter-subgraph vertical connection (e.g. Node1 ===> Node2 or Subgraph link)
                has_inter_subgraph_edge = bool(re.search(r'===>|-->|-\.->', block.split('end')[-1])) or ('===>' in block)
                if not has_inter_subgraph_edge:
                    horizontal_layout_issues.append(f"Diagram {idx} has {len(subgraphs)} disconnected subgraphs without vertical connecting arrow (e.g. UpperNode ===> LowerNode), which causes horizontal side-by-side layout.")

        if horizontal_layout_issues:
            errors.append(f"Mermaid horizontal layout violations: {'; '.join(horizontal_layout_issues)}")
        else:
            passes.append(f"Mermaid vertical layout check ({len(mermaid_blocks)} diagrams adhere to strictly vertical mobile-friendly top-down flow)")
    else:
        passes.append("Mermaid check (no diagrams in this post)")

    # 7. Walkthrough copy check (if walkthrough provided or discovered)
    explicit_walkthrough = bool(walkthrough_path)
    if not walkthrough_path:
        brain_base = Path("/Users/jingliang/.gemini/antigravity/brain")
        active_walkthrough = brain_base / "f0e7480f-958a-4183-80da-595bc3ad23df" / "walkthrough.md"
        if active_walkthrough.is_file():
            walkthrough_path = active_walkthrough
        elif brain_base.is_dir():
            candidates = sorted(brain_base.glob("*/walkthrough.md"), key=lambda p: p.stat().st_mtime, reverse=True)
            if candidates:
                walkthrough_path = candidates[0]

    if walkthrough_path and Path(walkthrough_path).is_file():
        with open(walkthrough_path, 'r', encoding='utf-8') as wf:
            w_content = wf.read()

        # If walkthrough was auto-discovered, verify it actually belongs to this post
        expected_canonical_url = f"https://powerpig99.github.io/not-a-toe/posts/{slug}/"
        if not explicit_walkthrough and expected_canonical_url not in w_content:
            w_content = None

        if w_content:
            missing_platforms = []
            for platform_name, patterns in REQUIRED_WALKTHROUGH_SECTIONS:
                if not any(pat in w_content for pat in patterns):
                    missing_platforms.append(platform_name)

            if missing_platforms:
                warnings.append(f"Walkthrough missing required sections for: {missing_platforms}")
            else:
                passes.append("Walkthrough copy check (NotebookLM Prompts, Spotify ZH/EN, WeChat Video, X EN all present)")

            # Verify that all 4 platform copies include the exact canonical post URL
            expected_canonical_url = f"https://powerpig99.github.io/not-a-toe/posts/{slug}/"
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
                    if expected_canonical_url not in sec_text:
                        missing_url_platforms.append(name)

            if missing_url_platforms:
                errors.append(f"Walkthrough platform copies missing exact canonical live link ({expected_canonical_url}): {missing_url_platforms}. Must use exact URL with trailing slash.")
            else:
                passes.append("Walkthrough platform copy links check (all 4 platform copies include exact canonical post URL)")

            # Strictly prohibit any fake/hallucinated domain in walkthrough
            fake_walkthrough_domains = re.findall(r'https?://(?:www\.)?not-?a-?toe\.(?:org|com|net|io|ai|xyz)', w_content, re.IGNORECASE)
            if fake_walkthrough_domains:
                errors.append(f"Fake/hallucinated domain detected in walkthrough ({fake_walkthrough_domains}). Canonical site is strictly: https://powerpig99.github.io/not-a-toe/")

            # Specific check for WeChat Video Channels: Short Title (<= 16 chars) and Topic Terms (#...)
            wechat_patterns = ['WeChat Video Channels', '微信视频号']
            wechat_found_pos = -1
            for pat in wechat_patterns:
                pos = w_content.find(pat)
                if pos != -1:
                    wechat_found_pos = pos
                    break
            if wechat_found_pos != -1:
                next_header = re.search(r'\n#{2,3}\s+', w_content[wechat_found_pos + 10:])
                end_pos = (wechat_found_pos + 10 + next_header.start()) if next_header else len(w_content)
                wechat_sec = w_content[wechat_found_pos:end_pos]

                # 1. Short Title check:
                title_match = re.search(r'\*\*(?:(?:Short\s+)?Title|视频标题(?:文案)?)(?:\s*\([^)]*\))?\*\*[:：]\s*(.+)', wechat_sec, re.IGNORECASE)
                if not title_match:
                    errors.append("Walkthrough WeChat Video Channels copy missing short title. Format: '**Title (<= 16字)**: <短标题>'")
                else:
                    raw_title = title_match.group(1).strip()
                    clean_title = re.sub(r'^[`"\'“”‘’]+|[`"\'“”‘’]+$', '', raw_title).strip()
                    title_len = len(clean_title)
                    if title_len == 0:
                        errors.append("Walkthrough WeChat Video Channels title is empty.")
                    elif title_len > 16:
                        errors.append(f"Walkthrough WeChat Video Channels title exceeds 16 Chinese characters ({title_len} chars > 16 max): '{clean_title}'. WeChat Video Channel cards strictly truncate titles longer than 16 characters.")
                    else:
                        passes.append(f"Walkthrough WeChat Video Channels short title check ('{clean_title}', {title_len}/16 chars)")

                # 2. Topic terms check:
                tags = re.findall(r'#([^\s#]+)', wechat_sec)
                if len(tags) < 2:
                    errors.append(f"Walkthrough WeChat Video Channels copy missing topic terms (found {len(tags)}; requires at least 3-5 tags, e.g. #话题1 #话题2 #话题3).")
                else:
                    passes.append(f"Walkthrough WeChat Video Channels topic terms check ({len(tags)} tags found: {' '.join('#' + t for t in tags[:5])})")

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

    # 9. Companion Cover Art audit
    covers_dir = root / 'assets' / 'covers'
    cover_extensions = ['.jpg', '.png', '.webp']
    found_cover = None
    for ext in cover_extensions:
        candidate = covers_dir / f"{slug}{ext}"
        if candidate.is_file():
            found_cover = candidate
            break

    if not found_cover:
        errors.append(f"Missing companion cover image: expected assets/covers/{slug}.jpg (or .png/.webp). Every post must have an installed cover art.")
    else:
        file_size = found_cover.stat().st_size
        if file_size == 0:
            errors.append(f"Cover art file is 0 bytes (empty): assets/covers/{found_cover.name}")
        else:
            file_size_kb = file_size / 1024
            dim = get_image_size(found_cover)
            dim_str = f"{dim[0]}x{dim[1]}" if dim else "unknown dimensions"

            # Aspect ratio advisory
            if dim:
                w, h = dim
                ratio = w / h
                if w < 1000 or h < 400:
                    warnings.append(f"Cover image resolution ({w}x{h}) is lower than standard. Recommended: 1344x576 (21:9) or 1280x576 (20:9).")
                elif not (1.7 <= ratio <= 2.5):
                    warnings.append(f"Cover image aspect ratio ({ratio:.2f}:1) deviates from ultra-wide landscape standard (21:9 ~ 2.33:1 or 20:9 ~ 2.22:1).")

            # STYLES.md registration check
            styles_file = covers_dir / 'STYLES.md'
            if styles_file.is_file():
                styles_text = styles_file.read_text(encoding='utf-8')
                if slug not in styles_text:
                    warnings.append(f"Cover for '{slug}' is not yet registered in assets/covers/STYLES.md. Please document its style family and inventory entry.")
                else:
                    passes.append("Cover art registered in STYLES.md")

            passes.append(f"Companion cover art check (assets/covers/{found_cover.name} present, {file_size_kb:.1f} KB, {dim_str})")

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
