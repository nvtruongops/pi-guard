# Rule 07: Single Maintainer & Local Workspace Privacy

> This rule defines current repository ownership and working-file placement. Tracked capstone reports may describe the progress of all team members while being maintained and published by the leader. The rule does not rewrite academic or historical Git records.

## Repository ownership

- Nguyễn Văn Trường (`nvtruongops`) is the sole current maintainer and publisher of this Git repository.
- He consolidates and publishes the group's progress reports and research outcomes. Member names in those reports are project records, not current repository contributors.
- GitHub write/admin access is limited to `nvtruongops`; keep repository collaborator permissions aligned with this rule.
- The former member workspaces `workspaces/ducnq/`, `workspaces/vietpmh/`, and `workspaces/phuongddd/` are retired. Do not recreate them.
- The academic team roster in the project register and capstone reports remains an academic record; it does not define current Git access.

## Private working files and deliverables

- `workspaces/truongnv/` is a local-only working directory covered by the root `.gitignore`. Do not use `git add -f` to publish its contents.
- Put deliverables intended for review, collaboration, or publication in their task-designated tracked locations outside `workspaces/`, such as `Final-Report/` or `Github-Page/`.
- Local notes, drafts, and experiments are not accepted project evidence until the required sources, provenance, validation, and scope are recorded in a tracked deliverable.

## Protected files

- `CAPSTONE PROJECT REGISTER.md` and `docs/fpt_capstone_guide/` remain strictly read-only under Rule 01.
- Run `python Final-Report/scripts/audit_workspace_boundaries.py` to check changed paths against these protected locations.
- Before committing, run `python Final-Report/scripts/validate_local.py --mode fast`.
