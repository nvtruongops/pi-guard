#!/usr/bin/env python3
"""Withdrawn probe; it did not evaluate JailbreakBench defense effectiveness."""


def main() -> int:
    print(
        "This runner is withdrawn. Its former setup applied a prompt-injection "
        "classifier to behavior-goal text and mislabeled flags as jailbreak detection."
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
