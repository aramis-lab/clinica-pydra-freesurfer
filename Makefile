POETRY ?= poetry
PACKAGES = pydra

.PHONY: install
install:
	@$(POETRY) install

.PHONY: format-black
format-black: install
	$(info Formatting code with black)
	@$(POETRY) run black --quiet $(PACKAGES)

.PHONY: format-isort
format-isort: install
	$(info Formatting code with isort)
	@$(POETRY) run isort --quiet $(PACKAGES)

.PHONY: format
format: format-black format-isort

.PHONY: lint-black
lint-black: install
	$(info Linting code with black)
	@$(POETRY) run black --check --diff $(PACKAGES)

.PHONY: lint-isort
lint-isort: install
	$(info Linting code with isort)
	@$(POETRY) run isort --check --diff $(PACKAGES)

.PHONY: lint
lint: lint-black lint-isort

.PHONY: clean-docs
clean-docs: docs/_build
	@$(MAKE) -C docs clean

.PHONY: install-docs
install-docs:
	@$(POETRY) install -E docs

.PHONY: docs
docs: install-docs clean-docs
	@$(POETRY) run make -C docs html
