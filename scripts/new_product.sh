#!/usr/bin/env bash
set -euo pipefail

NAME="${1:-}"
if [[ -z "$NAME" ]]; then
  echo "Usage: bash scripts/new_product.sh <product-name>"
  exit 1
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/product-template"
DST="$ROOT/products/$NAME"

if [[ -e "$DST" ]]; then
  echo "Error: $DST already exists."
  exit 1
fi

cp -R "$SRC" "$DST"

# Replace placeholder tokens
find "$DST" -type f -name "*.md" -print0 | while IFS= read -r -d '' f; do
  sed -i.bak "s/<PRODUCT_NAME>/$NAME/g" "$f" && rm -f "$f.bak"
done

echo "Created product: $DST"
echo "Next: python scripts/status_check.py $DST"
