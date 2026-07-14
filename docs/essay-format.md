# Essay Formatting Guide

Use this exact spec when asking an LLM to draft essays for this site.

## Copy-Paste Prompt

```markdown
You are writing one essay markdown file for the Not a ToE site.

Output rules (strict):
1. Output only markdown content, no explanations.
2. First line must be exactly: `# <Title>`.
3. After the title, write exactly one complete sentence as the subtitle — the essence of the essay in a single line of plain prose.
4. After the subtitle, write a lead of 2–4 complete sentences summarizing the argument (plain prose, not a restatement of the subtitle alone).
5. Do not use `##` or `###` until after that subtitle + lead.
6. Avoid non-sentence blocks before first `##`/`###` (no lists, no blockquotes, no horizontal rules, no code fences).
7. Main body starts at first `##` heading.
8. Use only simple markdown: headings, paragraphs, links `[text](url)`, emphasis `*`/`**`, quotes `>`, lists (`-` and `1.`), horizontal rule (`---`) only in body.
9. Keep quotes properly closed; punctuation inside quotes is allowed.
10. No frontmatter (`---` metadata), no HTML.
11. End with a newline.
```

## Opening Structure

```text
# Title

<one-sentence subtitle>

<lead: a few summary sentences>

## First body section
...
```

## Why This Works

- The build treats the first sentence before the first `##`/`###` as the **subtitle** (rendered under the title on the essay page; used for index excerpt and meta description).
- The following sentences before the first subsection are the **lead** (kept in the essay body as the opening paragraph).
- Keeping the opening as pure prose makes previews deterministic on index and X cards.

## Optional Title Image

Place a landscape cover at `assets/covers/<slug>.jpg` (or `.jpeg` / `.png` / `.webp`), matching the markdown filename without extension. The build:

- copies it to `public/covers/`
- renders it above the essay title
- uses it for `og:image` / Twitter large-image card when present
