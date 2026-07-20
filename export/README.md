# export/ (generated, not source)

Markdown and JSON here are **projections** of `content/posts/` for external surfaces (Substack paste, X Article dry-run/receipts). Generated files are gitignored; only this pointer is tracked.

**Do not edit files in this folder as canon.** Edit `content/posts/<slug>.md`, then re-export.

```bash
# Substack / absolute markdown
node scripts/export-absolute-md.mjs <slug>
node scripts/export-absolute-md.mjs <slug> --stdout | pbcopy

# X Article dry-run payload / receipts
node scripts/publish-x-article.mjs <slug>
node scripts/publish-x-article.mjs <slug> --draft
```

Workflows: [`docs/export-for-substack.md`](../docs/export-for-substack.md) · [`docs/export-for-x-article.md`](../docs/export-for-x-article.md).
