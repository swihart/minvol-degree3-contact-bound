#!/usr/bin/env python3
"""Regenerate or verify the repository and certificate SHA-256 manifests."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CERTIFICATE = ROOT / "certificate"
PAPER = ROOT / "paper"
IGNORED_DIRS = {".git", ".venv", "__pycache__", "build", "ci-artifacts"}
IGNORED_NAMES = {".DS_Store"}
IGNORED_SUFFIXES = {".pyc", ".tmp"}


def included_files(base: Path, manifest: Path) -> list[Path]:
    files: list[Path] = []
    for path in base.rglob("*"):
        if not path.is_file() or path == manifest:
            continue
        relative = path.relative_to(base)
        if any(part in IGNORED_DIRS for part in relative.parts):
            continue
        if path.name in IGNORED_NAMES or path.suffix in IGNORED_SUFFIXES:
            continue
        files.append(path)
    return sorted(files, key=lambda path: path.relative_to(base).as_posix())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def manifest_bytes(base: Path, manifest: Path) -> bytes:
    lines = [
        f"{sha256(path)}  ./{path.relative_to(base).as_posix()}\n"
        for path in included_files(base, manifest)
    ]
    return "".join(lines).encode("ascii")


def process(base: Path, manifest: Path, check: bool) -> None:
    expected = manifest_bytes(base, manifest)
    if check:
        if not manifest.exists() or manifest.read_bytes() != expected:
            raise SystemExit(f"checksum manifest is stale: {manifest}")
        print(f"CHECKSUM MANIFEST: OK ({manifest.relative_to(ROOT) if manifest != ROOT / 'SHA256SUMS.txt' else manifest.name})")
    else:
        manifest.write_bytes(expected)
        print(f"CHECKSUM MANIFEST: WROTE {manifest}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify manifests without modifying them")
    args = parser.parse_args()
    process(CERTIFICATE, CERTIFICATE / "SHA256SUMS.txt", args.check)
    process(PAPER, PAPER / "SHA256SUMS.txt", args.check)
    process(ROOT, ROOT / "SHA256SUMS.txt", args.check)


if __name__ == "__main__":
    main()
