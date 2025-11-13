# Makefile for Bank Management System

.PHONY: help install install-dev test test-coverage lint format clean docs run-cli run-example

help:
	@echo "Bank Management System - Available Commands"
	@echo "============================================"
	@echo "make install        - Install package"
	@echo "make install-dev    - Install with development dependencies"
	@echo "make test           - Run tests"
	@echo "make test-coverage  - Run tests with coverage report"
	@echo "make lint           - Run linting checks"
	@echo "make format         - Format code with black and isort"
	@echo "make type-check     - Run type checking with mypy"
	@echo "make clean          - Clean up generated files"
	@echo "make docs           - Generate documentation"
	@echo "make run-cli        - Run the CLI interface"
	@echo "make run-example    - Run basic example"
	@echo "make all-checks     - Run all quality checks"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

test-coverage:
	pytest tests/ -v --cov=bank_management --cov-report=term-missing --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

lint:
	flake8 bank_management tests --max-line-length=100 --exclude=__pycache__
	@echo "Linting complete!"

format:
	black bank_management tests examples
	isort bank_management tests examples
	@echo "Code formatting complete!"

type-check:
	mypy bank_management --ignore-missing-imports
	@echo "Type checking complete!"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -f bank_data.json
	rm -f *_backup_*.json
	@echo "Cleanup complete!"

docs:
	@echo "Documentation available in docs/ directory"
	@echo "- API Reference: docs/API.md"
	@echo "- Usage Guide: docs/USAGE.md"
	@echo "- Contributing: docs/CONTRIBUTING.md"

run-cli:
	python -m bank_management.cli

run-example:
	python examples/basic_usage.py

run-advanced:
	python examples/advanced_usage.py

all-checks: format lint type-check test
	@echo "All quality checks passed!"

# Development workflow
dev-setup: install-dev
	@echo "Development environment ready!"
	@echo "Run 'make test' to verify installation"

# Quick test and format
quick: format test
	@echo "Quick checks complete!"
