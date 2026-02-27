#!/usr/bin/env python3
import sys, pathlib
from datetime import datetime

CLASSES = ["Cosmetic","Tactical","Structural","Invalidating"]

def classify(text: str) -> str:
    t=text.lower()
    if any(k in t for k in ["repealed","illegal","invalidates","breaks","ban","enforcement","no longer valid"]):
        return "Invalidating"
    if any(k in t for k in ["new law","regulation","deadline","requirement","policy update","procedure change","pricing change"]):
        return "Tactical"
    if any(k in t for k in ["framework change","decision logic","core logic","model change"]):
        return "Structural"
    return "Cosmetic"

def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/update_classifier.py <product_dir> <signal_file>")
        return 2
    product_dir=pathlib.Path(sys.argv[1]).resolve()
    signal_path=pathlib.Path(sys.argv[2]).resolve()
    if not signal_path.exists():
        print(f"Signal file not found: {signal_path}")
        return 2
    c=classify(signal_path.read_text(encoding="utf-8", errors="ignore"))
    log_path=product_dir/"updates"/"update_log.md"
    if not log_path.exists():
        print("update_log.md missing.")
        return 1
    date=datetime.now().strftime("%Y-%m-%d")
    table=log_path.read_text(encoding="utf-8", errors="ignore").strip()+"
"
    if "| Date | Signal | Classification | Action |" not in table:
        table += "
| Date | Signal | Classification | Action |
|---|---|---|---|
"
    line=f"| {date} | {signal_path.name} | {c} | Review → {'Patch' if c in ['Cosmetic','Tactical'] else 'Escalate'} |
"
    if line not in table:
        table += line
        log_path.write_text(table, encoding="utf-8")
    print(f"CLASSIFICATION: {c} ✅")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
