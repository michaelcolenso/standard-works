PRODUCT ?= products/EXAMPLE_living_product
SLOT ?= SLOT-1

.PHONY: intake intake\:seed intake\:run intake\:promote workflow\:init workflow\:advance all core quickstart assets updates check

intake\:seed:
	@echo "=== STANDARD WORKS :: PHASE 0 NICHE DISCOVERY ==="
	@python3 scripts/run_agent.py knowledge_niche_generator

intake:
	@echo "=== STANDARD WORKS :: INTAKE MODE ==="
	@python3 scripts/intake_status.py

intake\:run:
	@python3 scripts/run_agent.py knowledge_discovery SLOT=$(SLOT)

intake\:promote:
	@python3 scripts/promote_to_slot.py

workflow\:init:
	@python3 scripts/agentic_workflow.py $(PRODUCT)

workflow\:advance:
	@python3 scripts/agentic_workflow.py $(PRODUCT) --advance

all: core quickstart assets updates

core:
	python3 build/scripts/assemble_core.py $(PRODUCT)
	bash build/scripts/compile_pdf.sh core $(PRODUCT)

quickstart:
	bash build/scripts/compile_pdf.sh quickstart $(PRODUCT)

assets:
	python3 build/scripts/assemble_assets.py $(PRODUCT)
	bash build/scripts/compile_pdf.sh assets $(PRODUCT)

updates:
	bash build/scripts/compile_pdf.sh updates $(PRODUCT)

check:
	python3 scripts/status_check.py $(PRODUCT)
	python3 scripts/quality_gate.py $(PRODUCT)
