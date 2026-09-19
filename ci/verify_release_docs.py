#!/usr/bin/env python3
"""Verify the public release-document set and its claim boundaries."""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
CERTIFICATE = ROOT / "certificate" / "certificates" / "universal_contact_bound_certificate.json"

REQUIRED_MARKDOWN = [
    "README.md",
    "AI_ASSISTANCE.md",
    "CLEAN_CLONE_CHECK.md",
    "RELEASE_CHECKLIST.md",
    "RELEASE_NOTES.md",
    "REPRODUCIBILITY.md",
    "VERIFICATION_STATUS.md",
    "certificate/CERTIFICATE_SPECIFICATION.md",
    "certificate/CLAIMS_AND_LIMITATIONS.md",
    "certificate/INDEPENDENT_AUDIT.md",
    "certificate/README.md",
    "certificate/STATUS.md",
    "certificate/TRUST_BOUNDARY.md",
    "paper/README.md",
    "proof/APPENDIX_A_EXACT_CONSTANTS.md",
    "proof/APPENDIX_B_CERTIFICATE_ARCHITECTURE.md",
    "proof/APPENDIX_C_REPLAY_TRANSCRIPTS.md",
    "proof/CLAIM_DEPENDENCIES.md",
    "proof/MATHEMATICAL_OVERVIEW.md",
    "proof/PROOF_AUDIT.md",
    "proof/PROOF_LEDGER.md",
    "proof/SOURCE_LEDGER.md",
]

THEOREM_DOCS = [
    "README.md",
    "RELEASE_NOTES.md",
    "REPRODUCIBILITY.md",
    "VERIFICATION_STATUS.md",
    "certificate/CLAIMS_AND_LIMITATIONS.md",
    "certificate/STATUS.md",
    "paper/README.md",
    "proof/APPENDIX_A_EXACT_CONSTANTS.md",
    "proof/MATHEMATICAL_OVERVIEW.md",
    "proof/PROOF_AUDIT.md",
]

LIMITATION_DOCS = [
    "README.md",
    "RELEASE_NOTES.md",
    "VERIFICATION_STATUS.md",
    "certificate/CLAIMS_AND_LIMITATIONS.md",
    "certificate/STATUS.md",
    "paper/README.md",
]

PROHIBITED_TEXT = [
    "minvol-spectral-refinements",
    "work/jung-endpoint",
    "0.4157",
    "d5916d673523015ddec4f735dfd254d5a927fd3c",
    "57050955c68e6b8bfd35b70e19631c70b9ab5364",
    "f3e54e68861677d6fd4b31664a1d85fe6350ee14",
    "PRIVATE WORKING DRAFT",
    "Author list to be finalized",
    "/mnt/data/",
    "/Users/",
    "~/github/",
]

LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def read_text(relative: str) -> str:
    path = ROOT / relative
    if not path.is_file():
        raise SystemExit(f"missing required release document: {relative}")
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise SystemExit(f"release document is not UTF-8: {relative}: {exc}") from exc
    if not text.startswith("# "):
        raise SystemExit(f"release document lacks a level-one title: {relative}")
    return text


def theorem_strings() -> tuple[str, str]:
    data = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    theorem = data.get("theorem")
    if not isinstance(theorem, dict):
        raise SystemExit("unexpected theorem certificate schema")
    coefficient = theorem.get("coefficient_of_pi")
    if not isinstance(coefficient, str) or "/" not in coefficient:
        raise SystemExit("could not locate theorem coefficient in certificate JSON")
    numerator_text, denominator_text = coefficient.split("/", 1)
    numerator = int(numerator_text)
    denominator = int(denominator_text)
    rational = f"\\frac{{{numerator}\\pi}}{{{denominator}}}"
    decimal = theorem.get("coefficient_decimal_lower")
    if not isinstance(decimal, str) or not decimal:
        raise SystemExit("could not locate theorem decimal lower bound in certificate JSON")
    return rational, decimal


def check_relative_links(relative: str, text: str) -> int:
    source = ROOT / relative
    checked = 0
    for match in LINK_RE.finditer(text):
        target = match.group(1).strip()
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        target = target.split("#", 1)[0].split("?", 1)[0]
        if not target:
            continue
        decoded = unquote(target)
        destination = (source.parent / decoded).resolve()
        try:
            destination.relative_to(ROOT.resolve())
        except ValueError as exc:
            raise SystemExit(f"relative link escapes repository: {relative}: {target}") from exc
        if not destination.exists():
            raise SystemExit(f"broken relative link: {relative}: {target}")
        checked += 1
    return checked


def main() -> None:
    texts = {relative: read_text(relative) for relative in REQUIRED_MARKDOWN}

    rational_fragment, exact_decimal = theorem_strings()
    decimal_prefix = exact_decimal[:17] if exact_decimal else "0.411877563780302"

    for relative in THEOREM_DOCS:
        text = texts[relative]
        if rational_fragment not in text.replace(" ", ""):
            raise SystemExit(f"theorem fraction missing or stale in {relative}")
        if decimal_prefix not in text:
            raise SystemExit(f"theorem decimal missing or stale in {relative}")

    for relative in LIMITATION_DOCS:
        lowered = texts[relative].lower()
        missing: list[str] = []
        if "meissner" not in lowered:
            missing.append("meissner")
        if "peer review" not in lowered and "peer-reviewed" not in lowered:
            missing.append("peer-review language")
        if "minimiz" not in lowered:
            missing.append("minimizer language")
        if missing:
            raise SystemExit(
                f"claim-limit language incomplete in {relative}; missing {missing}"
            )

    scan_paths = list(REQUIRED_MARKDOWN) + ["paper/contact_geometric_bound.tex"]
    for relative in scan_paths:
        path = ROOT / relative
        text = path.read_text(encoding="utf-8")
        for prohibited in PROHIBITED_TEXT:
            if prohibited in text:
                raise SystemExit(f"private or provisional text leaked into {relative}: {prohibited}")

    source_ledger = texts["proof/SOURCE_LEDGER.md"]
    if "September 19, 2026" not in source_ledger:
        raise SystemExit("source ledger lacks the dated literature-check stamp")
    for token in (
        "10.1016/j.jmaa.2026.131038",
        "Tencent-Hunyuan/Hyra-results",
        "10.1007/s00454-024-00688-0",
        "not a systematic novelty review",
    ):
        if token not in source_ledger:
            raise SystemExit(f"source ledger missing required provenance token: {token}")

    readme = texts["README.md"]
    for relative in REQUIRED_MARKDOWN:
        if relative in {"README.md", "paper/README.md", "certificate/README.md", "certificate/STATUS.md"}:
            continue
        if relative not in readme:
            raise SystemExit(f"top-level README does not link the release document: {relative}")

    version = (ROOT / "VERSION").read_text(encoding="ascii").strip()
    release_date = (ROOT / "RELEASE_DATE").read_text(encoding="ascii").strip()
    if version == "0.1.0-dev" and release_date != "UNRELEASED":
        raise SystemExit("development version must retain RELEASE_DATE=UNRELEASED")
    if release_date == "UNRELEASED" and "DO NOT RELEASE YET" not in texts["RELEASE_CHECKLIST.md"]:
        raise SystemExit("unreleased checklist lacks an explicit no-release decision")

    link_count = sum(
        check_relative_links(relative, text) for relative, text in texts.items()
    )

    print(f"Required Markdown documents: {len(REQUIRED_MARKDOWN)}")
    print(f"Theorem-bearing documents:   {len(THEOREM_DOCS)}")
    print(f"Relative links checked:      {link_count}")
    print("MINVOL RELEASE-DOCUMENT CHECK: PASS")


if __name__ == "__main__":
    main()
