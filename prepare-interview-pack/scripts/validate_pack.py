#!/usr/bin/env python3
"""Deterministic structural checks for prepare-interview-pack Markdown output."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
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


def load_resume_projects(path: Path) -> list[tuple[str, list[str]]]:
    """Load resume project names from JSON or a one-project-per-line text file."""
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return []
    if path.suffix.lower() == ".json":
        data = json.loads(raw)
        if isinstance(data, dict):
            data = data.get("projects", [])
        if not isinstance(data, list):
            raise ValueError("resume project manifest JSON must be a list or contain a projects list")
        projects: list[tuple[str, list[str]]] = []
        for item in data:
            if isinstance(item, str):
                projects.append((item.strip(), []))
            elif isinstance(item, dict) and isinstance(item.get("name"), str):
                aliases = item.get("aliases", [])
                if not isinstance(aliases, list) or not all(isinstance(alias, str) for alias in aliases):
                    raise ValueError("each project aliases field must be a list of strings")
                projects.append((item["name"].strip(), [alias.strip() for alias in aliases]))
            else:
                raise ValueError("each resume project must be a string or an object with name")
        return [(name, aliases) for name, aliases in projects if name]
    return [(line.strip(), []) for line in raw.splitlines() if line.strip() and not line.lstrip().startswith("#")]


def validate_resume_project_coverage(
    text: str, projects: list[tuple[str, list[str]]]
) -> tuple[list[str], int]:
    """Require every resume project to have an explicit disposition in the coverage ledger."""
    target = section(
        text,
        [r"简历项目.*(?:覆盖|清单|分层)", r"resume.*project.*coverage", r"project coverage ledger"],
    )
    if not target:
        return ["missing resume project coverage ledger"], 0

    disposition = re.compile(r"\bP[012]\b|\bExcluded\b|排除", re.I)
    lines = target.splitlines()
    errors: list[str] = []
    covered = 0
    for name, aliases in projects:
        candidates = [name, *aliases]
        matching = [line for line in lines if any(candidate and candidate.casefold() in line.casefold() for candidate in candidates)]
        if not matching:
            errors.append(f"resume project missing from coverage ledger: {name}")
        elif not any(disposition.search(line) for line in matching):
            errors.append(f"resume project lacks P0/P1/P2/Excluded disposition: {name}")
        else:
            covered += 1
    return errors, covered


def validate_company_research(data: object) -> list[str]:
    """Check substantive coverage and pointers, not factual truth or tool execution."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["company research must be a JSON object"]
    def nonempty(value: object) -> bool:
        return isinstance(value, str) and bool(value.strip())
    def valid_date(value: object) -> bool:
        try:
            return isinstance(value, str) and date.fromisoformat(value).isoformat() == value
        except ValueError:
            return False
    if not valid_date(data.get("checked_at")):
        errors.append("company research checked_at must be an ISO date")
    mode = data.get("mode")
    if mode not in ("searched", "provided-only", "unavailable"):
        errors.append("invalid company research mode")
    elif mode != "searched" and not nonempty(data.get("exception_reason")):
        errors.append("company research exception requires a concrete reason")
    def records(key: str) -> dict:
        items = data.get(key)
        if not isinstance(items, list):
            errors.append(f"company research {key} must be a list")
            return {}
        result = {}
        for item in items:
            if not isinstance(item, dict) or not nonempty(item.get("id")):
                errors.append(f"invalid company research {key} record")
                continue
            if item["id"] in result:
                errors.append(f"duplicate company research {key} id: {item['id']}")
            result[item["id"]] = item
        return result
    sources, searches = records("sources"), records("searches")
    def refs(item: dict, key: str, known: dict, label: str) -> list:
        values = item.get(key)
        if not isinstance(values, list) or not all(isinstance(v, str) for v in values):
            errors.append(f"{label} {key} must be a list of IDs")
            return []
        for value in values:
            if value not in known:
                errors.append(f"{label} references unknown {key}: {value}")
        return values
    for sid, item in sources.items():
        if not nonempty(item.get("pointer")) or not nonempty(item.get("kind")) or not valid_date(item.get("accessed_at")):
            errors.append(f"company source {sid} requires pointer, kind and ISO accessed_at")
        for field in ("published_at", "updated_at"):
            if item.get(field) is not None and not valid_date(item[field]):
                errors.append(f"company source {sid} {field} must be ISO date or null")
        if any(item.get(field) is not None for field in ("published_at", "updated_at")) and not nonempty(item.get("date_evidence")):
            errors.append(f"company source {sid} known date requires observed date label and location")
    if mode == "searched" and not searches:
        errors.append("searched company research contains no search attempts")
    for qid, item in searches.items():
        if not nonempty(item.get("query")) or item.get("outcome") not in ("read", "no-results", "blocked"):
            errors.append(f"invalid company search {qid}")
        linked = refs(item, "source_ids", sources, f"search {qid}")
        if item.get("outcome") == "read" and not linked:
            errors.append(f"read search {qid} has no inspected source")
    if mode == "searched" and searches and all(item.get("outcome") == "blocked" for item in searches.values()):
        errors.append("all company searches blocked; use unavailable mode and disclose the access failure")
    topics = data.get("topics")
    if not isinstance(topics, dict):
        return errors + ["company research topics must be an object"]
    for name in ("identity", "scale_and_model", "recent_developments", "conflicts", "interview_implications"):
        item = topics.get(name)
        if not isinstance(item, dict):
            errors.append(f"missing company research topic: {name}")
            continue
        if not nonempty(item.get("finding")) or item.get("status") not in ("supported", "partial", "not-found", "blocked"):
            errors.append(f"company topic {name} requires finding and valid status")
        source_ids = refs(item, "source_ids", sources, f"topic {name}")
        search_ids = refs(item, "search_ids", searches, f"topic {name}")
        evidence = item.get("evidence")
        if not isinstance(evidence, list):
            errors.append(f"company topic {name} evidence must be a list")
            evidence = []
        for entry in evidence:
            if not isinstance(entry, dict) or not nonempty(entry.get("locator")) or not nonempty(entry.get("excerpt")):
                errors.append(f"company topic {name} evidence requires precise locator and observed excerpt")
            elif entry.get("source_id") not in source_ids:
                errors.append(f"company topic {name} evidence must reference a listed topic source")
        if item.get("status") in ("supported", "partial") and not evidence:
            errors.append(f"company topic {name} claims support without precise evidence")
        if item.get("status") == "not-found" and search_ids and all(searches.get(q, {}).get("outcome") == "blocked" for q in search_ids):
            errors.append(f"company topic {name} is access-blocked, not a searched no-result finding")
        if item.get("status") in ("supported", "partial") and not source_ids:
            errors.append(f"company topic {name} claims support without a source")
        if mode == "searched" and name != "interview_implications" and not search_ids:
            errors.append(f"company topic {name} has no relevant search attempt")
    return errors


def company_research_status(data: object, invalid: bool = False) -> str:
    """Describe recorded access/coverage, never imply independent fact verification."""
    if invalid or not isinstance(data, dict):
        return "invalid"
    mode = data.get("mode")
    if mode in ("provided-only", "unavailable"):
        return mode
    if mode != "searched":
        return "invalid"
    topics = data.get("topics", {})
    if any(item.get("status") != "supported" for item in topics.values() if isinstance(item, dict)) or any(item.get("outcome") == "blocked" for item in data.get("searches", []) if isinstance(item, dict)):
        return "searched-with-gaps"
    return "searched"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("handbook", type=Path)
    parser.add_argument("--mode", choices=["sprint", "standard", "deep"], default="standard")
    parser.add_argument(
        "--resume-projects",
        type=Path,
        help="JSON manifest or one-project-per-line text file for resume project coverage checks",
    )
    parser.add_argument("--company-research", type=Path, help="Required company research coverage ledger JSON")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not args.handbook.is_file():
        print(f"ERROR: file not found: {args.handbook}", file=sys.stderr)
        return 2

    text = args.handbook.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []
    research_status = "invalid"
    if not args.company_research:
        errors.append("missing company research ledger; pass --company-research in every mode")
    else:
        try:
            research_data = json.loads(args.company_research.read_text(encoding="utf-8"))
            research_errors = validate_company_research(research_data)
            errors.extend(research_errors)
            research_status = company_research_status(research_data, bool(research_errors))
            if research_status != "searched" and research_status != "invalid":
                warnings.append(f"company research status: {research_status}; disclose gaps or exception separately from structural validity")
        except (OSError, ValueError) as exc:
            errors.append(f"invalid company research ledger: {exc}")
    resume_project_count = 0
    resume_project_covered = 0

    if args.resume_projects:
        if not args.resume_projects.is_file():
            errors.append(f"resume project manifest not found: {args.resume_projects}")
        else:
            try:
                resume_projects = load_resume_projects(args.resume_projects)
                resume_project_count = len(resume_projects)
                coverage_errors, resume_project_covered = validate_resume_project_coverage(
                    text, resume_projects
                )
                errors.extend(coverage_errors)
                if not resume_projects:
                    errors.append("resume project manifest contains no projects")
            except (ValueError, json.JSONDecodeError) as exc:
                errors.append(f"invalid resume project manifest: {exc}")

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
        "structural_passed": not errors,
        "research_status": research_status,
        "factual_verification": "not-assessed-by-script",
        "question_count": question_count,
        "interviewer_question_count": interviewer_count,
        "resume_project_count": resume_project_count,
        "resume_project_covered": resume_project_covered,
        "errors": errors,
        "warnings": warnings,
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("STRUCTURE PASS" if not errors else "STRUCTURE FAIL")
        print(f"Company research: {research_status}; factual verification not assessed by script")
        for item in errors:
            print(f"ERROR: {item}")
        for item in warnings:
            print(f"WARNING: {item}")
        print(f"Questions: {question_count}; interviewer questions: {interviewer_count}")
        if args.resume_projects:
            print(f"Resume projects: {resume_project_covered}/{resume_project_count} covered")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
