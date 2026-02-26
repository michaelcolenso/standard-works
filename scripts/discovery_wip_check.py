#!/usr/bin/env python3
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
ROT = ROOT / "intake" / "rotation"

EXPECTED = {"SLOT-1", "SLOT-2", "SLOT-3"}

def main():
    if not ROT.exists():
        print("No intake/rotation directory found.")
        return 1

    slots = {p.name for p in ROT.iterdir() if p.is_dir() and p.name.startswith("SLOT-")}
    extra = sorted(slots - EXPECTED)
    missing = sorted(EXPECTED - slots)

    ok = True
    if extra:
        ok = False
        print("FAIL: Extra discovery slots detected:", ", ".join(extra))
    if missing:
        ok = False
        print("FAIL: Missing required slots:", ", ".join(missing))

    if ok:
        print("DISCOVERY WIP CHECK: OK ✅")
        return 0
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
