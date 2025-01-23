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
	poetry run flask upgrade

downgrade:
	poetry run flask downgrade

start:
	poetry run flask run

#: run tests
tests:
	poetry run pytest -s tests/ -vvv --cov --cov-report term-missing

#: list available make targets
help:
	@grep -B1 -E "^[a-zA-Z0-9_-]+\:([^\=]|$$)" Makefile \
		| grep -v -- -- \
		| sed 'N;s/\n/###/' \
		| sed -n 's/^#: \(.*\)###\(.*\):.*/make \2###    \1/p' \
		| column -t  -s '###' \
		| sort

.PHONY: lint format tests upgrade downgrade start help
