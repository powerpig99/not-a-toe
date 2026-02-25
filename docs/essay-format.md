# Essay Formatting Guide

Use this exact spec when asking an LLM to draft essays for this site.

## Copy-Paste Prompt

```markdown
You are writing one essay markdown file for the Not a ToE site.

Output rules (strict):
1. Output only markdown content, no explanations.
2. First line must be exactly: `# <Title>`.
3. After the title, write a summary lead of 1–3 complete sentences in plain prose.
4. Do not use `##` or `###` until after that summary lead.
5. Avoid non-sentence blocks before first `##`/`###` (no lists, no blockquotes, no horizontal rules, no code fences).
6. Main body starts at first `##` heading.
7. Use only simple markdown: headings, paragraphs, links `[text](url)`, emphasis `*`/`**`, quotes `>`, lists (`-` and `1.`), horizontal rule (`---`) only in body.
8. Keep quotes properly closed; punctuation inside quotes is allowed.
9. No frontmatter (`---` metadata), no HTML.
10. End with a newline.
```

## Why This Works

- The index/meta summary is extracted from content before the first `##` or `###`.
- The extractor keeps up to 3 sentences and skips non-sentence blocks.
- Keeping the opening as pure prose makes previews deterministic on index and X cards.
