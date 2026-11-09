"""SYNTHETIC fixtures only: every cell below is invented for these tests."""

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "source_stats.py"
spec = importlib.util.spec_from_file_location("source_stats", SCRIPT)
source_stats = importlib.util.module_from_spec(spec)
sys.modules["source_stats"] = source_stats
spec.loader.exec_module(source_stats)

SECRET = "SYNTHETICSECRET"
GOOD = (
    "Name,Address,Pincode,Note\n"
    f"{SECRET} One,12 Fake Road Testville,600001,NA\n"
    f"{SECRET} Two,,600002,\n"
    f"{SECRET} Three,9 Other Lane,not a pin,x@example.invalid 9876543210\n"
).encode()


def write(tmp_path, data: bytes) -> tuple[Path, str]:
    path = tmp_path / "synthetic.csv"
    path.write_bytes(data)
    return path, hashlib.sha256(data).hexdigest()


def test_counts_header_and_shapes(tmp_path):
    path, sha = write(tmp_path, GOOD)
    report = source_stats.inspect(path, sha, ["NA"])
    assert report["status"] == "ok"
    assert report["sha256"] == sha
    assert report["bytes"] == len(GOOD)
    assert report["bom"] is False
    assert report["header"] == ["Name", "Address", "Pincode", "Note"]
    assert report["data_rows"] == 3
    assert report["ragged_rows"] == 0
    columns = report["columns"]
    assert columns["Address"]["empty"] == 1
    assert columns["Address"]["tokens"] == {"min": 3, "median": 3.5, "max": 4}
    assert columns["Note"]["missing_tokens"] == {"NA": 1}
    assert columns["Pincode"]["six_digit_run"] == 2
    assert columns["Note"]["email_like"] == 1
    assert columns["Note"]["ten_digit_run"] == 1


def test_report_never_contains_a_cell_value(tmp_path):
    path, sha = write(tmp_path, GOOD)
    text = json.dumps(source_stats.inspect(path, sha, ["NA"]))
    for leaked in (SECRET, "Fake Road", "Testville", "example.invalid", "9876543210", "600001"):
        assert leaked not in text


def test_two_runs_are_byte_identical(tmp_path):
    path, sha = write(tmp_path, GOOD)
    first = source_stats.render(source_stats.inspect(path, sha, ["NA"]))
    second = source_stats.render(source_stats.inspect(path, sha, ["NA"]))
    assert first == second


def test_checksum_mismatch_refuses_before_reading(tmp_path):
    path, _ = write(tmp_path, GOOD)
    with pytest.raises(source_stats.InspectError, match="SHA-256"):
        source_stats.inspect(path, "0" * 64, [])


def test_invalid_utf8_is_reported_without_replacement(tmp_path):
    data = b"Name,Address\n" + SECRET.encode() + b",bad\xff byte\n"
    path, sha = write(tmp_path, data)
    report = source_stats.inspect(path, sha, [])
    assert report["status"] == "decode_error"
    assert report["decode_error_offset"] == data.index(b"\xff")
    assert "columns" not in report
    assert SECRET not in json.dumps(report)


def test_bom_is_recorded_and_not_part_of_the_header(tmp_path):
    path, sha = write(tmp_path, b"\xef\xbb\xbfName,Address\na,b\n")
    report = source_stats.inspect(path, sha, [])
    assert report["bom"] is True
    assert report["header"] == ["Name", "Address"]


def test_ragged_rows_are_counted_and_not_folded_into_columns(tmp_path):
    path, sha = write(tmp_path, b"A,B\n1,2\n1,2,3\n4\n")
    report = source_stats.inspect(path, sha, [])
    assert report["data_rows"] == 3
    assert report["ragged_rows"] == 2
    assert report["columns"]["A"]["non_empty"] == 1


def test_empty_file_and_duplicate_headers_are_errors(tmp_path):
    path, sha = write(tmp_path, b"")
    with pytest.raises(source_stats.InspectError, match="empty"):
        source_stats.inspect(path, sha, [])
    path, sha = write(tmp_path, b"A,A\n1,2\n")
    with pytest.raises(source_stats.InspectError, match="duplicate"):
        source_stats.inspect(path, sha, [])


def test_nul_byte_is_a_structured_error(tmp_path):
    path, sha = write(tmp_path, b"A,B\n1,\x002\n")
    report = source_stats.inspect(path, sha, [])
    assert report["status"] == "parse_error"
    assert "columns" not in report


def test_cli_prints_report_and_exits_zero(tmp_path, capsys, monkeypatch):
    path, sha = write(tmp_path, GOOD)
    monkeypatch.setattr(sys, "argv", ["source_stats.py", str(path), "--sha256", sha])
    assert source_stats.main() == 0
    assert json.loads(capsys.readouterr().out)["data_rows"] == 3


def test_cli_exits_nonzero_on_checksum_mismatch(tmp_path, capsys, monkeypatch):
    path, _ = write(tmp_path, GOOD)
    monkeypatch.setattr(sys, "argv", ["source_stats.py", str(path), "--sha256", "0" * 64])
    assert source_stats.main() == 2
    assert "SHA-256" in capsys.readouterr().err
