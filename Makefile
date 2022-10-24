POETRY ?= poetry
PACKAGES = pydra

all: clean install check test

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

.PHONY: check-lock
check-lock:
	@$(POETRY) lock --check

.PHONY: clean
clean: clean-docs clean-test
	@$(RM) $(INSTALL_STAMP)

.PHONY: clean-docs
clean-docs:
	@$(RM) -r docs/_build

.PHONY: clean-py
clean-py:
	@find . -name __pycache__ -exec $(RM) -r {} +

.PHONY: clean-test
clean-test: clean-py
	@$(RM) -r .pytest_cache

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
install: check-lock
	@$(POETRY) install

.PHONY: lock
lock:
	@$(POETRY) lock --no-update

.PHONY: test
test: clean-test
	@$(POETRY) run pytest

.PHONY: update
update:
	@$(POETRY) update
