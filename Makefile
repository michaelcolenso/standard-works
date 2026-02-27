PRODUCT ?= products/EXAMPLE_living_product

.PHONY: intake:seed

intake:seed:
	@echo "=== STANDARD WORKS :: PHASE 0 NICHE DISCOVERY ==="
	@python scripts/run_agent.py knowledge_niche_generator

.PHONY: intake

intake:
	@echo "=== STANDARD WORKS :: INTAKE MODE ==="
	@python scripts/intake_status.py

.PHONY: intake:run

intake:run:
	@python scripts/run_agent.py knowledge_discovery SLOT=$(SLOT)

.PHONY: intake:promote

intake:promote:
	@python scripts/promote_to_slot.py

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
