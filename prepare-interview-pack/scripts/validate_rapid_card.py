#!/usr/bin/env python3
"""Deterministic checks for a 30-minute interview rapid-review card."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from validate_pack import contains, find_duplicate_major_headings, find_spoken_provenance_leaks, section


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("card", type=Path)
    args = parser.parse_args()

    if not args.card.is_file():
        print(f"ERROR: file not found: {args.card}")
        return 2

    text = args.card.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []

    required = {
        "30-minute schedule": [r"30\s*分钟", r"30-minute"],
        "60-second introduction": [r"60\s*秒", r"60-second"],
        "primary story": [r"主项目", r"首选项目", r"primary story"],
        "backup story": [r"备用项目", r"备选项目", r"backup story"],
        "three gaps": [r"三个缺口", r"3\s*(?:个|大)?缺口", r"three gaps"],
        "five P0 questions": [r"五道\s*P0", r"5\s*道\s*P0", r"five P0"],
        "interviewer questions": [r"问面试官", r"反问", r"questions for the interviewer"],
        "fact boundaries": [r"事实红线", r"事实边界", r"fact.*boundar"],
        "last updated": [r"最后更新", r"last updated"],
    }
    for label, patterns in required.items():
        if not contains(text, patterns):
            errors.append(f"missing {label}")

    interviewer = section(text, [r"问面试官", r"反问", r"questions for the interviewer"])
    interviewer_count = len(re.findall(r"^\s*\d+[.、．]\s+", interviewer, re.M))
    if interviewer_count < 3:
        errors.append(f"only {interviewer_count} interviewer questions; need at least 3")

    leaks = find_spoken_provenance_leaks(text)
    if leaks:
        errors.append(f"{len(leaks)} spoken passage(s) expose source provenance or claim status")

    duplicates = find_duplicate_major_headings(text)
    if duplicates:
        errors.append("duplicate major heading(s): " + ", ".join(duplicates))

    compact_length = len(re.sub(r"\s+", "", text))
    if compact_length > 4500:
        warnings.append(
            f"rapid-review card has {compact_length} non-whitespace characters; consider shortening to 4500 or fewer"
        )

    print("PASS" if not errors else "FAIL")
    for item in errors:
        print(f"ERROR: {item}")
    for item in warnings:
        print(f"WARNING: {item}")
    print(f"Characters: {compact_length}; interviewer questions: {interviewer_count}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
