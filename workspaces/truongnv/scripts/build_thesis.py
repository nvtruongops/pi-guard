#!/usr/bin/env python3
"""Disabled: thesis source chapters were withdrawn pending evidence review."""

import sys


def main() -> int:
    print(
        "Thesis build is paused: replace and review the withdrawn chapter drafts "
        "against current evidence before generating a thesis."
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
