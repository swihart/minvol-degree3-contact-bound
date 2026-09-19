#!/usr/bin/env python3
"""Verify one committed or locally built PDF for every repository Markdown source."""
from __future__ import annotations

import argparse
import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE_LISTER = ROOT / "tools" / "markdown_pdf" / "list_markdown_sources.sh"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def markdown_sources() -> list[Path]:
    result = subprocess.run(
        ["sh", str(SOURCE_LISTER)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [Path(line) for line in result.stdout.splitlines() if line.strip()]


def parse_manifest(path: Path) -> dict[str, str]:
    entries: dict[str, str] = {}
    for line in path.read_text(encoding="ascii").splitlines():
        if not line.strip():
            continue
        digest, rendered = line.split(None, 1)
        entries[rendered.strip()] = digest
    return entries


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pdf-root",
        type=Path,
        default=Path("rendered/markdown"),
        help="PDF tree relative to the repository root",
    )
    args = parser.parse_args()

    pdf_root = (ROOT / args.pdf_root).resolve()
    manifest = pdf_root / "SHA256SUMS.txt"
    if not manifest.is_file():
        raise SystemExit(f"missing PDF checksum manifest: {manifest}")

    sources = markdown_sources()
    expected = {
        (pdf_root / source.with_suffix(".pdf")).resolve(): source for source in sources
    }
    actual = {
        path.resolve()
        for path in pdf_root.rglob("*.pdf")
        if path.is_file()
    }

    missing = sorted(expected.keys() - actual)
    extra = sorted(actual - expected.keys())
    if missing or extra:
        details: list[str] = []
        if missing:
            details.append(
                "missing PDFs: "
                + ", ".join(str(path.relative_to(ROOT)) for path in missing)
            )
        if extra:
            details.append(
                "unexpected PDFs: "
                + ", ".join(str(path.relative_to(ROOT)) for path in extra)
            )
        raise SystemExit("; ".join(details))

    entries = parse_manifest(manifest)
    expected_manifest_paths = {
        str(path.relative_to(ROOT)) for path in sorted(actual)
    }
    if set(entries) != expected_manifest_paths:
        missing_entries = expected_manifest_paths - set(entries)
        extra_entries = set(entries) - expected_manifest_paths
        raise SystemExit(
            "PDF checksum manifest path mismatch; "
            f"missing={sorted(missing_entries)}, extra={sorted(extra_entries)}"
        )

    for path in sorted(actual):
        if path.stat().st_size == 0 or path.read_bytes()[:5] != b"%PDF-":
            raise SystemExit(f"invalid or empty PDF: {path.relative_to(ROOT)}")
        relative = str(path.relative_to(ROOT))
        if sha256(path) != entries[relative]:
            raise SystemExit(f"PDF checksum mismatch: {relative}")

    print(f"Markdown sources: {len(sources)}")
    print(f"Paired PDFs:      {len(actual)}")
    print(f"PDF root:         {pdf_root.relative_to(ROOT)}")
    print("MINVOL MARKDOWN/PDF PAIR CHECK: PASS")


if __name__ == "__main__":
    main()
