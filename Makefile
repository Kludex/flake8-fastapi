.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: install
install:  ## Install package.
	@echo "🏗️ Installing package"
	pip install --upgrade pip
	pip install --upgrade poetry
	poetry install


.PHONY: lint
lint:  ## Linter the code.
	@echo "🚨 Linting code"
	poetry run isort flake8_fastapi tests --check
	poetry run flake8 flake8_fastapi tests
	poetry run mypy flake8_fastapi
	poetry run black flake8_fastapi tests --check --diff


.PHONY: format
format:
	@echo "🎨 Formatting code"
	poetry run isort flake8_fastapi tests
	poetry run autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place flake8_fastapi tests --exclude=__init__.py
	poetry run black flake8_fastapi tests


.PHONY: test
test:  ## Test your code.
	@echo "🍜 Running pytest"
	poetry run pytest tests/ --cov=flake8_fastapi --cov-report=term-missing:skip-covered --cov-report=xml --cov-fail-under 100
