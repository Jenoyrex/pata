"""Version 1 readiness (ADR-0009). SYNTHETIC fixtures only: Testland is fictional, not LGD data."""

import re
import subprocess
import sys
from pathlib import Path

import pytest
from openpyxl import Workbook
from test_gazetteer import _xlsx_value, fixture_sources, read, write_sources

from pata.normalize import name_key

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "scripts" / "build_gazetteer.py"
GUIDE = ROOT / "docs" / "toolkit.md"
NEW_FILE = "states_new_download.xlsx"
NO_BENCHMARK = "no address dataset, model, benchmark or metric"
ACKNOWLEDGEMENT = "Source: Local Government Directory (LGD), Ministry of Panchayati Raj"


def cli(mdir: Path, rdir: Path, *args: str) -> subprocess.CompletedProcess:
    command = [sys.executable, str(BUILD), "--manifests", str(mdir), "--raw", str(rdir), *args]
    return subprocess.run(command, capture_output=True, text=True, encoding="utf-8", cwd=ROOT)


def new_download(tmp_path: Path) -> tuple[Path, Path]:
    """A workbook with a new name and one more row, saved where the guide says."""
    sources = fixture_sources()
    mdir, rdir = write_sources(tmp_path, sources, xlsx=("states",))
    rows = [*sources["states"][2], dict(code="92", name="Otherland")]
    (rdir / "states.xlsx").unlink()
    (rdir / "lgdirectory.gov.in").mkdir()
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(["Fixture states"])
    sheet.append(list(rows[0]))
    for row in rows:
        sheet.append([_xlsx_value(column, value) for column, value in row.items()])
    workbook.save(rdir / "lgdirectory.gov.in" / NEW_FILE)
    return mdir, rdir


def set_raw_file(mdir: Path, value: str) -> None:
    path = mdir / "states.toml"
    text = re.sub(r'raw_file = "[^"]+"', f'raw_file = "{value}"', path.read_text(encoding="utf-8"))
    path.write_text(text, encoding="utf-8")


def repin(mdir: Path, rdir: Path) -> None:
    """Follow the guide: set raw_file, then copy each printed [snapshot] into its manifest."""
    set_raw_file(mdir, f"lgdirectory.gov.in/{NEW_FILE}")
    printed = cli(mdir, rdir, "--snapshot-info").stdout
    blocks = re.findall(
        r'# (\S+\.toml)\s[^\n]*\n.*?retrieved = "([^"]+)"\nsha256 = "(\w+)"\nrows = (\d+)\n',
        printed,
        re.S,
    )
    assert len(blocks) == len(fixture_sources())
    for name, retrieved, sha256, rows in blocks:
        path = mdir / name
        text = path.read_text(encoding="utf-8")
        text = re.sub(r'retrieved = "[^"]+"', f'retrieved = "{retrieved}"', text)
        text = re.sub(r'sha256 = "\w+"', f'sha256 = "{sha256}"', text)
        path.write_text(re.sub(r"rows = \d+", f"rows = {rows}", text), encoding="utf-8")


def test_bare_file_name_is_not_found(tmp_path):
    mdir, rdir = new_download(tmp_path)
    set_raw_file(mdir, NEW_FILE)
    assert "not found" in cli(mdir, rdir, "--snapshot-info").stdout


def test_new_snapshot_is_refused_until_repinned(tmp_path):
    mdir, rdir = new_download(tmp_path)
    set_raw_file(mdir, f"lgdirectory.gov.in/{NEW_FILE}")
    refused = cli(mdir, rdir, "--out", str(tmp_path / "refused"))
    assert refused.returncode == 2
    assert "sha256" in refused.stderr
    repin(mdir, rdir)
    built = cli(mdir, rdir, "--out", str(tmp_path / "out"))
    assert built.returncode == 0, built.stderr
    assert "lgd:state:92" in {r["id"] for r in read(tmp_path / "out" / "admin_unit.csv")}


def test_repinned_build_is_deterministic(tmp_path):
    mdir, rdir = new_download(tmp_path)
    repin(mdir, rdir)
    assert cli(mdir, rdir, "--out", str(tmp_path / "a")).returncode == 0
    assert cli(mdir, rdir, "--out", str(tmp_path / "b")).returncode == 0
    for path in (tmp_path / "a").iterdir():
        assert path.read_bytes() == (tmp_path / "b" / path.name).read_bytes(), path.name


def test_guide_gives_the_working_raw_file_form():
    assert "`lgdirectory.gov.in/<your file name>`" in GUIDE.read_text(encoding="utf-8")


@pytest.mark.parametrize("doc", [GUIDE, ROOT / "README.md"])
def test_docs_state_what_version_1_is_not(doc):
    assert NO_BENCHMARK in " ".join(doc.read_text(encoding="utf-8").split())


def test_guide_carries_the_lgd_acknowledgement():
    assert ACKNOWLEDGEMENT in " ".join(GUIDE.read_text(encoding="utf-8").split())


def test_guide_name_key_example_is_correct():
    assert name_key("Mahatma  Gandhi Rd.") == "mahatma gandhi rd"
    assert '"mahatma gandhi rd"' in GUIDE.read_text(encoding="utf-8")
