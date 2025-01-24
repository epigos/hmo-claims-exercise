.DEFAULT_GOAL = help

#: run linter
lint: format
	poetry check --lock
	poetry run autoflake --check .
	poetry run isort --check-only .
	poetry run black --check .
	poetry run mypy  --show-error-codes .

#: format all source files
format:
	poetry run autoflake --in-place .
	poetry run isort --atomic .
	poetry run black .

upgrade:
	docker compose run --rm app poetry run flask db upgrade

downgrade:
	docker compose run --rm app poetry run flask db downgrade

#: run tests
tests:
	docker compose run --rm app poetry run pytest -s tests/ -vvv --cov --cov-report term-missing

build:
	docker compose build

start:
	docker compose up --remove-orphans -d --force-recreate

#: list available make targets
help:
	@grep -B1 -E "^[a-zA-Z0-9_-]+\:([^\=]|$$)" Makefile \
		| grep -v -- -- \
		| sed 'N;s/\n/###/' \
		| sed -n 's/^#: \(.*\)###\(.*\):.*/make \2###    \1/p' \
		| column -t  -s '###' \
		| sort

.PHONY: lint format tests upgrade downgrade start help
