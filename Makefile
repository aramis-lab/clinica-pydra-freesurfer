POETRY ?= poetry
PACKAGES = pydra

.PHONY: check
check: check-black check-isort

.PHONY: check-black
check-black:
	$(info Checking code with black)
	@$(POETRY) run black --check --diff $(PACKAGES)

.PHONY: check-isort
check-isort:
	$(info Checking code with isort)
	@$(POETRY) run isort --check --diff $(PACKAGES)

.PHONY: clean-docs
clean-docs:
	@$(POETRY) run make -C docs clean

.PHONY: docs
docs: clean-docs
	@$(POETRY) run make -C docs html

.PHONY: format
format: format-black format-isort

.PHONY: format-black
format-black:
	$(info Formatting code with black)
	@$(POETRY) run black --quiet $(PACKAGES)

.PHONY: format-isort
format-isort:
	$(info Formatting code with isort)
	@$(POETRY) run isort --quiet $(PACKAGES)

.PHONY: install
install:
	@$(POETRY) install

.PHONY: install-docs
install-docs:
	@$(POETRY) install --extras docs

.PHONY: test
test:
	@$(POETRY) run python -m pytest
