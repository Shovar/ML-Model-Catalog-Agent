.PHONY: install dev run seed clean lint test

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

seed:
	python -c "from catalogue.seed import seed; seed()"

clean:
	rm -f catalogue.db
	rm -rf __pycache__ app/__pycache__ catalogue/__pycache__

test:
	python -m pytest tests/ -v

lint:
	ruff check . --fix
