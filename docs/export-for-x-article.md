# Export for X Article

Living guide for putting a site post into an **X Article**. **Current path: absolute markdown → MacDown preview paste** — same as Substack. The Articles API path is **parked**.

| Related | Path |
|---------|------|
| **Active workflow** | [`docs/export-for-substack.md`](export-for-substack.md) — `export-absolute-md.mjs` → MacDown |
| Source posts | [`content/posts/`](../content/posts/) · authoring [`content/posts/README.md`](../content/posts/README.md) |
| Cover styles | [`assets/covers/STYLES.md`](../assets/covers/STYLES.md) |
| Parked API script | [`scripts/publish-x-article.mjs`](../scripts/publish-x-article.mjs) (kept; not the default) |

## Active path (paste)

X Article body accepts formatted paste the same way Substack does. Plain markdown does not auto-render — copy the **rendered** preview.

```bash
# After the post is live on the site
node scripts/export-absolute-md.mjs <slug>
open -a MacDown export/<slug>.md
```

Then in the X Article editor:

1. Set **title**.
2. **Paste** body from MacDown preview (⌘V) — not “Match Style.”
3. Upload cover from `assets/covers/<slug>.jpg` (20:9).
4. Publish when ready.

Full detail, flags, and failure modes: [`export-for-substack.md`](export-for-substack.md). Optional escape hatch: `--rich --no-title` for RTF clipboard without MacDown.

## Parked: Articles API

`scripts/publish-x-article.mjs` projects markdown → Draft.js `content_state` and can draft/publish via the X Articles API. That path is **parked** while operator paste works:

- No default ship step calls the API.
- Credentials, dry-run JSON, and `--draft` / `--publish` remain in the script for a later resume.
- Do not document API publish as the normal workflow until the operator unparks it.

If resuming API publish later: dry-run → inspect `export/<slug>.x-article.json` → `--draft` → review in X → publish. Official endpoints: [Articles introduction](https://docs.x.com/x-api/articles/introduction).

## Principle

**One source.** `content/posts/<slug>.md` stays relative. External surfaces get a disposable projection (absolute markdown → rendered paste now; API payload only if unparked). Never edit source for the editor; never treat `export/` as canon.
