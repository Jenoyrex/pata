"""Build the Pata reference gazetteer from pinned source snapshots (see docs/gazetteer.md)."""

import argparse
import sys
from pathlib import Path

from pata import gazetteer

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifests", type=Path, default=ROOT / "data" / "manifests")
    p.add_argument("--raw", type=Path, default=ROOT / "data" / "raw")
    p.add_argument("--out", type=Path, default=ROOT / "data" / "processed" / "gazetteer")
    p.add_argument(
        "--snapshot-info",
        action="store_true",
        help="print checksums, row counts and headers of raw files for pinning, then exit",
    )
    args = p.parse_args()
    try:
        if args.snapshot_info:
            print(gazetteer.snapshot_info(args.manifests, args.raw))
            return 0
        return gazetteer.run(args.manifests, args.raw, args.out)
    except gazetteer.BuildError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
