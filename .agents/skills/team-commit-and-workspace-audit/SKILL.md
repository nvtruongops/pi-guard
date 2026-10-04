---
name: team-commit-and-workspace-audit
description: Audits changed repository paths against the protected academic records in the single-maintainer PI-Guard repository.
---

# Repository change and workspace audit

This check protects immutable academic records. It no longer assigns file permissions by team member: Nguyễn Văn Trường (`nvtruongops`) is the sole repository maintainer, while the capstone team roster remains in academic records.

## Protected paths

Changes to either path are rejected:

- `CAPSTONE PROJECT REGISTER.md`
- `docs/fpt_capstone_guide/`

Personal files under `workspaces/truongnv/` are ignored by Git. Do not force-add them. Put deliverables intended for review or publication in tracked locations outside `workspaces/`.

## Run the audit

Check all working-tree and staged changes:

```sh
python Final-Report/scripts/audit_workspace_boundaries.py --mode all
```

Check only staged changes before committing:

```sh
python Final-Report/scripts/audit_workspace_boundaries.py --mode staged
```

Check the last commit or a commit range:

```sh
python Final-Report/scripts/audit_workspace_boundaries.py --mode last_commit
python Final-Report/scripts/audit_workspace_boundaries.py --mode commit_range --commit-range origin/main..HEAD
```

Install the local pre-commit validation hook when needed:

```sh
python Final-Report/scripts/audit_workspace_boundaries.py --install-hook
```

The normal repository pre-commit workflow calls `Final-Report/scripts/validate_local.py --mode pre-commit`. Before submitting a commit, run `python Final-Report/scripts/validate_local.py --mode fast`.

## Failure handling

If the audit reports `IMMUTABLE_FILE_VIOLATION`, restore the protected path and rerun the audit. Other changed paths are allowed by this audit; task scope, academic evidence, and content validation still apply.

Ignoring `workspaces/truongnv/` affects future Git additions only. Existing copies in repository history are unaffected unless the history is separately rewritten.
