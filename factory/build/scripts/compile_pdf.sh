#!/usr/bin/env bash
set -euo pipefail

KIND="${1:-}"
PRODUCT_DIR="${2:-}"

if [[ -z "$KIND" || -z "$PRODUCT_DIR" ]]; then
  echo "Usage: bash build/scripts/compile_pdf.sh <core|quickstart|assets|updates> <product_dir>"
  exit 1
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DIST="$ROOT/dist"
mkdir -p "$DIST"

NAME="$(basename "$PRODUCT_DIR")"
BUILD_DIR="$PRODUCT_DIR/_build"
mkdir -p "$BUILD_DIR"

case "$KIND" in
  core)
    IN_MD="$BUILD_DIR/core_guide.md"
    TEMPLATE="$ROOT/build/templates/core_guide.tex"
    OUT_PDF="$DIST/${NAME}_Core_Guide.pdf"
    TITLE="${NAME} — Core Guide"
    ;;
  quickstart)
    IN_MD="$PRODUCT_DIR/06-packaging/quick_start.md"
    TEMPLATE="$ROOT/build/templates/quick_start.tex"
    OUT_PDF="$DIST/${NAME}_Quick_Start.pdf"
    TITLE="${NAME} — Quick Start"
    ;;
  assets)
    IN_MD="$BUILD_DIR/asset_pack.md"
    TEMPLATE="$ROOT/build/templates/asset_pack.tex"
    OUT_PDF="$DIST/${NAME}_Asset_Pack.pdf"
    TITLE="${NAME} — Asset Pack"
    ;;
  updates)
    DIGEST_DIR="$PRODUCT_DIR/updates/digests"
    if ls "$DIGEST_DIR"/*.md >/dev/null 2>&1; then
      IN_MD="$(ls -t "$DIGEST_DIR"/*.md | head -n 1)"
    else
      IN_MD="$PRODUCT_DIR/updates/changelog.md"
    fi
    TEMPLATE="$ROOT/build/templates/update_digest.tex"
    OUT_PDF="$DIST/${NAME}_Update_Digest.pdf"
    TITLE="${NAME} — Update Digest"
    ;;
  *)
    echo "Unknown kind: $KIND"
    exit 2
    ;;
esac

if [[ ! -f "$IN_MD" ]]; then
  echo "Missing input markdown: $IN_MD"
  exit 1
fi

pandoc "$IN_MD"   --from markdown   --pdf-engine=xelatex   --template="$TEMPLATE"   -V title="$TITLE"   --toc   -o "$OUT_PDF"

echo "Built: $OUT_PDF"
