#!/usr/bin/env python3
"""Verify MinVol GitHub release assets and their deterministic archives."""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path, PurePosixPath

EXPECTED_VERSION = "v1.1.0"
EXPECTED_DATE = "2026-09-26"
PROJECT_STEM = "minvol-contact-bound"
FIXED_ZIP_TIME = (2026, 9, 26, 0, 0, 0)
FORBIDDEN_PARTS = {".git", ".venv", "__pycache__", "build", "ci-artifacts"}
FORBIDDEN_NAMES = {".DS_Store"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_manifest(path: Path) -> dict[str, str]:
    entries: dict[str, str] = {}
    for line in path.read_text(encoding="ascii").splitlines():
        if not line.strip():
            continue
        digest, filename = line.split(None, 1)
        filename = filename.strip()
        if filename in entries:
            raise SystemExit(f"duplicate manifest filename: {filename}")
        entries[filename] = digest
    return entries


def check_zip(path: Path) -> int:
    with zipfile.ZipFile(path) as archive:
        bad = archive.testzip()
        if bad is not None:
            raise SystemExit(f"corrupt zip member in {path.name}: {bad}")
        names = archive.namelist()
        if not names:
            raise SystemExit(f"empty zip archive: {path.name}")
        if len(names) != len(set(names)):
            raise SystemExit(f"duplicate zip member name: {path.name}")
        for info in archive.infolist():
            if info.date_time != FIXED_ZIP_TIME:
                raise SystemExit(
                    f"non-deterministic zip timestamp in {path.name}: {info.filename}"
                )
        roots = {PurePosixPath(name).parts[0] for name in names if name}
        if len(roots) != 1:
            raise SystemExit(f"archive must have one top-level directory: {path.name}")
        for name in names:
            member = PurePosixPath(name)
            if member.is_absolute() or ".." in member.parts:
                raise SystemExit(f"unsafe archive path in {path.name}: {name}")
            if any(part in FORBIDDEN_PARTS for part in member.parts):
                raise SystemExit(f"forbidden archive path in {path.name}: {name}")
            if member.name in FORBIDDEN_NAMES:
                raise SystemExit(f"forbidden archive file in {path.name}: {name}")
        return len(names)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", nargs="?", default="release/build", type=Path)
    args = parser.parse_args()
    directory = args.directory.resolve()
    if not directory.is_dir():
        raise SystemExit(f"release-asset directory does not exist: {directory}")

    expected = {
        f"{PROJECT_STEM}-paper-{EXPECTED_VERSION}.pdf",
        f"{PROJECT_STEM}-paper-source-{EXPECTED_VERSION}.zip",
        f"{PROJECT_STEM}-certificate-{EXPECTED_VERSION}.zip",
        f"{PROJECT_STEM}-docs-{EXPECTED_VERSION}.zip",
        f"{PROJECT_STEM}-replay-transcripts-{EXPECTED_VERSION}.zip",
        f"{PROJECT_STEM}-release-record-{EXPECTED_VERSION}.json",
        "RELEASE_NOTES.md",
        "RELEASE_NOTES.pdf",
    }
    manifest_path = directory / "SHA256SUMS.txt"
    if not manifest_path.is_file():
        raise SystemExit("missing release-asset SHA256SUMS.txt")
    entries = parse_manifest(manifest_path)
    if set(entries) != expected:
        raise SystemExit(
            f"release manifest path mismatch; missing={sorted(expected-set(entries))}, "
            f"extra={sorted(set(entries)-expected)}"
        )

    for filename, digest in entries.items():
        path = directory / filename
        if not path.is_file() or path.stat().st_size == 0:
            raise SystemExit(f"missing or empty release asset: {filename}")
        if sha256(path) != digest:
            raise SystemExit(f"release-asset hash mismatch: {filename}")

    paper = directory / f"{PROJECT_STEM}-paper-{EXPECTED_VERSION}.pdf"
    notes_pdf = directory / "RELEASE_NOTES.pdf"
    for path in (paper, notes_pdf):
        if path.read_bytes()[:5] != b"%PDF-":
            raise SystemExit(f"invalid PDF signature: {path.name}")

    zip_members = 0
    for path in sorted(directory.glob("*.zip")):
        zip_members += check_zip(path)

    record_path = directory / f"{PROJECT_STEM}-release-record-{EXPECTED_VERSION}.json"
    record = json.loads(record_path.read_text(encoding="utf-8"))
    if record.get("schema") != "minvol.contact_bound.release_record.v1":
        raise SystemExit("unexpected release-record schema")
    if record.get("version") != EXPECTED_VERSION or record.get("release_date") != EXPECTED_DATE:
        raise SystemExit("release-record version/date mismatch")
    if record.get("repository") != "https://github.com/swihart/minvol-degree3-contact-bound":
        raise SystemExit("release-record repository mismatch")
    if record.get("release_url") != (
        "https://github.com/swihart/minvol-degree3-contact-bound/releases/tag/" + EXPECTED_VERSION
    ):
        raise SystemExit("release-record URL mismatch")
    record_assets = record.get("assets")
    if not isinstance(record_assets, dict):
        raise SystemExit("release-record assets field is missing")
    record_filename = f"{PROJECT_STEM}-release-record-{EXPECTED_VERSION}.json"
    expected_record_assets = expected - {record_filename}
    if set(record_assets) != expected_record_assets:
        raise SystemExit(
            "release-record asset set mismatch; "
            f"missing={sorted(expected_record_assets-set(record_assets))}, "
            f"extra={sorted(set(record_assets)-expected_record_assets)}"
        )
    for filename, metadata in record_assets.items():
        if filename not in entries:
            raise SystemExit(f"release-record references an unmanifested asset: {filename}")
        if not isinstance(metadata, dict) or metadata.get("sha256") != entries[filename]:
            raise SystemExit(f"release-record digest mismatch: {filename}")
    commit = record.get("commit")
    if not isinstance(commit, str) or len(commit) != 40 or any(c not in "0123456789abcdef" for c in commit):
        raise SystemExit("release-record commit is not a full lowercase SHA-1")
    tag = record.get("tag")
    mode = record.get("mode")
    if tag is None:
        if mode != "preview":
            raise SystemExit("untagged release record must use preview mode")
    elif tag == EXPECTED_VERSION:
        if mode != "tagged-release":
            raise SystemExit("tagged release record must use tagged-release mode")
    else:
        raise SystemExit(f"unexpected release-record tag: {tag!r}")

    boundary = record.get("claim_boundary")
    if not isinstance(boundary, dict) or any(boundary.get(key) is not False for key in (
        "peer_review", "external_mathematical_reproduction", "sharpness",
        "minimizer_identified", "meissner_extremality"
    )):
        raise SystemExit("release-record claim boundary is overstated")

    print(f"Release assets: {len(entries)}")
    print(f"ZIP members:    {zip_members}")
    print(f"Asset directory: {directory}")
    print("MINVOL RELEASE-ASSET VERIFICATION: PASS")


if __name__ == "__main__":
    main()
