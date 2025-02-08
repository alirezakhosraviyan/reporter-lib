help:
	@echo 'Available commands:'
	@echo '  make install  - Installs dependencies'
	@echo '  make test     - Runs the tests'
	@echo '  make lint     - Runs the linters and formatter'
	@echo '  make check    - Runs all checks'

install:
	poetry install

test:
	poetry run pytest --cov-report term-missing

lint:
	poetry run ruff format .
	poetry run ruff check . --fix
	poetry run mypy .

check: lint
	poetry run pytest
	poetry run bandit .
