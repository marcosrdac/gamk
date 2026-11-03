---
work: 20261103_0057_localize-global-rules
branch: main
worktree: .
origin: user conversation
commit: 1369fb2
---

# Integrate local/global rule separation

Integrated the completed worktree with a fast-forward into `main`. GAMK
maintenance guidance now lives under `.ai/rules/`, while `global/` contains
optional personal context without mandatory entries. The duplicated global
context-loading rule was removed because the installed `AGENTS.md` already
defines that protocol.
