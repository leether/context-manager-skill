.PHONY: help install test lint format clean upload docs

help:
	@echo "Context Manager - 可用命令:"
	@echo ""
	@echo "  make install    - 安装项目及开发依赖"
	@echo "  make test       - 运行测试"
	@echo "  make lint       - 运行代码检查"
	@echo "  make format     - 格式化代码"
	@echo "  make clean      - 清理临时文件"
	@echo "  make upload     - 发布到 PyPI"
	@echo "  make docs       - 生成文档"

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=scripts --cov-report=html --cov-report=term

test-quick:
	pytest tests/ -v

lint:
	ruff check scripts/ tests/
	black --check scripts/ tests/
	isort --check-only scripts/ tests/
	mypy scripts/

format:
	black scripts/ tests/
	isort scripts/ tests/
	ruff check --fix scripts/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -rf build/
	rm -rf dist/

upload:
	python -m build
	twine check dist/*
	twine upload dist/*

docs:
	@echo "文档已包含在 SKILL.md 和 README.md 中"
