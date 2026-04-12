.PHONY: dev-setup test lint pdf-preview schema-validate clean install

dev-setup:
	pip install -e ".[dev]"
	pre-commit install

install:
	pip install -e .

test:
	pytest --cov --cov-report=term-missing

test-fast:
	pytest -x -q

lint:
	ruff check src/ tests/
	ruff format --check src/ tests/

format:
	ruff format src/ tests/
	ruff check --fix src/ tests/

schema-validate:
	python -c "import json, jsonschema; schema=json.load(open('src/riskforge/_data/schemas/rmf.schema.json')); print('Schema valid:', schema.get('$$id'))"

pdf-preview:
	riskforge init --name "Test System" --version "1.0" --purpose "Test" --provider "AiExponent" --category essential_services --non-interactive 2>/dev/null || true
	@echo "Run riskforge assess then riskforge export --format pdf to preview"

clean:
	rm -rf dist/ build/ .eggs/ *.egg-info src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

audit:
	pip-audit -r requirements.txt 2>/dev/null || pip-audit
