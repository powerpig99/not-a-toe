# export/ (generated, not source)

**One projection:** absolute-link markdown from `content/posts/` for Substack and X Article paste. Same file for both. Gitignored; this pointer is tracked.

```bash
node scripts/export-absolute-md.mjs <slug>
# → export/<slug>.md
```

**Generate after live is required** on every essay ship (“finish the rest”). **Paste** into Substack / X is operator-only. Do not skip generation because paste might wait.

Do not edit files here as canon. Edit `content/posts/<slug>.md`, then re-export. Guide: [`docs/export-for-substack.md`](../docs/export-for-substack.md). Full ship: [`content/posts/README.md`](../content/posts/README.md) § Ship checklist.

Parked X Articles API receipts (if any) are not a second paste export — see [`docs/export-for-x-article.md`](../docs/export-for-x-article.md).
