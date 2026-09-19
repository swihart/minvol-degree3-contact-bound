#!/usr/bin/env python3
"""Canonicalize volatile fields in an xdvipdfmx-generated PDF.

For reproducible repository documentation, the Markdown PDF build asks
xdvipdfmx to disable stream compression and PDF object streams.  This script
then canonicalizes three fields that may otherwise vary between equivalent
XeLaTeX runs:

* six-letter embedded-font subset prefixes;
* CreationDate and ModDate values; and
* the PDF trailer ID.

All replacements preserve byte lengths, so PDF cross-reference offsets remain
valid.  The final trailer ID is a SHA-256 digest of the already-canonicalized
PDF with both ID strings zeroed.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import os
import re
from pathlib import Path
from typing import Match

HEX_ID_PATTERN = re.compile(
    rb"/ID\s*\[\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*\]"
)

# ID strings produced by xdvipdfmx may instead be PDF literal strings.
LITERAL_ID_PATTERN = re.compile(
    rb"/ID\s*\[\s*\(((?:\\[0-7]{1,3}|\\\r?\n|\\.|[^\\()])*)\)"
    rb"\s*\(((?:\\[0-7]{1,3}|\\\r?\n|\\.|[^\\()])*)\)\s*\]",
    re.DOTALL,
)

DATE_PATTERN = re.compile(
    rb"/(CreationDate|ModDate)(\s*)\((D:\d{14}Z)\)"
)

# With compression and object streams disabled, xdvipdfmx font subset names
# occur in ordinary PDF dictionaries and CMap streams.  Collect prefixes only
# from font-name fields, then replace those exact prefixes everywhere so the
# dictionary, descriptor, CMap, and embedded font program remain consistent.
FONT_NAME_PATTERN = re.compile(
    rb"/(?:BaseFont|FontName|CMapName)\s*/"
    rb"([A-Z]{6})\+([A-Za-z0-9][A-Za-z0-9_.-]{2,})"
)

FONT_NAME_SUFFIXES = (b"-Identity-H", b"-UTF16")


def _font_root(name: bytes) -> bytes:
    for suffix in FONT_NAME_SUFFIXES:
        if name.endswith(suffix):
            return name[: -len(suffix)]
    return name


def _six_letters(key: bytes, salt: int = 0) -> bytes:
    digest = hashlib.sha256(
        b"minvol-pdf-font-subset\0" + key + b"\0" + str(salt).encode("ascii")
    ).digest()
    value = int.from_bytes(digest[:8], "big")
    letters = bytearray(6)
    for index in range(5, -1, -1):
        letters[index] = ord("A") + value % 26
        value //= 26
    return bytes(letters)


def _canonicalize_font_prefixes(data: bytes) -> bytes:
    prefix_to_roots: dict[bytes, set[bytes]] = {}
    for old_prefix, name in FONT_NAME_PATTERN.findall(data):
        prefix_to_roots.setdefault(old_prefix, set()).add(_font_root(name))

    if not prefix_to_roots:
        return data

    for old_prefix, roots in prefix_to_roots.items():
        if len(roots) != 1:
            rendered = b", ".join(sorted(roots)).decode("ascii", errors="replace")
            raise RuntimeError(
                f"font subset prefix {old_prefix.decode('ascii')} refers to "
                f"multiple font roots: {rendered}"
            )

    roots = sorted({next(iter(values)) for values in prefix_to_roots.values()})
    root_to_new: dict[bytes, bytes] = {}
    used: set[bytes] = set()
    for root in roots:
        salt = 0
        while True:
            candidate = _six_letters(root, salt)
            if candidate not in used:
                break
            salt += 1
        root_to_new[root] = candidate
        used.add(candidate)

    old_to_new = {
        old_prefix: root_to_new[next(iter(roots_for_prefix))]
        for old_prefix, roots_for_prefix in prefix_to_roots.items()
    }
    alternatives = b"|".join(re.escape(prefix) for prefix in sorted(old_to_new))
    occurrence_pattern = re.compile(rb"(?:" + alternatives + rb")\+")

    def replace_occurrence(match: Match[bytes]) -> bytes:
        old_prefix = match.group(0)[:-1]
        return old_to_new[old_prefix] + b"+"

    return occurrence_pattern.sub(replace_occurrence, data)


def _source_date() -> bytes:
    raw_epoch = os.environ.get("SOURCE_DATE_EPOCH", "1788652800")
    try:
        epoch = int(raw_epoch)
    except ValueError as exc:
        raise RuntimeError(f"invalid SOURCE_DATE_EPOCH: {raw_epoch!r}") from exc
    instant = dt.datetime.fromtimestamp(epoch, tz=dt.timezone.utc)
    return instant.strftime("D:%Y%m%d%H%M%SZ").encode("ascii")


def _canonicalize_dates(data: bytes) -> bytes:
    target = _source_date()

    def replace_date(match: Match[bytes]) -> bytes:
        return b"/" + match.group(1) + match.group(2) + b"(" + target + b")"

    return DATE_PATTERN.sub(replace_date, data)


def _canonicalize_trailer_id(data: bytes, path: Path) -> bytes:
    matches = list(HEX_ID_PATTERN.finditer(data)) + list(
        LITERAL_ID_PATTERN.finditer(data)
    )
    if len(matches) != 1:
        raise RuntimeError(
            f"expected exactly one supported PDF trailer ID in {path}, "
            f"found {len(matches)}"
        )

    match = matches[0]
    first = match.group(1)
    second = match.group(2)
    if len(first) != len(second):
        raise RuntimeError(f"unequal PDF trailer ID representation lengths in {path}")

    zeroed = bytearray(data)
    zeroed[match.start(1) : match.end(1)] = b"0" * len(first)
    zeroed[match.start(2) : match.end(2)] = b"0" * len(second)
    digest = hashlib.sha256(zeroed).hexdigest().encode("ascii")
    repeats = (len(first) + len(digest) - 1) // len(digest)
    replacement = (digest * repeats)[: len(first)]

    normalized = bytearray(data)
    normalized[match.start(1) : match.end(1)] = replacement
    normalized[match.start(2) : match.end(2)] = replacement
    return bytes(normalized)


def normalize_pdf(path: Path) -> None:
    data = path.read_bytes()
    data = _canonicalize_font_prefixes(data)
    data = _canonicalize_dates(data)
    data = _canonicalize_trailer_id(data, path)
    path.write_bytes(data)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    args = parser.parse_args()
    normalize_pdf(args.pdf)


if __name__ == "__main__":
    main()
