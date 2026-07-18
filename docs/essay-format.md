# Essay Formatting Guide

Use this exact spec when drafting essays for this site. For full authoring workflow (voice, cross-links, cover, ship, Substack), see [`content/posts/README.md`](../content/posts/README.md). Sleep audits living trackers via [`docs/local-memory.md`](local-memory.md).

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
12. Internal cross-links use relative form only: `[title](../other-slug/)`. Do not use absolute site URLs in the source file.
13. Fold any seed observation (tweet, note) into the prose so the essay stands alone; do not depend on a deletable external post link.
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

## Cross-links

- In **source** (`content/posts/`): `[axis name](../slug/)`.
- Pointers only — restore an axis; do not restate the linked essay.
- For Substack paste, project absolute URLs with the export script — see [`docs/export-for-substack.md`](export-for-substack.md).

## Optional Title Image

Place a landscape cover at `assets/covers/<slug>.jpg` (or `.jpeg` / `.png` / `.webp`), matching the markdown filename without extension. Target **1280×720**. The build:

- copies it to `public/covers/`
- renders it above the essay title
- uses it for `og:image` / Twitter large-image card when present

**Style rule:** each new cover must use a visual style not already in the set. Track families, inventory, unused candidates, and the update workflow in [`assets/covers/STYLES.md`](../assets/covers/STYLES.md). Read that file before generating; update it after installing a new cover.
