# export/ (generated, not source)

Markdown and JSON here are **projections** of `content/posts/` for external surfaces (Substack / X Article paste, optional X dry-run receipts). Generated files are gitignored; only this pointer is tracked.

**Do not edit files in this folder as canon.** Edit `content/posts/<slug>.md`, then re-export.

```bash
# Default: absolute markdown → open in MacDown → copy rendered preview
node scripts/export-absolute-md.mjs <slug>
open -a MacDown export/<slug>.md

# Optional raw markdown to clipboard
node scripts/export-absolute-md.mjs <slug> --stdout | pbcopy

# Optional RTF clipboard (escape hatch without MacDown; keeps title)
node scripts/export-absolute-md.mjs <slug> --rich

# X Article API dry-run / receipts (parked path)
node scripts/publish-x-article.mjs <slug>
node scripts/publish-x-article.mjs <slug> --draft
```

Workflows: [`docs/export-for-substack.md`](../docs/export-for-substack.md) · [`docs/export-for-x-article.md`](../docs/export-for-x-article.md).
