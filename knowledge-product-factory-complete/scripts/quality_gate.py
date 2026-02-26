#!/usr/bin/env python3
import sys, pathlib, re

DISALLOWED = [
    r"\bshould consider\b",
    r"\bgenerally\b",
    r"\bit depends\b",
    r"\bmight want to\b",
    r"\btypically\b",
    r"\boften\b",
    r"\bmaybe\b",
]

REQUIRED_HEADERS = ["Outcome:", "Steps:", "Example:", "Verification:"]

def scan_file(p: pathlib.Path):
    txt = p.read_text(encoding="utf-8", errors="ignore")
    issues = []
    for pat in DISALLOWED:
        for m in re.finditer(pat, txt, flags=re.IGNORECASE):
            window = txt[m.start():m.start()+500]
            if pat == r"\bit depends\b" and ("Decision tree" in window or "Decision Tree" in window):
                continue
            issues.append((p, m.start(), m.group(0)))
    return issues

def check_headers(p: pathlib.Path):
    txt = p.read_text(encoding="utf-8", errors="ignore")
    missing = [h for h in REQUIRED_HEADERS if h not in txt]
    return missing

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/quality_gate.py <product_dir>")
        return 2
    root = pathlib.Path(sys.argv[1]).resolve()
    drafts = list((root / "03-drafts").rglob("*.md"))
    if not drafts:
        print("No draft files found under 03-drafts/")
        return 1

    lint_issues=[]
    header_issues=[]
    for p in drafts:
        if p.name == "draft_log.md":
            continue
        lint_issues += scan_file(p)
        miss = check_headers(p)
        if miss:
            header_issues.append((p, miss))

    ok=True
    if lint_issues:
        ok=False
        print("Language lint issues:")
        for p, pos, token in lint_issues[:200]:
            print(f" - {p.relative_to(root)} @ {pos}: '{token}'")
    if header_issues:
        ok=False
        print("Missing required headers (Outcome/Steps/Example/Verification):")
        for p, miss in header_issues:
            print(f" - {p.relative_to(root)} missing: {', '.join(miss)}")

    if ok:
        print("QUALITY GATE: OK ✅")
        return 0
    print("QUALITY GATE: FAIL ❌")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
