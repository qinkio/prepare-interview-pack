#!/usr/bin/env python3
"""Deterministic structural checks for prepare-interview-pack Markdown output."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def contains(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, re.I | re.M) for pattern in patterns)


def section(text: str, heading_patterns: list[str]) -> str:
    lines = text.splitlines()
    start = None
    level = None
    for index, line in enumerate(lines):
        match = re.match(r"^(#+)\s+(.+)$", line)
        if match and any(re.search(pattern, match.group(2), re.I) for pattern in heading_patterns):
            start = index + 1
            level = len(match.group(1))
            break
    if start is None:
        return ""
    end = len(lines)
    for index in range(start, len(lines)):
        match = re.match(r"^(#+)\s+", lines[index])
        if match and len(match.group(1)) <= level:
            end = index
            break
    return "\n".join(lines[start:end])


def count_numbered_questions(text: str) -> int:
    target = section(text, [r"高概率.*问题", r"round-specific questions", r"面试问题", r"questions.*answers"])
    if not target:
        return 0
    headings = re.findall(r"^#{2,4}\s+(?:Q\s*)?\d+[.、．:]\s*.+", target, re.M | re.I)
    if headings:
        return len(headings)
    return len(re.findall(r"^\s*\d+[.、．]\s*.+[？?]\s*$", target, re.M))


def count_interviewer_questions(text: str) -> int:
    target = section(text, [r"问面试官", r"反问", r"questions for the interviewer"])
    return len(re.findall(r"^\s*\d+[.、．]\s+", target, re.M)) if target else 0


def find_spoken_provenance_leaks(text: str) -> list[tuple[int, str]]:
    """Find analyst-facing provenance or status language inside blockquoted speech."""
    patterns = [
        r"简历(?:中|里)?(?:记录|显示|写着|能确认)",
        r"(?:根据|按照)(?:我的)?简历",
        r"(?:工作)?资料(?:中)?(?:记录|显示|表明|证明|能证明)",
        r"(?:材料|文档)(?:中)?(?:记录|显示|表明|证明)",
        r"现有简历",
        r"`(?:Verified|Candidate-confirmed|Derived-safe|Confirm|Conflict|Inference|Do not use)`",
    ]
    combined = re.compile("|".join(f"(?:{pattern})" for pattern in patterns), re.I)
    leaks: list[tuple[int, str]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if re.match(r"^\s*>", line) and combined.search(line):
            leaks.append((line_number, line.lstrip("> ").strip()))
    return leaks


def find_duplicate_major_headings(text: str) -> list[str]:
    """Return repeated level-one or level-two headings after light normalization."""
    seen: dict[str, int] = {}
    duplicates: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^(#{1,2})\s+(.+)$", line)
        if not match:
            continue
        heading = re.sub(r"\s*\{[^}]+\}\s*$", "", match.group(2)).strip().casefold()
        seen[heading] = seen.get(heading, 0) + 1
        if seen[heading] == 2:
            duplicates.append(match.group(2).strip())
    return duplicates


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("handbook", type=Path)
    parser.add_argument("--mode", choices=["sprint", "standard", "deep"], default="standard")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not args.handbook.is_file():
        print(f"ERROR: file not found: {args.handbook}", file=sys.stderr)
        return 2

    text = args.handbook.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []

    provenance_leaks = find_spoken_provenance_leaks(text)
    if provenance_leaks:
        preview = "; ".join(
            f"line {line_number}: {line[:90]}" for line_number, line in provenance_leaks[:5]
        )
        errors.append(
            f"{len(provenance_leaks)} spoken passage(s) expose source provenance or claim status; {preview}"
        )

    duplicate_headings = find_duplicate_major_headings(text)
    if duplicate_headings:
        errors.append(
            "duplicate major heading(s) should be merged: " + ", ".join(duplicate_headings)
        )

    required = {
        "Battle Card or P0 layer": [r"battle card", r"作战卡", r"^#\s*P0", r"^##\s*P0"],
        "60-second introduction": [r"60\s*秒", r"60-second"],
        "90-second introduction": [r"90\s*秒", r"90-second"],
        "company STARS map": [r"STARS", r"公司.*阶段", r"company and role map"],
        "primary story": [r"首选(?:项目|｜|:|：)", r"主项目", r"primary story"],
        "backup story": [r"备用项目", r"备选", r"backup story"],
        "final claim card": [r"最后事实卡", r"final claim card", r"事实边界"],
        "last updated": [r"最后更新", r"last updated"],
    }
    for label, patterns in required.items():
        if not contains(text, patterns):
            errors.append(f"missing {label}")

    question_count = count_numbered_questions(text)
    if question_count < 10:
        errors.append(f"only {question_count} numbered high-probability questions; need at least 10")

    interviewer_count = count_interviewer_questions(text)
    if interviewer_count < 3:
        errors.append(f"only {interviewer_count} interviewer questions; need at least 3")

    first_impression = contains(text, [r"第一印象", r"快速扫描", r"招聘方.*判断", r"first impression"])
    if not first_impression:
        warnings.append("missing recruiter first-impression diagnostic")

    company_identity = contains(text, [r"招聘主体", r"品牌.*确认", r"分析边界", r"identity boundary"])
    if not company_identity:
        warnings.append("company identity boundary is not explicit")

    culture = contains(text, [r"文化", r"culture"])
    if not culture:
        errors.append("missing culture hypotheses or culture-fit language")

    p0_depth = all(contains(text, patterns) for patterns in [
        [r"证据锚点", r"evidence anchor"],
        [r"可能追问", r"likely follow-up", r"三层追问"],
        [r"停止句", r"安全边界", r"stop sentence", r"事实边界"],
    ])
    if not p0_depth:
        warnings.append("P0 answers may be missing evidence anchors, follow-ups, or stop boundaries")

    top = "\n".join(text.splitlines()[:120])
    if not contains(top, [r"60\s*秒", r"60-second"]):
        warnings.append("60-second introduction is not near the top Battle Card")
    if not contains(top, [r"主项目", r"首选(?:项目|｜|:|：)", r"primary story"]):
        warnings.append("primary story card is not near the top Battle Card")

    result = {
        "file": str(args.handbook),
        "mode": args.mode,
        "passed": not errors,
        "question_count": question_count,
        "interviewer_question_count": interviewer_count,
        "errors": errors,
        "warnings": warnings,
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("PASS" if not errors else "FAIL")
        for item in errors:
            print(f"ERROR: {item}")
        for item in warnings:
            print(f"WARNING: {item}")
        print(f"Questions: {question_count}; interviewer questions: {interviewer_count}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
