"""Print a candidate source file's header row and aggregate column statistics as JSON.

ADR-0007 §5 evidence limit: before the split, an assessment may use a downloaded file's header
row and scripted aggregate statistics, and no person reads records. So the report holds counts
and shapes only, never a cell value. Only the header row is printed from the file.
"""

import argparse
import csv
import hashlib
import io
import json
import re
import statistics
import sys
from pathlib import Path

BOM = b"\xef\xbb\xbf"
SIX_DIGITS = re.compile(r"(?<!\d)\d{6}(?!\d)")
TEN_DIGITS = re.compile(r"(?<!\d)\d{10}(?!\d)")
EMAIL_LIKE = re.compile(r"\S+@\S+\.\S+")
NON_CSV_SIGNATURES = {
    b"PK\x03\x04": "zip_or_xlsx",
    b"\xd0\xcf\x11\xe0": "ole2_or_xls",
    b"%PDF": "pdf",
}
HTML_START = re.compile(rb"\s*<(?:!doctype\s+html|html)\b", re.IGNORECASE)


class InspectError(Exception):
    """The file cannot be inspected at all."""


def _spread(values: list[int]) -> dict[str, float] | None:
    if not values:
        return None
    return {"min": min(values), "median": statistics.median(values), "max": max(values)}


def _column(values: list[str], missing_tokens: list[str]) -> dict:
    missing = {token: values.count(token) for token in missing_tokens}
    present = [v for v in values if v.strip() and v not in missing_tokens]
    return {
        "empty": sum(not v.strip() for v in values),
        "missing_tokens": missing,
        "non_empty": len(present),
        "chars": _spread([len(v) for v in present]),
        "tokens": _spread([len(v.split()) for v in present]),
        "six_digit_run": sum(bool(SIX_DIGITS.search(v)) for v in present),
        "ten_digit_run": sum(bool(TEN_DIGITS.search(v)) for v in present),
        "email_like": sum(bool(EMAIL_LIKE.search(v)) for v in present),
    }


def _non_csv_format(body: bytes) -> str | None:
    for signature, name in NON_CSV_SIGNATURES.items():
        if body.startswith(signature):
            return name
    return "html" if HTML_START.match(body) else None


def inspect(
    path: Path,
    expected_sha256: str,
    missing_tokens: list[str],
    expected_columns: list[str] | None = None,
) -> dict:
    # ponytail: reads the whole file into memory; candidates are at most tens of MB.
    data = path.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    if sha256 != expected_sha256.lower():
        raise InspectError(f"SHA-256 mismatch: file is {sha256}, expected {expected_sha256}")
    if not data:
        raise InspectError("file is empty")
    has_bom = data.startswith(BOM)
    report: dict = {"sha256": sha256, "bytes": len(data), "bom": has_bom}
    body = data[len(BOM) :] if has_bom else data
    if fmt := _non_csv_format(body):
        return {**report, "status": "unsupported_format", "format": fmt}
    try:
        text = body.decode("utf-8")
    except UnicodeDecodeError as e:
        offset = e.start + (len(BOM) if has_bom else 0)
        return {**report, "status": "decode_error", "decode_error_offset": offset}
    if "\x00" in text:
        return {**report, "status": "parse_error", "parse_error": "NUL byte"}
    csv.field_size_limit(len(text) + 1)
    try:
        rows = list(csv.reader(io.StringIO(text, newline=""), strict=True))
    except csv.Error as e:
        # csv.Error messages describe the fault and do not quote cell text.
        return {**report, "status": "parse_error", "parse_error": str(e)}
    if not rows or not rows[0]:
        raise InspectError("file is empty: no header row")
    header, *records = rows
    # A file with no header row would otherwise print its first record as the header.
    absent = sum(name not in header for name in expected_columns or [])
    if absent:
        return {**report, "status": "header_mismatch", "expected_columns_missing": absent}
    if len(set(header)) != len(header):
        raise InspectError("duplicate column names in the header row")
    records_with_cells = [r for r in records if r]
    regular = [r for r in records_with_cells if len(r) == len(header)]
    return {
        **report,
        "status": "ok",
        "header": header,
        "data_rows": len(records_with_cells),
        "blank_rows": len(records) - len(records_with_cells),
        "ragged_rows": len(records_with_cells) - len(regular),
        "columns": {
            name: _column([r[i] for r in regular], missing_tokens) for i, name in enumerate(header)
        },
    }


def render(report: dict) -> str:
    return json.dumps(report, indent=2, sort_keys=True)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("path", type=Path)
    p.add_argument("--sha256", required=True, help="recorded checksum of the file")
    p.add_argument(
        "--missing-token",
        action="append",
        default=[],
        help="a value the publisher documents as missing, such as NA (repeatable)",
    )
    p.add_argument(
        "--expected-column",
        action="append",
        help="a column the platform field list names; if absent, the header is not printed "
        "(repeatable)",
    )
    args = p.parse_args()
    try:
        report = inspect(args.path, args.sha256, args.missing_token, args.expected_column)
    except (InspectError, OSError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    print(render(report))
    return 0 if report["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
