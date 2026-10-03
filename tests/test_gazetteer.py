"""Gazetteer build tests. All fixture data is fictional (Testland), not real places."""

import csv
import hashlib
import json
from pathlib import Path

import pytest
from openpyxl import Workbook

from pata import gazetteer
from pata.gazetteer import BuildError, load_manifests, run

ROOT = Path(__file__).resolve().parents[1]
REPO_MANIFESTS = ROOT / "data" / "manifests"
LGD_CORE = ("lgd_states", "lgd_districts", "lgd_subdistricts", "lgd_villages_pincode")

V = dict(state_code="91", state_name="Testland", district_code="9101", district_name="North Test")


def fixture_sources():
    office = dict(
        office_type="BO",
        delivery="Delivery",
        circle="Test Circle",
        region="Test Region",
        division="Test Division",
        district_name="NORTH TEST",
        state_name="TESTLAND",
    )
    return {
        "states": ("admin_unit", "state", [dict(code="91", name="Testland")]),
        "districts": (
            "admin_unit",
            "district",
            [dict(code="9101", name="North Test", parent_code="91")],
        ),
        "subdistricts": (
            "admin_unit",
            "subdistrict",
            [
                dict(code="910101", name="Alpha Tehsil", parent_code="9101"),
                dict(code="910102", name="Beta Tehsil", parent_code="9101"),
            ],
        ),
        "villages": (
            "lgd_village_pincode",
            None,
            [
                {
                    **V,
                    "subdistrict_code": "910101",
                    "subdistrict_name": "Alpha Tehsil",
                    "village_code": "9100001",
                    "village_name": "Rampur Test",
                    "pincode": "990001",
                },
                {
                    **V,
                    "subdistrict_code": "910101",
                    "subdistrict_name": "Alpha Tehsil",
                    "village_code": "9100001",
                    "village_name": "Rampur Test",
                    "pincode": "990002",
                },
                {
                    **V,
                    "subdistrict_code": "910102",
                    "subdistrict_name": "Beta Tehsil",
                    "village_code": "9100002",
                    "village_name": "Kheda Test",
                    "pincode": "",
                },
            ],
        ),  # fmt: skip
        "offices": (
            "post_office",
            None,
            [
                dict(
                    pincode="990001",
                    office_name="Rampur Test B.O",
                    **office,
                    latitude="20.5",
                    longitude="78.9",
                ),
                dict(
                    pincode="990002",
                    office_name="Beta S.O",
                    **office,
                    latitude="NA",
                    longitude="NA",
                ),
            ],
        ),  # fmt: skip
    }


def _xlsx_value(col: str, v: str):
    """Store codes and PINs as numeric cells, as the LGD portal does (35 -> 35.0)."""
    if not v:
        return None
    return float(v) if col.endswith("code") or col == "pincode" else v


def write_sources(root: Path, sources: dict, xlsx=()) -> tuple[Path, Path]:
    """Write fixture raw files and manifests. Sources named in xlsx are LGD-style workbooks."""
    mdir, rdir = root / "manifests", root / "raw"
    mdir.mkdir(parents=True)
    rdir.mkdir()
    for sid, (entity, level, rows) in sources.items():
        header = list(rows[0])
        if sid in xlsx:
            raw = rdir / f"{sid}.xlsx"
            wb = Workbook()
            ws = wb.active
            ws.append([f"Fixture {sid}"])  # row 1: report title
            ws.append(header)  # row 2: header
            for r in rows:
                ws.append([_xlsx_value(c, r[c]) for c in header])
            wb.save(raw)
        else:
            raw = rdir / f"{sid}.csv"
            with raw.open("w", encoding="utf-8", newline="") as f:
                w = csv.DictWriter(f, header, lineterminator="\n")
                w.writeheader()
                w.writerows(rows)
        lines = [f'{k} = "fixture"' for k in gazetteer.MANIFEST_KEYS[1:10]]
        lines += [f'id = "{sid}"', f'entity = "{entity}"', f'raw_file = "{raw.name}"']
        lines += [f'level = "{level}"'] if level else []
        if sid in xlsx:
            lines += [f'title = "Fixture {sid}"', f"header = {json.dumps(header)}"]
        lines += [
            "[snapshot]",
            'retrieved = "2026-01-01"',
            f'sha256 = "{hashlib.sha256(raw.read_bytes()).hexdigest()}"',
            f"rows = {len(rows)}",
            "[columns]",
            *(f'{c} = "{c}"' for c in rows[0]),
        ]
        (mdir / f"{sid}.toml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return mdir, rdir


def read(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def codes(out: Path) -> set[str]:
    return {i["code"] for i in read(out / "issues.csv")}


def test_build_succeeds(tmp_path):
    mdir, rdir = write_sources(tmp_path, fixture_sources())
    assert run(mdir, rdir, tmp_path / "out") == 0
    units = {u["id"]: u for u in read(tmp_path / "out" / "admin_unit.csv")}
    assert len(units) == 6  # 1 state, 1 district, 2 subdistricts, 2 villages
    assert units["lgd:village:9100001"]["parent_id"] == "lgd:subdistrict:910101"
    assert len(read(tmp_path / "out" / "village_pincode.csv")) == 2
    offices = {o["id"]: o for o in read(tmp_path / "out" / "post_office.csv")}
    assert offices["dop:po:990002:beta-s-o"]["latitude"] == ""  # "NA" blanked, not invented
    # India Post labels are kept raw, never resolved to LGD units.
    assert offices["dop:po:990001:rampur-test-b-o"]["district_name"] == "NORTH TEST"
    assert codes(tmp_path / "out") == {"unparseable_coordinate", "village_row_without_pincode"}


def test_build_is_deterministic(tmp_path):
    mdir, rdir = write_sources(tmp_path, fixture_sources())
    run(mdir, rdir, tmp_path / "a")
    run(mdir, rdir, tmp_path / "b")
    files = sorted(p.name for p in (tmp_path / "a").iterdir())
    assert len(files) == 6
    for name in files:
        assert (tmp_path / "a" / name).read_bytes() == (tmp_path / "b" / name).read_bytes()


def test_changed_file_is_rejected(tmp_path):
    mdir, rdir = write_sources(tmp_path, fixture_sources())
    with (rdir / "states.csv").open("a", encoding="utf-8") as f:
        f.write("92,Otherland\n")
    with pytest.raises(BuildError, match="sha256"):
        run(mdir, rdir, tmp_path / "out")


def test_row_count_must_match_manifest(tmp_path):
    mdir, rdir = write_sources(tmp_path, fixture_sources())
    p = mdir / "states.toml"
    p.write_text(p.read_text(encoding="utf-8").replace("rows = 1", "rows = 2"), encoding="utf-8")
    with pytest.raises(BuildError, match="parsed 1 rows"):
        run(mdir, rdir, tmp_path / "out")


def test_unmapped_required_column_is_rejected(tmp_path):
    mdir, rdir = write_sources(tmp_path, fixture_sources())
    p = mdir / "districts.toml"
    text = p.read_text(encoding="utf-8").replace('parent_code = "parent_code"', 'parent_code = ""')
    p.write_text(text, encoding="utf-8")
    with pytest.raises(BuildError, match="mapping incomplete"):
        run(mdir, rdir, tmp_path / "out")


def test_mapped_column_missing_from_header_is_rejected(tmp_path):
    mdir, rdir = write_sources(tmp_path, fixture_sources())
    p = mdir / "states.toml"
    p.write_text(p.read_text(encoding="utf-8").replace('name = "name"', 'name = "nm"'), "utf-8")
    with pytest.raises(BuildError, match="not in header"):
        run(mdir, rdir, tmp_path / "out")


def test_broken_parent_fails_build_and_writes_no_tables(tmp_path):
    src = fixture_sources()
    src["subdistricts"][2][1]["parent_code"] = "9999"
    mdir, rdir = write_sources(tmp_path, src)
    assert run(mdir, rdir, tmp_path / "out") == 1
    assert "broken_parent" in codes(tmp_path / "out")
    assert not (tmp_path / "out" / "admin_unit.csv").exists()


def test_hierarchy_mismatch_between_lgd_files(tmp_path):
    src = fixture_sources()
    src["districts"][2].append(dict(code="9102", name="South Test", parent_code="91"))
    src["villages"][2][2]["district_code"] = "9102"  # file claims 910102 lies in 9102
    mdir, rdir = write_sources(tmp_path, src)
    assert run(mdir, rdir, tmp_path / "out") == 1
    assert "hierarchy_mismatch" in codes(tmp_path / "out")


def test_post_office_duplicates(tmp_path):
    src = fixture_sources()
    offices = src["offices"][2]
    offices.append(dict(offices[0]))  # exact duplicate: dropped with a warning
    offices.append({**offices[0], "office_name": "RAMPUR TEST B.O."})  # same normalized key
    mdir, rdir = write_sources(tmp_path, src)
    assert run(mdir, rdir, tmp_path / "out") == 1
    assert {"exact_duplicate_row", "name_key_collision"} <= codes(tmp_path / "out")


def test_invalid_codes_are_errors(tmp_path):
    src = fixture_sources()
    src["offices"][2][0]["pincode"] = "09900"
    src["states"][2][0]["code"] = "9A"
    mdir, rdir = write_sources(tmp_path, src)
    assert run(mdir, rdir, tmp_path / "out") == 1
    assert {"invalid_pincode", "invalid_lgd_code"} <= codes(tmp_path / "out")


def edit(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    assert old in text
    path.write_text(text.replace(old, new), encoding="utf-8")


LGD_XLSX = ("states", "districts", "subdistricts", "villages")


def test_xlsx_sources_are_decoded(tmp_path):
    src = fixture_sources()
    for r in src["villages"][2][:2]:  # both PIN rows of village 9100001
        r["village_name"] = " Rampur Test  "  # stored text is kept as is
    mdir, rdir = write_sources(tmp_path, src, xlsx=LGD_XLSX)
    assert run(mdir, rdir, tmp_path / "out") == 0
    units = {u["id"]: u for u in read(tmp_path / "out" / "admin_unit.csv")}
    assert units["lgd:district:9101"]["lgd_code"] == "9101"  # numeric cell 9101.0 -> "9101"
    assert units["lgd:district:9101"]["parent_id"] == "lgd:state:91"
    assert units["lgd:village:9100001"]["name"] == " Rampur Test  "
    links = read(tmp_path / "out" / "village_pincode.csv")
    assert {lk["pincode"] for lk in links} == {"990001", "990002"}


def test_xlsx_non_integral_number_is_rejected(tmp_path):
    src = fixture_sources()
    src["villages"][2][0]["pincode"] = "990001.5"
    mdir, rdir = write_sources(tmp_path, src, xlsx=LGD_XLSX)
    with pytest.raises(BuildError, match="never rounded"):
        run(mdir, rdir, tmp_path / "out")


def test_xlsx_title_must_match_manifest(tmp_path):
    mdir, rdir = write_sources(tmp_path, fixture_sources(), xlsx=LGD_XLSX)
    edit(mdir / "states.toml", 'title = "Fixture states"', 'title = "All States"')
    with pytest.raises(BuildError, match="row 1"):
        run(mdir, rdir, tmp_path / "out")


def test_xlsx_header_must_match_manifest(tmp_path):
    mdir, rdir = write_sources(tmp_path, fixture_sources(), xlsx=LGD_XLSX)
    edit(mdir / "districts.toml", '"parent_code"]', '"parent code"]')
    with pytest.raises(BuildError, match="row 2 header"):
        run(mdir, rdir, tmp_path / "out")


def test_deferred_source_is_skipped(tmp_path):
    src = fixture_sources()
    src["villages"][2][0]["pincode"] = "990009"  # not an India Post PIN in the fixture
    mdir, rdir = write_sources(tmp_path, src)
    p = mdir / "offices.toml"
    p.write_text('deferred = "not built"\n' + p.read_text(encoding="utf-8"), encoding="utf-8")
    (rdir / "offices.csv").unlink()  # a deferred source needs no raw file
    assert run(mdir, rdir, tmp_path / "out") == 0
    assert read(tmp_path / "out" / "post_office.csv") == []
    assert "pincode_not_in_dop" not in codes(tmp_path / "out")  # no DoP list to compare with
    info = json.loads((tmp_path / "out" / "build_info.json").read_text(encoding="utf-8"))
    assert info["sources"]["offices"]["deferred"] == "not built"


def test_repo_manifests_are_complete():
    manifests = {m["id"]: m for _, m in load_manifests(REPO_MANIFESTS)}
    assert set(manifests) == {"dop_pincode_directory", *LGD_CORE}
    for m in manifests.values():
        assert m["license"] and m["license_url"] and m["publisher"] and m["attribution"]
    assert manifests["dop_pincode_directory"]["deferred"]  # India Post deferred (ADR-0004)
    for sid in LGD_CORE:
        m = manifests[sid]
        assert m["dataset_url"] == "https://lgdirectory.gov.in/downloadDirectory.do"
        assert m["license_url"] == "https://lgdirectory.gov.in/copyRightPolicy.do"
        assert m["raw_file"].startswith("lgdirectory.gov.in/") and m["raw_file"].endswith(".xlsx")
        assert m["report"] and m["report_generated"] and m["snapshot"]["sha256"]
        assert "deferred" not in m


REAL_RAW = ROOT / "data" / "raw"
REAL_FILES = [REAL_RAW / m["raw_file"] for _, m in load_manifests(REPO_MANIFESTS)
              if m["id"] in LGD_CORE]  # fmt: skip


@pytest.mark.skipif(
    not all(f.is_file() for f in REAL_FILES), reason="pinned LGD snapshots not in data/raw"
)
def test_real_lgd_snapshots_build(tmp_path):
    """Full build against the real pinned LGD files (slow; skipped when they are absent)."""
    assert run(REPO_MANIFESTS, REAL_RAW, tmp_path) == 0
    info = json.loads((tmp_path / "build_info.json").read_text(encoding="utf-8"))
    assert info["rows"]["admin_unit"] == 36 + 784 + 7092 + 672619
    assert info["rows"]["village_pincode"] == 672619
    assert not [k for k in info["issues"] if k.startswith("error:")]
