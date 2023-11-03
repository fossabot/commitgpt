.PHONY: lint
lint:
	ruff check commitgpt

.PHONY: test
test:
	poetry run pytest -v

.PHONY: install-precommit
install-precommit:
	pre-commit install

.PHONY: precommit
precommit:
	pre-commit run --all-files -v

.PHONY: update-precommit
update-precommit:
	pre-commit autoupdate

release:
	standard-version
	git push --follow-tags origin main
