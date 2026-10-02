"""Gazetteer build tests. All fixture data is fictional (Testland), not real places."""

import csv
import hashlib
from pathlib import Path

import pytest

from pata import gazetteer
from pata.gazetteer import BuildError, load_manifests, run

REPO_MANIFESTS = Path(__file__).resolve().parents[1] / "data" / "manifests"

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


def write_sources(root: Path, sources: dict) -> tuple[Path, Path]:
    mdir, rdir = root / "manifests", root / "raw"
    mdir.mkdir(parents=True)
    rdir.mkdir()
    for sid, (entity, level, rows) in sources.items():
        raw = rdir / f"{sid}.csv"
        with raw.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, list(rows[0]), lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
        lines = [f'{k} = "fixture"' for k in gazetteer.MANIFEST_KEYS[1:10]]
        lines += [f'id = "{sid}"', f'entity = "{entity}"', f'raw_file = "{sid}.csv"']
        lines += [f'level = "{level}"'] if level else []
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


def test_repo_manifests_are_complete():
    manifests = load_manifests(REPO_MANIFESTS)
    assert {m["id"] for _, m in manifests} == {
        "dop_pincode_directory",
        "lgd_states",
        "lgd_districts",
        "lgd_subdistricts",
        "lgd_villages_pincode",
    }
    for _, m in manifests:
        assert m["license"] and m["license_url"] and m["publisher"] and m["attribution"]
        assert m["dataset_url"].startswith("https://www.data.gov.in/")
