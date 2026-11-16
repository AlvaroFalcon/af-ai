---
name: check-all
description: Run every check CI runs ({{LIST_OF_CHECKS}}) with one summary. Use before every commit/push and whenever the user asks if things are green.
---

# check-all

Run from the repo root:

```bash
scripts/check_all.sh
```

- {{NOTES: optional --fix flag, tools that are skipped when missing locally but always run in CI}}
- The exit code is non-zero if anything failed. The tail of each failing check is printed above
  the summary.

When reporting, paste the summary table. If something fails, fix the cause; never skip or weaken a
test to get green. Don't push with a red summary.
