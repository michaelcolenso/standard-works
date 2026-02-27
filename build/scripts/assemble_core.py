#!/usr/bin/env python3
import sys, pathlib

def collect(product_dir: pathlib.Path):
    core = sorted([p for p in (product_dir/"03-drafts/core").rglob("*.md") if p.is_file()])
    evg  = sorted([p for p in (product_dir/"03-drafts/evergreen").rglob("*.md") if p.is_file()])
    return core, evg

def concat(out_path: pathlib.Path, files, title):
    parts=[f"% {title}\n"]
    for p in files:
        txt=p.read_text(encoding="utf-8", errors="ignore").strip()
        parts.append(f"\n\n<!-- SOURCE: {p.as_posix()} -->\n\n")
        parts.append(txt)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(parts).strip()+"\n", encoding="utf-8")

def main():
    if len(sys.argv)<2:
        print("Usage: python build/scripts/assemble_core.py <product_dir>")
        return 2
    product_dir=pathlib.Path(sys.argv[1]).resolve()
    name=product_dir.name
    core, evg = collect(product_dir)
    if not core and not evg:
        print("No drafts found.")
        return 1
    build_dir=product_dir/"_build"
    build_dir.mkdir(exist_ok=True)
    out=build_dir/"core_guide.md"
    concat(out, core+evg, f"{name} — Core Guide")
    print(f"Assembled: {out}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
