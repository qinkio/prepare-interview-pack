#!/usr/bin/env python3
"""Build a deterministic WorkBuddy upload package for prepare-interview-pack."""

from __future__ import annotations

import argparse
import hashlib
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "prepare-interview-pack"
DEFAULT_OUTPUT = REPO_ROOT / "dist" / "prepare-interview-pack-workbuddy.zip"
INCLUDED_PATHS = ("SKILL.md", "references", "scripts")
EXCLUDED_PARTS = {"__pycache__", ".DS_Store"}


def is_package_file(path: Path) -> bool:
    relative = path.relative_to(SKILL_ROOT)
    return (
        path.is_file()
        and not any(part in EXCLUDED_PARTS for part in relative.parts)
        and path.suffix not in {".pyc", ".pyo"}
    )


def iter_files() -> list[Path]:
    files: list[Path] = []
    for item in INCLUDED_PATHS:
        path = SKILL_ROOT / item
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            files.extend(candidate for candidate in path.rglob("*") if is_package_file(candidate))
        else:
            raise FileNotFoundError(f"Required package path is missing: {path}")
    return sorted(files, key=lambda path: path.relative_to(SKILL_ROOT).as_posix())


def write_member(archive: zipfile.ZipFile, source: Path) -> None:
    relative = source.relative_to(SKILL_ROOT).as_posix()
    info = zipfile.ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = (0o755 if source.suffix == ".py" else 0o644) << 16
    archive.writestr(info, source.read_bytes())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    if not (SKILL_ROOT / "SKILL.md").is_file():
        raise FileNotFoundError(f"SKILL.md not found under {SKILL_ROOT}")

    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w") as archive:
        for source in iter_files():
            write_member(archive, source)

    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    print(f"Built: {output}")
    print(f"SHA256: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
