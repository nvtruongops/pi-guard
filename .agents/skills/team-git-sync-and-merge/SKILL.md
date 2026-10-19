---
name: team-git-sync-and-merge
description: Single-maintainer Git workflow for the PI-Guard repository, with a local-only private workspace and protected academic records.
---

# PI-Guard single-maintainer Git workflow

This repository is maintained by Nguyễn Văn Trường (`nvtruongops`). The academic capstone roster and historical team contributions remain in the official records but do not define Git access.

## Working tree policy

- Keep private notes, drafts, and experiments in `workspaces/truongnv/`, which is ignored by Git.
- Put requested deliverables in their official tracked locations outside `workspaces/`.
- Do not recreate the retired `workspaces/ducnq/`, `workspaces/vietpmh/`, or `workspaces/phuongddd/` directories.
- Keep `CAPSTONE PROJECT REGISTER.md` and `docs/fpt_capstone_guide/` read-only.

## Change workflow

1. Start from an up-to-date `main` and create a task branch, for example `codex/update-repository-docs`.
2. Make the smallest change that satisfies the task and keep generated research artifacts out of tracked deliverables unless the task explicitly calls for them.
3. Review the changed paths and run the required local validation:

   ```sh
   python Final-Report/scripts/audit_workspace_boundaries.py --mode all
   python Final-Report/scripts/validate_local.py --mode fast
   ```

4. Commit only the intended tracked files. Review the diff before opening or merging a pull request.

## Privacy limit

The ignore rule prevents future versions of `workspaces/truongnv/` from being added. It does not erase versions already present in Git history. History removal requires a separate, coordinated rewrite and is not performed by this routine.
