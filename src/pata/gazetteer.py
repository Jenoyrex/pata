"""India-wide reference gazetteer: pinned source snapshots -> canonical tables.

Publishers' concepts are kept apart. LGD administrative units and India Post
post offices live in separate tables and are linked only where a source itself
states the link (LGD's village -> PIN code crosswalk). India Post's district and
state labels stay raw strings; they are NOT resolved to LGD units here.
See docs/gazetteer.md and docs/decisions/0002-gazetteer-sources-and-schema.md
(XLSX sources: 0004-lgd-portal-xlsx-snapshots.md).
"""

import csv
import hashlib
import json
import math
import re
import subprocess
import tomllib
import warnings
from collections import Counter, defaultdict
from collections.abc import Iterator
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

from openpyxl import load_workbook

from pata import __version__
from pata.normalize import name_key

PARENT_LEVEL = {"district": "state", "subdistrict": "district", "village": "subdistrict"}
LEVELS = ("state", *PARENT_LEVEL)

TABLES = {
    "admin_unit": ("id", "level", "lgd_code", "name", "name_local", "parent_id", "source"),
    "post_office": (
        "id",
        "pincode",
        "office_name",
        "office_type",
        "delivery",
        "circle",
        "region",
        "division",
        "district_name",
        "state_name",
        "latitude",
        "longitude",
        "source",
    ),
    "pincode": ("pincode", "office_count", "district_names", "state_names"),
    "village_pincode": ("village_id", "pincode", "source"),
}
ISSUE_FIELDS = ("severity", "code", "entity_id", "message")

# Canonical source columns per manifest entity: (required, optional).
SOURCE_COLUMNS = {
    "admin_unit": (("code", "name", "parent_code"), ("name_local",)),
    "post_office": (("pincode", "office_name"), TABLES["post_office"][3:12]),
    "lgd_village_pincode": (
        (
            "state_code",
            "state_name",
            "district_code",
            "district_name",
            "subdistrict_code",
            "subdistrict_name",
            "village_code",
            "village_name",
            "pincode",
        ),
        (),
    ),
}
MANIFEST_KEYS = (
    "id",
    "name",
    "publisher",
    "distributor",
    "dataset_url",
    "license",
    "license_url",
    "redistribution",
    "attribution",
    "retrieval",
    "entity",
    "raw_file",
    "snapshot",
    "columns",
)

PINCODE_RE = re.compile(r"[1-9][0-9]{5}")
LGD_CODE_RE = re.compile(r"[0-9]+")
# ponytail: rough lat/lon box around India, used only to flag suspicious points.
# Not a boundary; replace with a real boundary check when geocoding starts.
INDIA_BBOX = (6.0, 38.0, 68.0, 98.0)


class BuildError(Exception):
    """A source cannot be used as-is (missing, unpinned, changed, or unmapped)."""


@dataclass(frozen=True)
class Issue:
    severity: str  # error | warning | info
    code: str
    entity_id: str
    message: str


def check_manifest(m: dict, path: Path) -> list[str]:
    problems = [f"missing key {k!r}" for k in MANIFEST_KEYS if k not in m]
    if m.get("id") != path.stem:
        problems.append("id must equal the file name")
    if m.get("entity") not in SOURCE_COLUMNS:
        problems.append(f"unknown entity {m.get('entity')!r}")
    if m.get("entity") == "admin_unit" and m.get("level") not in LEVELS:
        problems.append(f"admin_unit needs level in {LEVELS}")
    if not {"retrieved", "sha256", "rows"} <= set(m.get("snapshot", {})):
        problems.append("snapshot needs retrieved, sha256, rows")
    if str(m.get("raw_file", "")).endswith(".xlsx") and not (
        isinstance(m.get("title"), str) and isinstance(m.get("header"), list)
    ):
        problems.append("an .xlsx source needs title (row 1) and header (row 2)")
    return problems


def load_manifests(manifest_dir: Path) -> list[tuple[Path, dict]]:
    out = []
    for path in sorted(manifest_dir.glob("*.toml")):
        m = tomllib.loads(path.read_text(encoding="utf-8"))
        if problems := check_manifest(m, path):
            raise BuildError(f"{path}: {'; '.join(problems)}")
        out.append((path, m))
    if not out:
        raise BuildError(f"no manifests in {manifest_dir}")
    return out


def sha256_file(path: Path) -> str:
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def _xlsx_rows(path: Path) -> Iterator[tuple]:
    """Cell values of the first worksheet, row by row."""
    with warnings.catch_warnings():
        # LGD portal workbooks carry no default style; irrelevant for reading values.
        warnings.filterwarnings("ignore", "Workbook contains no default style")
        wb = load_workbook(path, read_only=True, data_only=True)
    try:
        yield from wb.worksheets[0].iter_rows(values_only=True)
    finally:
        wb.close()


def _xlsx_cell(v, where: str) -> str:
    """Decode a stored cell to the published text (ADR-0004 section 4). Not normalization."""
    if v is None:
        return ""
    if isinstance(v, str):
        return v  # exactly as stored, whitespace included
    if isinstance(v, int) and not isinstance(v, bool):
        return str(v)
    if isinstance(v, float) and v.is_integer():
        return str(int(v))  # numeric cell 35.0 -> "35"
    raise BuildError(f"{where}: cannot decode {type(v).__name__} cell {v!r}; never rounded")


def _read_xlsx(m: dict, path: Path, cols: dict[str, str]) -> list[dict[str, str]]:
    """Row 1 = report title, row 2 = header, data from row 3; all checked against the manifest."""
    sid, rows = m["id"], _xlsx_rows(path)
    title = [c for c in next(rows, ()) if c is not None]
    if title != [m["title"]]:
        raise BuildError(f"{sid}: row 1 is {title}, manifest title is {m['title']!r}")
    header = list(next(rows, ()))
    if header != m["header"]:
        raise BuildError(f"{sid}: row 2 header {header} != manifest header {m['header']}")
    if missing := [v for v in cols.values() if v not in header]:
        raise BuildError(f"{sid}: columns {missing} not in header {header}")
    idx = {k: header.index(v) for k, v in cols.items()}
    return [
        {k: _xlsx_cell(r[i] if i < len(r) else None, f"{sid} row {n} {cols[k]!r}")
         for k, i in idx.items()}
        for n, r in enumerate(rows, start=3)
    ]  # fmt: skip


def _read_csv(sid: str, path: Path, cols: dict[str, str]) -> list[dict[str, str]]:
    try:
        with path.open(encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            header = {h.strip().casefold(): h for h in reader.fieldnames or ()}
            if missing := [v for v in cols.values() if v.strip().casefold() not in header]:
                raise BuildError(f"{sid}: columns {missing} not in header {reader.fieldnames}")
            src = {k: header[v.strip().casefold()] for k, v in cols.items()}
            return [{k: (r[h] or "").strip() for k, h in src.items()} for r in reader]
    except UnicodeDecodeError as e:
        raise BuildError(f"{sid}: not UTF-8 ({e})") from e


def read_source(m: dict, raw_dir: Path) -> list[dict[str, str]]:
    """Read a pinned raw file into rows keyed by canonical column names."""
    sid, path, snap = m["id"], raw_dir / m["raw_file"], m["snapshot"]
    if not path.is_file():
        raise BuildError(f"{sid}: {path} not found. Retrieval: {m['retrieval'].strip()}")
    digest = sha256_file(path)
    if digest != snap["sha256"]:
        raise BuildError(
            f"{sid}: sha256 {digest} != pinned {snap['sha256'] or '(not pinned)'}. "
            "If this is a new snapshot, run --snapshot-info and update the manifest."
        )
    required, optional = SOURCE_COLUMNS[m["entity"]]
    if m.get("level") == "state":
        required = tuple(c for c in required if c != "parent_code")
    cols = {k: v for k, v in m["columns"].items() if v}
    if unmapped := [c for c in required if c not in cols]:
        raise BuildError(
            f"{sid}: column mapping incomplete {unmapped}; inspect the file header "
            "(--snapshot-info) and fill [columns] in the manifest"
        )
    if unknown := sorted(set(cols) - set(required) - set(optional)):
        raise BuildError(f"{sid}: unknown canonical columns {unknown}")
    rows = _read_xlsx(m, path, cols) if path.suffix == ".xlsx" else _read_csv(sid, path, cols)
    if len(rows) != snap["rows"]:
        raise BuildError(f"{sid}: parsed {len(rows)} rows, manifest pins {snap['rows']}")
    return rows


def snapshot_info(manifest_dir: Path, raw_dir: Path) -> str:
    """Checksums, row counts and headers of raw files, for pinning in manifests."""
    out = []
    for path, m in load_manifests(manifest_dir):
        f = raw_dir / m["raw_file"]
        if m.get("deferred"):
            out.append(f"# {m['id']}: deferred ({m['deferred']})\n")
            continue
        if not f.is_file():
            out.append(f"# {m['id']}: {f} not found\n")
            continue
        title = ""
        if f.suffix == ".xlsx":
            it = _xlsx_rows(f)
            title = f"# title (row 1): {[c for c in next(it, ()) if c is not None]}\n"
            header = list(next(it, ()))
            rows = sum(1 for _ in it)
        else:
            with f.open(encoding="utf-8-sig", newline="") as fh:
                reader = csv.reader(fh)
                header = next(reader, [])
                rows = sum(1 for _ in reader)
        retrieved = date.fromtimestamp(f.stat().st_mtime).isoformat()
        out.append(
            f"# {path.name}  (retrieved = file modification date; correct it if needed)\n"
            f"{title}# header: {header}\n[snapshot]\n"
            f'retrieved = "{retrieved}"\nsha256 = "{sha256_file(f)}"\nrows = {rows}\n'
        )
    return "\n".join(out)


def _admin_row(r: dict, m: dict) -> dict:
    level, parent = m["level"], r.get("parent_code", "")
    return {
        "id": f"lgd:{level}:{r['code']}",
        "level": level,
        "lgd_code": r["code"],
        "name": r["name"],
        "name_local": r.get("name_local", ""),
        "parent_id": f"lgd:{PARENT_LEVEL[level]}:{parent}" if level != "state" and parent else "",
        "source": m["id"],
    }


def _office_row(r: dict, m: dict) -> dict:
    row = {f: r.get(f, "") for f in TABLES["post_office"]}
    row["id"] = f"dop:po:{r['pincode']}:{name_key(r['office_name']).replace(' ', '-')}"
    row["source"] = m["id"]
    return row


def _village_rows(rows: list[dict], m: dict):
    """LGD village->PIN file: village units, PIN links, and ancestor claims to cross-check."""
    units, links, claims, seen, no_pin = [], [], set(), {}, 0
    for r in rows:
        st, di, sd = (f"lgd:{lv}:{r[f'{lv}_code']}" for lv in ("state", "district", "subdistrict"))
        v = {
            "id": f"lgd:village:{r['village_code']}",
            "level": "village",
            "lgd_code": r["village_code"],
            "name": r["village_name"],
            "name_local": "",
            "parent_id": sd,
            "source": m["id"],
        }
        if seen.get(v["id"]) != v:  # one row per village-PIN pair is expected
            units.append(v)
            seen[v["id"]] = v
        claims |= {(st, "", r["state_name"]), (di, st, r["district_name"])}
        claims.add((sd, di, r["subdistrict_name"]))
        if r["pincode"]:
            links.append({"village_id": v["id"], "pincode": r["pincode"], "source": m["id"]})
        else:
            no_pin += 1
    issues = [Issue("info", "village_row_without_pincode", "", f"{no_pin} rows")] if no_pin else []
    return units, links, claims, issues


def _dedupe(rows: list[dict], key) -> tuple[list[dict], list[Issue]]:
    kept, issues = {}, []
    for r in rows:
        k = key(r)
        prev = kept.setdefault(k, r)
        if prev is r:
            continue
        if prev == r:
            issues.append(Issue("warning", "exact_duplicate_row", k, "identical row dropped"))
            continue
        diff = sorted(f for f in r if r[f] != prev[f])
        code = "name_key_collision" if "office_name" in diff else "conflicting_duplicate_id"
        issues.append(Issue("error", code, k, f"rows share an id but differ in {diff}"))
    return list(kept.values()), issues


def _float(s: str) -> float | None:
    try:
        x = float(s)
    except ValueError:
        return None
    return x if math.isfinite(x) else None


def _check_coordinates(offices: list[dict]) -> list[Issue]:
    """Blank unparseable coordinates (with an issue each); flag points outside the box."""
    issues, empty = [], 0
    lat0, lat1, lon0, lon1 = INDIA_BBOX
    for o in offices:
        raw = (o["latitude"], o["longitude"])
        lat, lon = _float(raw[0]), _float(raw[1])
        if lat is None or lon is None:
            if any(raw):
                issues.append(Issue("warning", "unparseable_coordinate", o["id"], f"{raw} blanked"))
            else:
                empty += 1
            o["latitude"] = o["longitude"] = ""
        elif not (lat0 <= lat <= lat1 and lon0 <= lon <= lon1):
            issues.append(Issue("warning", "coordinate_outside_india_bbox", o["id"], str(raw)))
    if empty:
        issues.append(Issue("info", "missing_coordinate", "", f"{empty} post offices"))
    return issues


def _check_admin(units: list[dict], claims: set) -> list[Issue]:
    by_id = {u["id"]: u for u in units}
    issues, siblings = [], defaultdict(list)
    for u in units:
        uid = u["id"]
        for f in ("lgd_code", "name"):
            if not u[f]:
                issues.append(Issue("error", "missing_required", uid, f"{f} is empty"))
        if u["lgd_code"] and not LGD_CODE_RE.fullmatch(u["lgd_code"]):
            issues.append(Issue("error", "invalid_lgd_code", uid, repr(u["lgd_code"])))
        if u["level"] != "state":
            if not u["parent_id"]:
                issues.append(Issue("error", "missing_required", uid, "parent code is empty"))
            elif u["parent_id"] not in by_id:
                issues.append(Issue("error", "broken_parent", uid, f"{u['parent_id']} not found"))
        siblings[(u["parent_id"], u["level"], name_key(u["name"]))].append(uid)
    for ids in siblings.values():
        if len(ids) > 1:
            issues.append(
                Issue("warning", "name_key_collision", "|".join(sorted(ids)), "same parent")
            )
    for cid, parent, name in sorted(claims):
        u = by_id.get(cid)
        if u is None:
            issues.append(Issue("error", "unknown_admin_unit", cid, "named in village file only"))
        elif u["parent_id"] != parent:
            msg = f"village file says parent {parent or '(none)'}, level file {u['parent_id']}"
            issues.append(Issue("error", "hierarchy_mismatch", cid, msg))
        elif name_key(u["name"]) != name_key(name):
            msg = f"{name!r} vs {u['name']!r}"
            issues.append(Issue("warning", "cross_source_name_mismatch", cid, msg))
    return issues


def _check_offices(offices: list[dict]) -> list[Issue]:
    issues = []
    for o in offices:
        if not o["office_name"]:
            issues.append(Issue("error", "missing_required", o["id"], "office_name is empty"))
        if not PINCODE_RE.fullmatch(o["pincode"]):
            issues.append(Issue("error", "invalid_pincode", o["id"], repr(o["pincode"])))
    return issues


def _pincodes(offices: list[dict]) -> tuple[list[dict], list[Issue]]:
    groups = defaultdict(list)
    for o in offices:
        groups[o["pincode"]].append(o)
    rows, issues = [], []
    for pin, group in groups.items():
        states = sorted({o["state_name"] for o in group} - {""})
        rows.append(
            {
                "pincode": pin,
                "office_count": str(len(group)),
                "district_names": "|".join(sorted({o["district_name"] for o in group} - {""})),
                "state_names": "|".join(states),
            }
        )
        if len({name_key(s) for s in states}) > 1:
            issues.append(Issue("info", "pincode_spans_states", pin, "|".join(states)))
    return rows, issues


def _check_links(links: list[dict], dop_pincodes: set[str] | None) -> list[Issue]:
    """dop_pincodes is None when India Post is not built: the cross-check is skipped."""
    issues = [
        Issue("error", "invalid_pincode", lk["village_id"], repr(lk["pincode"]))
        for lk in links
        if not PINCODE_RE.fullmatch(lk["pincode"])
    ]
    if dop_pincodes is None:
        return issues
    valid = {lk["pincode"] for lk in links if PINCODE_RE.fullmatch(lk["pincode"])}
    issues += [
        Issue("warning", "pincode_not_in_dop", pin, "LGD village PIN absent from India Post list")
        for pin in sorted(valid - dop_pincodes)
    ]
    return issues


def build(manifest_dir: Path, raw_dir: Path) -> tuple[dict, list[Issue], dict]:
    """Return (tables, issues, sources). Raises BuildError if a source is unusable."""
    admin, offices, links, claims, issues, sources = [], [], [], set(), [], {}
    has_dop = False
    for path, m in load_manifests(manifest_dir):
        if m.get("deferred"):  # kept for provenance, not built (e.g. India Post, ADR-0004)
            sources[m["id"]] = {"manifest": path.name, "deferred": m["deferred"]}
            continue
        has_dop |= m["entity"] == "post_office"
        rows = read_source(m, raw_dir)
        sources[m["id"]] = {"manifest": path.name, "license": m["license"], **m["snapshot"]}
        if m["entity"] == "admin_unit":
            admin += [_admin_row(r, m) for r in rows]
        elif m["entity"] == "post_office":
            offices += [_office_row(r, m) for r in rows]
        else:
            units, lks, cls, found = _village_rows(rows, m)
            admin += units
            links += lks
            claims |= cls
            issues += found
    admin, found = _dedupe(admin, lambda r: r["id"])
    issues += found
    offices, found = _dedupe(offices, lambda r: r["id"])
    issues += found
    links, found = _dedupe(links, lambda r: f"{r['village_id']}|{r['pincode']}")
    issues += found
    issues += _check_admin(admin, claims) + _check_offices(offices) + _check_coordinates(offices)
    pincodes, found = _pincodes(offices)
    dop_pincodes = {p["pincode"] for p in pincodes} if has_dop else None
    issues += found + _check_links(links, dop_pincodes)
    tables = {
        "admin_unit": admin,
        "post_office": offices,
        "pincode": pincodes,
        "village_pincode": links,
    }
    return tables, issues, sources


def _write_csv(path: Path, fields: tuple, rows: list[dict]) -> None:
    rows = sorted(rows, key=lambda r: tuple(r[f] for f in fields))
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def _git_commit() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent,
            check=False,
        )
    except OSError:
        return "unknown"
    return out.stdout.strip() or "unknown"


def run(manifest_dir: Path, raw_dir: Path, out_dir: Path) -> int:
    """Build, validate and write the gazetteer. Tables are written only if no errors."""
    tables, issues, sources = build(manifest_dir, raw_dir)
    ok = not any(i.severity == "error" for i in issues)
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, rows in tables.items():
        path = out_dir / f"{name}.csv"
        if ok:
            _write_csv(path, TABLES[name], rows)
        else:
            path.unlink(missing_ok=True)  # never leave a stale table next to a failed build
    _write_csv(out_dir / "issues.csv", ISSUE_FIELDS, [asdict(i) for i in issues])
    info = {
        "status": "ok" if ok else "failed",
        "pata_version": __version__,
        "git_commit": _git_commit(),
        "sources": sources,
        "rows": {name: len(rows) for name, rows in tables.items()},
        "issues": dict(sorted(Counter(f"{i.severity}:{i.code}" for i in issues).items())),
    }
    text = json.dumps(info, indent=2, sort_keys=True, default=str) + "\n"
    (out_dir / "build_info.json").write_text(text, encoding="utf-8", newline="\n")
    print(text)
    return 0 if ok else 1
