#!/usr/bin/env python3
"""Build deterministic GitHub release assets from the checked-out tree."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import zipfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = ROOT / "release" / "build"
EXPECTED_VERSION = "v1.1.0"
EXPECTED_DATE = "2026-09-26"
PROJECT_STEM = "minvol-contact-bound"
FIXED_ZIP_TIME = (2026, 9, 26, 0, 0, 0)

FORBIDDEN_PARTS = {
    ".git",
    ".venv",
    "__pycache__",
    "build",
    "ci-artifacts",
}
FORBIDDEN_NAMES = {".DS_Store"}


@dataclass(frozen=True)
class Asset:
    path: Path
    role: str


def run(*args: str) -> str:
    result = subprocess.run(
        list(args), cwd=ROOT, check=True, capture_output=True, text=True
    )
    return result.stdout.strip()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def read_scalar(path: Path) -> str:
    value = path.read_text(encoding="utf-8").strip()
    if not value:
        raise SystemExit(f"empty release metadata file: {path.relative_to(ROOT)}")
    return value


def require_release_metadata() -> tuple[str, str]:
    version = read_scalar(ROOT / "VERSION")
    release_date = read_scalar(ROOT / "RELEASE_DATE")
    if version != EXPECTED_VERSION:
        raise SystemExit(f"VERSION is {version!r}; expected {EXPECTED_VERSION!r}")
    if release_date != EXPECTED_DATE:
        raise SystemExit(
            f"RELEASE_DATE is {release_date!r}; expected {EXPECTED_DATE!r}"
        )
    date.fromisoformat(release_date)
    return version, release_date


def git_state(preview: bool) -> tuple[str, str | None]:
    commit = run("git", "rev-parse", "HEAD")
    status_text = run("git", "status", "--porcelain", "--untracked-files=normal")
    if status_text and not preview:
        raise SystemExit("release assets must be built from a clean checkout")

    tags = [line for line in run("git", "tag", "--points-at", "HEAD").splitlines() if line]
    tag = EXPECTED_VERSION if EXPECTED_VERSION in tags else None
    if not preview and tag != EXPECTED_VERSION:
        raise SystemExit(
            f"HEAD is not tagged {EXPECTED_VERSION}; use --preview only for pre-tag testing"
        )
    return commit, tag


def ensure_source(path: Path) -> Path:
    resolved = (ROOT / path).resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise SystemExit(f"source escapes repository: {path}") from exc
    if not resolved.is_file():
        raise SystemExit(f"missing release source: {path}")
    return resolved


def executable_mode(path: Path) -> int:
    mode = path.stat().st_mode
    return 0o755 if mode & stat.S_IXUSR else 0o644


def add_bytes(
    archive: zipfile.ZipFile,
    arcname: PurePosixPath,
    data: bytes,
    mode: int = 0o644,
) -> None:
    info = zipfile.ZipInfo(str(arcname), date_time=FIXED_ZIP_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = (mode & 0xFFFF) << 16
    archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def write_zip(
    output: Path,
    prefix: str,
    paths: list[Path],
    generated: dict[str, bytes] | None = None,
) -> None:
    seen: set[str] = set()
    with zipfile.ZipFile(output, "w", allowZip64=True) as archive:
        for relative in sorted(paths, key=lambda p: p.as_posix()):
            if any(part in FORBIDDEN_PARTS for part in relative.parts):
                raise SystemExit(f"forbidden release path: {relative}")
            if relative.name in FORBIDDEN_NAMES:
                raise SystemExit(f"forbidden release file: {relative}")
            source = ensure_source(relative)
            arcname = PurePosixPath(prefix) / PurePosixPath(relative.as_posix())
            name = str(arcname)
            if name in seen:
                raise SystemExit(f"duplicate archive member: {name}")
            seen.add(name)
            add_bytes(archive, arcname, source.read_bytes(), executable_mode(source))
        for relative_name, data in sorted((generated or {}).items()):
            arcname = PurePosixPath(prefix) / PurePosixPath(relative_name)
            name = str(arcname)
            if name in seen:
                raise SystemExit(f"duplicate generated archive member: {name}")
            seen.add(name)
            add_bytes(archive, arcname, data)


def markdown_sources() -> list[Path]:
    result = subprocess.run(
        ["sh", "tools/markdown_pdf/list_markdown_sources.sh"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [Path(line) for line in result.stdout.splitlines() if line.strip()]


def paper_source_paths() -> list[Path]:
    return [
        Path("LICENSE"),
        Path("VERSION"),
        Path("RELEASE_DATE"),
        Path("paper/README.md"),
        Path("paper/SHA256SUMS.txt"),
        Path("paper/build.sh"),
        Path("paper/certificate_constants.tex"),
        Path("paper/contact_geometric_bound.tex"),
        Path("paper/contact_geometric_bound.pdf"),
        Path("paper/lower_branch_table.tex"),
        Path("paper/reconcile_certificate.py"),
        Path("certificate/certificates/universal_contact_bound_certificate.json"),
        Path("tools/markdown_pdf/normalize_pdf_id.py"),
    ]


def certificate_paths() -> list[Path]:
    paths = [
        path.relative_to(ROOT)
        for path in (ROOT / "certificate").rglob("*")
        if path.is_file()
        and not any(part in FORBIDDEN_PARTS for part in path.relative_to(ROOT).parts)
        and path.name not in FORBIDDEN_NAMES
    ]
    paths.extend(
        [
            Path("LICENSE"),
            Path("VERSION"),
            Path("RELEASE_DATE"),
            Path("requirements.txt"),
        ]
    )
    return sorted(set(paths), key=lambda p: p.as_posix())


def documentation_paths() -> list[Path]:
    sources = markdown_sources()
    rendered = [Path("rendered/markdown") / src.with_suffix(".pdf") for src in sources]
    supporting = [
        Path("rendered/markdown/SHA256SUMS.txt"),
        Path("build_markdown_pdfs.sh"),
        Path("ci/verify_doc_pairs.py"),
        Path("tools/markdown_pdf/first_h1_title.lua"),
        Path("tools/markdown_pdf/list_markdown_sources.sh"),
        Path("tools/markdown_pdf/math_display_fixes.lua"),
        Path("tools/markdown_pdf/normalize_pdf_id.py"),
        Path("tools/markdown_pdf/preamble.tex"),
        Path("LICENSE"),
        Path("CITATION.cff"),
        Path("VERSION"),
        Path("RELEASE_DATE"),
    ]
    return sorted(set(sources + rendered + supporting), key=lambda p: p.as_posix())


def replay_paths() -> list[Path]:
    paths: list[Path] = []
    for directory in (ROOT / "certificate" / "transcripts", ROOT / "certificate" / "evidence"):
        paths.extend(path.relative_to(ROOT) for path in directory.rglob("*") if path.is_file())
    paths.extend(
        [
            Path("CLEAN_CLONE_CHECK.md"),
            Path("VERIFICATION_STATUS.md"),
            Path("certificate/INDEPENDENT_AUDIT.md"),
            Path("proof/APPENDIX_C_REPLAY_TRANSCRIPTS.md"),
            Path("rendered/markdown/CLEAN_CLONE_CHECK.pdf"),
            Path("rendered/markdown/VERIFICATION_STATUS.pdf"),
            Path("rendered/markdown/certificate/INDEPENDENT_AUDIT.pdf"),
            Path("rendered/markdown/proof/APPENDIX_C_REPLAY_TRANSCRIPTS.pdf"),
            Path("SHA256SUMS.txt"),
            Path("certificate/SHA256SUMS.txt"),
            Path("LICENSE"),
            Path("VERSION"),
            Path("RELEASE_DATE"),
        ]
    )
    return sorted(set(paths), key=lambda p: p.as_posix())


def copy_asset(source: Path, destination: Path) -> None:
    ensure_source(source.relative_to(ROOT))
    shutil.copyfile(source, destination)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="output directory (default: release/build)",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="allow an untagged or dirty tree for pre-release packaging tests",
    )
    args = parser.parse_args()

    version, release_date = require_release_metadata()
    commit, tag = git_state(args.preview)
    output = args.output if args.output.is_absolute() else ROOT / args.output
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    stem = f"{PROJECT_STEM}-{version}"
    assets: list[Asset] = []

    paper_pdf = output / f"{PROJECT_STEM}-paper-{version}.pdf"
    copy_asset(ROOT / "paper" / "contact_geometric_bound.pdf", paper_pdf)
    assets.append(Asset(paper_pdf, "paper PDF"))

    notes_md = output / "RELEASE_NOTES.md"
    notes_pdf = output / "RELEASE_NOTES.pdf"
    copy_asset(ROOT / "RELEASE_NOTES.md", notes_md)
    copy_asset(ROOT / "rendered" / "markdown" / "RELEASE_NOTES.pdf", notes_pdf)
    assets.extend([Asset(notes_md, "release notes Markdown"), Asset(notes_pdf, "release notes PDF")])

    paper_zip = output / f"{PROJECT_STEM}-paper-source-{version}.zip"
    write_zip(paper_zip, f"{stem}-paper-source", paper_source_paths())
    assets.append(Asset(paper_zip, "paper source archive"))

    certificate_zip = output / f"{PROJECT_STEM}-certificate-{version}.zip"
    certificate_readme = (
        "MinVol standalone certificate archive\n"
        f"Version: {version}\n"
        f"Release date: {release_date}\n\n"
        "Install the pinned Python dependency from requirements.txt, then run:\n"
        "  cd certificate\n"
        "  ./run_python_checks.sh\n"
        "With base R installed, use ./run_all.sh for the complete replay.\n"
    ).encode("utf-8")
    write_zip(
        certificate_zip,
        f"{stem}-certificate",
        certificate_paths(),
        {"ARCHIVE_README.txt": certificate_readme},
    )
    assets.append(Asset(certificate_zip, "standalone certificate archive"))

    docs_zip = output / f"{PROJECT_STEM}-docs-{version}.zip"
    write_zip(docs_zip, f"{stem}-docs", documentation_paths())
    assets.append(Asset(docs_zip, "documentation archive"))

    replay_zip = output / f"{PROJECT_STEM}-replay-transcripts-{version}.zip"
    write_zip(replay_zip, f"{stem}-replay-transcripts", replay_paths())
    assets.append(Asset(replay_zip, "replay and audit archive"))

    record_path = output / f"{PROJECT_STEM}-release-record-{version}.json"
    record = {
        "schema": "minvol.contact_bound.release_record.v1",
        "version": version,
        "release_date": release_date,
        "repository": "https://github.com/swihart/minvol-degree3-contact-bound",
        "release_url": f"https://github.com/swihart/minvol-degree3-contact-bound/releases/tag/{version}",
        "commit": commit,
        "tag": tag,
        "mode": "preview" if args.preview else "tagged-release",
        "theorem_certificate_sha256": sha256(
            ROOT / "certificate" / "certificates" / "universal_contact_bound_certificate.json"
        ),
        "paper_pdf_sha256": sha256(ROOT / "paper" / "contact_geometric_bound.pdf"),
        "assets": {
            asset.path.name: {"role": asset.role, "sha256": sha256(asset.path)}
            for asset in assets
        },
        "claim_boundary": {
            "peer_review": False,
            "external_mathematical_reproduction": False,
            "sharpness": False,
            "minimizer_identified": False,
            "meissner_extremality": False,
        },
    }
    record_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    assets.append(Asset(record_path, "machine-readable release record"))

    manifest_path = output / "SHA256SUMS.txt"
    manifest_lines = [f"{sha256(asset.path)}  {asset.path.name}\n" for asset in sorted(assets, key=lambda a: a.path.name)]
    manifest_path.write_text("".join(manifest_lines), encoding="ascii")

    print(f"Release version: {version}")
    print(f"Release date:    {release_date}")
    print(f"Source commit:   {commit}")
    print(f"Tag at HEAD:     {tag or '(preview: tag not required)'}")
    print(f"Assets written:  {len(assets)}")
    print(f"Output:          {output.relative_to(ROOT) if output.is_relative_to(ROOT) else output}")
    print("MINVOL RELEASE-ASSET BUILD: PASS")


if __name__ == "__main__":
    main()
