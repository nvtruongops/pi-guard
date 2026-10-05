# Repository contribution guide

## Maintainer

Nguyễn Văn Trường (`nvtruongops`) is the sole current maintainer and publisher of this Git repository. Tracked reports in `Final-Report/` and `Github-Page/` summarize the capstone group's progress and research outcomes as consolidated by the leader. Names and assignments in those reports describe project activity; they do not indicate current Git contributors. Historical Git commit records remain unchanged.

## Working files and deliverables

- `workspaces/truongnv/` is a local-only directory ignored by Git. Do not force-add its contents.
- Put reports and artifacts intended for review, collaboration, or publication in their task-designated tracked locations outside `workspaces/`, such as `Final-Report/` or `Github-Page/`.
- Keep literature claims, local empirical results, and project proposals distinct, with the required sources and provenance.
- The former `workspaces/ducnq/`, `workspaces/vietpmh/`, and `workspaces/phuongddd/` folders are retired.

## Change workflow

1. Start from an up-to-date `main` and use a task-specific branch, for example `codex/update-report-index`.
2. Review the changed paths and run the local checks before committing:

   ```sh
   python Final-Report/scripts/audit_workspace_boundaries.py --mode all
   python Final-Report/scripts/validate_local.py --mode fast
   ```

3. Commit only the intended tracked files. Keep `CAPSTONE PROJECT REGISTER.md` and `docs/fpt_capstone_guide/` read-only under Rule 01.

The ignore rule prevents future additions; it does not remove earlier versions from Git history. GitHub permissions and repository visibility are managed in the repository settings.
