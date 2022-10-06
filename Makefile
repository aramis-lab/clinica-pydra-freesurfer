POETRY ?= poetry
PACKAGES = pydra
INSTALL_STAMP = .install.stamp

all: clean install check test

.PHONY: check
check: check-black check-isort

.PHONY: check-black
check-black: install
	$(info Checking code with black)
	@$(POETRY) run black --check --diff $(PACKAGES)

.PHONY: check-isort
check-isort: install
	$(info Checking code with isort)
	@$(POETRY) run isort --check --diff $(PACKAGES)

.PHONY: clean
clean:
	@$(RM) $(INSTALL_STAMP)

.PHONY: clean-docs
clean-docs:
	@$(RM) -r docs/_build

.PHONY: clean-test
clean-test:
	@$(RM) -r .pytest_cache

.PHONY: docs
docs: clean-docs install
	@$(POETRY) run make -C docs html

.PHONY: format
format: format-black format-isort

.PHONY: format-black
format-black: install
	$(info Formatting code with black)
	@$(POETRY) run black --quiet $(PACKAGES)

.PHONY: format-isort
format-isort: install
	$(info Formatting code with isort)
	@$(POETRY) run isort --quiet $(PACKAGES)

.PHONY: install
install: $(INSTALL_STAMP)
$(INSTALL_STAMP):
	@$(POETRY) install
	@touch $(INSTALL_STAMP)

.PHONY: test
test: clean-test install
	@$(POETRY) run pytest

.PHONY: update
update:
	@$(POETRY) update
