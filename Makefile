.PHONY: test

include .env

test:
	poetry run pytest -s