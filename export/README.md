# export/ (generated, not source)

Markdown here is a **projection** of `content/posts/` with absolute links for Substack and other paste targets. Generated files are gitignored; only this pointer is tracked.

**Do not edit files in this folder as canon.** Edit `content/posts/<slug>.md`, then re-export.

```bash
node scripts/export-absolute-md.mjs <slug>
node scripts/export-absolute-md.mjs <slug> --stdout | pbcopy
```

Full workflow: [`docs/export-for-substack.md`](../docs/export-for-substack.md).
