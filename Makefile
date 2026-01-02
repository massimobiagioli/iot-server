.PHONY: default help up down status logs sync console start-dev create-migration migrate test test-cov lint lint-fix format create-admin
default: help ;

DOCKER_COMPOSE = docker compose
UV = uv
PYTHON = uv run python
FASTAPI = uv run fastapi
ALEMBIC = uv run alembic
PYTEST = uv run pytest
RUFF = uv run ruff

help:             ## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

up:               ## Start docker containers in detached mode
	$(DOCKER_COMPOSE) up -d

down:             ## Stop and remove docker containers
	$(DOCKER_COMPOSE) down

logs:             ## Show docker containers logs
	$(DOCKER_COMPOSE) logs -f

status:           ## Show docker containers status
	$(DOCKER_COMPOSE) ps

sync:             ## Synchronize Python environment with uv
	$(UV) sync

start-dev:        ## Start development environment
	$(FASTAPI) run app/main.py

console:          ## Start an IPython shell con shell_context.py
	PYTHONPATH=. $(UV) run ipython --no-autoindent --no-banner -i shell_context.py

create-migration: ## Create migration
	$(ALEMBIC) revision --autogenerate -m "$(message)"

migrate:          ## Run migration
	$(ALEMBIC) upgrade head

test:             ## Run tests
	PYTHONPATH=. $(PYTEST)

test-cov:         ## Run tests with coverage
	PYTHONPATH=. $(PYTEST) --cov-report term-missing --cov=app

lint:             ## Run ruff linter
	$(RUFF) check app tests

lint-fix:         ## Run ruff linter with autofix
	$(RUFF) check app tests --fix

format:           ## Format code with ruff
	$(RUFF) format app tests

create-admin:     ## Create an admin user
	PYTHONPATH=. $(PYTHON) utils/create_admin_user.py