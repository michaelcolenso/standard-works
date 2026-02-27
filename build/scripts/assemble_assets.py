#!/usr/bin/env python3
import sys, pathlib

def collect(product_dir: pathlib.Path):
    assets = []
    for sub in ["checklists","templates","worksheets","diagrams","verification"]:
        d = product_dir/"05-assets"/sub
        if d.exists():
            assets += sorted([p for p in d.rglob("*.md") if p.is_file() and p.name.lower()!="readme.md"])
    return assets

def concat(out_path: pathlib.Path, files, title):
    parts=[f"% {title}\n", "\n## How to use\nPrint these sheets or copy them into your tracker.\n"]
    for p in files:
        txt=p.read_text(encoding="utf-8", errors="ignore").strip()
        parts.append("\n\n\newpage\n\n")
        parts.append(f"<!-- SOURCE: {p.as_posix()} -->\n\n")
        parts.append(txt)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(parts).strip()+"\n", encoding="utf-8")

def main():
    if len(sys.argv)<2:
        print("Usage: python build/scripts/assemble_assets.py <product_dir>")
        return 2
    product_dir=pathlib.Path(sys.argv[1]).resolve()
    name=product_dir.name
    files=collect(product_dir)
    if not files:
        print("No assets found.")
        return 1
    build_dir=product_dir/"_build"
    build_dir.mkdir(exist_ok=True)
    out=build_dir/"asset_pack.md"
    concat(out, files, f"{name} — Asset Pack")
    print(f"Assembled: {out}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
