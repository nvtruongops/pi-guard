# PI-Guard documentation portal source

This directory is the checked-in source for the MkDocs Material GitHub Pages site. The deployment configuration is the repository-root mkdocs.yml; this folder does not have a separate MkDocs configuration.

The [home page](index.md) and [ingress architecture overview](models/ingress_architecture.md) describe the current Review 2 status and the proposed L1/L2/L3/API flow. The architecture is a proposal; the seed-42 cascade experiment is one local run and does not establish final project KPI acceptance or a deployed service.

The homepage is maintained in the checked-in index.md. Final-Report/scripts/build_docs_portal.py copies mapped topic content and refreshes static assets while preserving existing checked-in pages. To preview and check the portal from the repository root, run:

    python Final-Report/scripts/build_docs_portal.py
    mkdocs serve
    mkdocs build --strict

The root configuration excludes this README from the published site. The immutable FPT guide is outside the portal and must remain out of the published source.
