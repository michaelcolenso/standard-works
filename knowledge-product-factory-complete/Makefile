PRODUCT ?= products/EXAMPLE_living_product

all: core quickstart assets updates

core:
	python build/scripts/assemble_core.py $(PRODUCT)
	bash build/scripts/compile_pdf.sh core $(PRODUCT)

quickstart:
	bash build/scripts/compile_pdf.sh quickstart $(PRODUCT)

assets:
	python build/scripts/assemble_assets.py $(PRODUCT)
	bash build/scripts/compile_pdf.sh assets $(PRODUCT)

updates:
	bash build/scripts/compile_pdf.sh updates $(PRODUCT)

check:
	python scripts/status_check.py $(PRODUCT)
	python scripts/quality_gate.py $(PRODUCT)
