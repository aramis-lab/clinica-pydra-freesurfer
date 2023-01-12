POETRY ?= poetry
PACKAGES = pydra

all: clean install check test

.PHONY: check
check: check-black check-isort check-codespell

.PHONY: check-black
check-black:
	$(info Checking code with black)
	@$(POETRY) run black --check --diff $(PACKAGES)

.PHONY: check-codespell
check-codespell:
	$(info Checking code with codespell)
	@$(POETRY) run codespell

.PHONY: check-isort
check-isort:
	$(info Checking code with isort)
	@$(POETRY) run isort --check --diff $(PACKAGES)

.PHONY: check-lock
check-lock:
	@$(POETRY) lock --check

.PHONY: clean
clean: clean-dist clean-docs clean-py clean-test

.PHONY: clean-dist
clean-dist:
	@$(RM) -r dist/

.PHONY: clean-docs
clean-docs:
	@$(RM) -r docs/_build/

.PHONY: clean-py
clean-py:
	@find . -name __pycache__ -exec $(RM) -r {} +

.PHONY: clean-test
clean-test:
	@$(RM) -r .pytest_cache/

.PHONY: config-pypi
config-pypi:
ifdef PYPI_TOKEN
	@$(POETRY) config pypi-token.pypi "${PYPI_TOKEN}"
else
	$(error "Missing API token for PyPI repository")
endif

.PHONY: docs
docs:
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

.PHONY: publish
publish: publish-pypi

.PHONY: publish-pypi
publish-pypi: config-pypi
	@$(POETRY) publish --build

.PHONY: serve-docs
serve-docs:
	@$(POETRY) run make -C docs livehtml

.PHONY: test
test:
	@$(POETRY) run pytest

.PHONY: update
update:
	@$(POETRY) update
