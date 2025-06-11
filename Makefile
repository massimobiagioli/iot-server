.PHONY: help install lint lint-fix format test coverage server prisma-generate prisma-db-push

default: help

help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

install: # Install dependencies
	pip install --upgrade pip && \
	pip install -r requirements_dev.txt

lint: # Run linter
	ruff check .

lint-fix: # Run linter with fix
	ruff check --fix .

format: # Run formatter
	ruff format .

test: # Run tests
ifdef filter
	@export $$(cat .env.test | xargs) && STAGE=test pytest $(filter) -vv
else
	@export $$(cat .env.test | xargs) && STAGE=test pytest -vv
endif

coverage: # Run tests with coverage
	@export $$(cat .env.test | xargs) && STAGE=test pytest tests --cov=src --cov-report term-missing

server: # Start local server
ifdef port
	uvicorn src.main:app --host 0.0.0.0 --port $(port) --reload
else
	uvicorn src.main:app --host 0.0.0.0 --reload
endif

prisma-generate: # Generate Prisma client
	prisma generate

prisma-db-push: # Push Prisma schema to the database
ifdef stage
	@echo "Using .env.$(stage) file"
	@export $$(cat .env.$(stage) | xargs) && prisma db push
else
	@echo "Using default .env file"
	@prisma db push
endif