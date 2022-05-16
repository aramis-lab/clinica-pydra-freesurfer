POETRY ?= poetry

.PHONY: clean-docs
clean-docs: docs/_build
	@$(MAKE) -C docs clean

.PHONY: install-docs
install-docs:
	@$(POETRY) install -E docs

.PHONY: docs
docs: install-docs clean-docs
	@$(POETRY) run make -C docs html
