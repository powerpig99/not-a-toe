#!/usr/bin/env python3
"""Re-embed a post's NotebookLM prompt files into its walkthrough.

Replaces the fenced ```text block that follows the "### Audio Dialogue" and
"### Video Monologue" headings in the walkthrough with the current contents of
notebooklm-auto/prompts/<slug>_zh.txt and <slug>_video_zh.txt.

Usage: python3 scripts/sync-walkthrough-prompts.py <slug> <walkthrough.md>
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOCKS = [("### Audio Dialogue", "{slug}_zh.txt"), ("### Video Monologue", "{slug}_video_zh.txt")]


def replace_block(text: str, header: str, body: str) -> str:
    h = text.index(header)
    start = text.index("```text\n", h) + len("```text\n")
    end = text.index("\n```\n", start)
    return text[:start] + body + text[end:]


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__.strip())
        return 2
    slug, wt = sys.argv[1], Path(sys.argv[2])
    text = wt.read_text(encoding="utf-8")
    for header, pattern in BLOCKS:
        pf = ROOT / "notebooklm-auto" / "prompts" / pattern.format(slug=slug)
        if not pf.is_file():
            print(f"skip: {pf.relative_to(ROOT)} missing")
            continue
        try:
            body = pf.read_text(encoding="utf-8").replace("\r\n", "\n").rstrip("\n")
            text = replace_block(text, header, body)
            print(f"synced: {header} <- {pf.relative_to(ROOT)} ({pf.stat().st_size} bytes)")
        except ValueError:
            print(f"error: no fenced ```text block found after '{header}' in {wt}")
            return 1
    wt.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
