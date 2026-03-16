.PHONY: install run test lint migrate

install:
	poetry install

run:
	uvicorn src.main:app --reload

test:
	pytest

lint:
	black src tests
	isort src tests
	flake8 src tests
	mypy src

migrate:
	alembic upgrade head

makemigrations:
	alembic revision --autogenerate -m "$(message)"