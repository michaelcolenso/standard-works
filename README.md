# Standard Works (Complete)

<img width="2816" height="1536" alt="Gemini_Generated_Image_8r38xv8r38xv8r38 2" src="https://github.com/user-attachments/assets/df83ef44-9a91-4841-911e-664af63dbdb1" />


This repository is a **complete works template** for building digital knowledge products end-to-end with:
- long-horizon agentic workflow (externalized state + phase gates)
- adversarial quality review
- minimum asset pack enforcement
- continuous update engine for living products
- CI that blocks merges unless products are shippable
- automated PDF builds (core guide, quick start, asset pack, update digest)

## Quick start
Create a product:
```bash
bash scripts/new_product.sh my-product
```

Run checks:
```bash
python scripts/status_check.py products/my-product
python scripts/quality_gate.py products/my-product
```

Build PDFs (requires `pandoc` + `xelatex`):
```bash
make all PRODUCT=products/my-product
```

Outputs go to `dist/`:
- `<product>_Core_Guide.pdf`
- `<product>_Quick_Start.pdf`
- `<product>_Asset_Pack.pdf`
- `<product>_Update_Digest.pdf` (living products)

## Reusable assets
See `works-assets/` for reusable structures (never reuse thresholds/examples).

## Example product
A fully populated living product is in:
`products/EXAMPLE_living_product/`

## CI
GitHub Actions workflow:
`.github/workflows/works-ci.yml`
