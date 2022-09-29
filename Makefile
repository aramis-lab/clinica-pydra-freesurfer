POETRY ?= poetry
PACKAGES = pydra
INSTALL_STAMP = .install.stamp
INSTALL_DOCS_STAMP = .install-docs.stamp

all:

.PHONY: check
check: check-black check-isort

.PHONY: check-black
check-black: $(INSTALL_STAMP)
	$(info Checking code with black)
	@$(POETRY) run black --check --diff $(PACKAGES)

.PHONY: check-isort
check-isort: $(INSTALL_STAMP)
	$(info Checking code with isort)
	@$(POETRY) run isort --check --diff $(PACKAGES)

.PHONY: clean
clean:
	$(RM) -r dist
	$(RM) $(INSTALL_STAMP)

.PHONY: clean-docs
clean-docs:
	@$(POETRY) run make -C docs clean
	$(RM) $(INSTALL_DOCS_STAMP)

.PHONY: docs
docs: $(INSTALL_DOCS_STAMP)
	@$(POETRY) run make -C docs html

.PHONY: format
format: format-black format-isort

.PHONY: format-black
format-black: $(INSTALL_STAMP)
	$(info Formatting code with black)
	@$(POETRY) run black --quiet $(PACKAGES)

.PHONY: format-isort
format-isort: $(INSTALL_STAMP)
	$(info Formatting code with isort)
	@$(POETRY) run isort --quiet $(PACKAGES)

.PHONY: install
install: $(INSTALL_STAMP)
$(INSTALL_STAMP): poetry.lock pyproject.toml
	@$(POETRY) install
	@touch $(INSTALL_STAMP)

.PHONY: install-docs
install-docs: $(INSTALL_DOCS_STAMP)
$(INSTALL_DOCS_STAMP): poetry.lock pyproject.toml
	@$(POETRY) install --only docs
	@touch $(INSTALL_DOCS_STAMP)

.PHONY: test
test: $(INSTALL_STAMP)
	@$(POETRY) run python -m pytest

.PHONY: update
update: pyproject.toml
	@$(POETRY) update
