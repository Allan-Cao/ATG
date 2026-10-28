.PHONY: docs docs-build

docs:
	uv run sphinx-autobuild docs docs/_build/html

docs-build:
	uv run sphinx-build docs docs/_build/html --fail-on-warning