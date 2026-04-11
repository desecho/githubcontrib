.SILENT:
.DEFAULT_GOAL := help

include makefiles/colors.mk
include makefiles/help.mk
include makefiles/deps.mk

export PROJECT := githubcontrib
export APP := $(PROJECT)
export BUCKET := scrap-db-backups
export DOCKER_SECRETS_ENV_FILE := docker_secrets.env

ENV_FILE         := env.sh
ENV_CUSTOM_FILE  := env_custom.sh
ENV_SECRETS_FILE := env_secrets.sh
DB_ENV_PROD_FILE := db_env_prod.sh

SHELL := /bin/bash
VENV_DIR := .venv
SOURCE_CMDS := source $(VENV_DIR)/bin/activate && source $(ENV_FILE) && source $(ENV_CUSTOM_FILE) && source $(ENV_SECRETS_FILE)
CMD_FRONTEND := cd frontend && source $(ENV_FILE)
PYTHON_VERSION := 3.12
PYTHON := python$(PYTHON_VERSION)

#------------------------------------
# Installation
#------------------------------------
.PHONY: install-linters-binaries
## Install linters binaries | Installation
install-linters-binaries: .install-hadolint .install-actionlint .install-shellcheck

.PHONY: install-deps
## Install dependencies
install-deps: install-linters-binaries
	sudo apt install $(PYTHON) $(PYTHON)-venv $(PYTHON)-dev -y
	sudo apt install libmysqlclient-dev -y
	pip3 install uv tox

.PHONY: create-venv
## Create venv and sync dependencies
create-venv:
	uv venv --python $(PYTHON_VERSION) --allow-existing
	uv sync

.PHONY: create-tox-venv
## Create tox venv and sync dependencies
create-tox-venv:
	tox -e py-requirements

.PHONY: create-venvs
## Create venv and tox venv and sync dependencies
create-venvs: create-venv create-tox-venv

.PHONY: yarn-install-locked
## Run frontend yarn install using lockfile
yarn-install-locked:
	$(CMD_FRONTEND) && yarn install --immutable

.PHONY: yarn-install
## Run frontend yarn install
yarn-install:
	$(CMD_FRONTEND) && yarn install

.PHONY: create-db
## Create db
create-db:
	source $(ENV_FILE) && scripts/create_db.sh

.PHONY: bootstrap
## Bootstrap project
bootstrap: yarn-install-locked create-env-files create-venvs create-db migrate build

.PHONY: create-env-files
## Create env files
create-env-files: $(ENV_CUSTOM_FILE) $(ENV_SECRETS_FILE) $(DB_ENV_PROD_FILE) $(DOCKER_SECRETS_ENV_FILE)

$(DOCKER_SECRETS_ENV_FILE):
	cp $(DOCKER_SECRETS_ENV_FILE).tpl $(DOCKER_SECRETS_ENV_FILE)

$(ENV_CUSTOM_FILE):
	cp $(ENV_CUSTOM_FILE).tpl $(ENV_CUSTOM_FILE)

$(ENV_SECRETS_FILE):
	cp $(ENV_SECRETS_FILE).tpl $(ENV_SECRETS_FILE)

$(DB_ENV_PROD_FILE):
	cp $(DB_ENV_PROD_FILE).tpl $(DB_ENV_PROD_FILE)

#------------------------------------
# Docker commands
#------------------------------------
export DOCKER_ENV_FILE := docker.env

.PHONY: docker-build-dev
## Build docker images | Docker
docker-build-dev: docker-build-backend docker-build-frontend-dev

.PHONY: docker-build-backend
## Build docker backend image
docker-build-backend:
	$(call print,Building Docker backend image)
	@docker build -t "${PROJECT}:backend" .

.PHONY: docker-build-frontend-dev
## Build docker frontend image
docker-build-frontend-dev:
	$(call print,Building Docker frontend image)
	docker build --build-arg VITE_BACKEND_URL="http://localhost:8000/" -t "${PROJECT}:frontend" ./frontend

.PHONY: docker-run
## Run server in docker
docker-run: collectstatic
	$(call print,Running server in docker)
	@docker-compose up

.PHONY: docker-sh
## Run docker shell
docker-sh:
	$(call print,Running docker shell)
	@docker run -ti --env-file ${DOCKER_ENV_FILE} --env-file $(DOCKER_SECRETS_ENV_FILE) ${PROJECT}:backend sh
#------------------------------------

#------------------------------------
# Scripts
#------------------------------------
.PHONY: backup-db
backup-db:
	scripts/backup_db.sh

.PHONY: flush-cdn-cache
flush-cdn-cache:
	scripts/flush_cdn_cache.sh

#------------------------------------
# Tests
#------------------------------------
.PHONY: test
## Run tests | Tests
test: shellcheck hadolint actionlint tox eslint prettier-json-lint prettier-scss-lint prettier-yaml-lint \
	prettier-ts-lint prettier-vue-lint test-frontend ts-lint

.PHONY: test-python
## Run Python tests
test-python: ruff mypy pytest

.PHONY: tox
## Run tox
tox:
	tox

.PHONY: rstlint
## Run rstlint linter
rstlint:
	tox -e py-rstlint

.PHONY: safety
## Run safety linter
safety:
	tox -e py-safety

.PHONY: pytest
## Run pytest
pytest:
	tox -e py-pytest

.PHONY: ruff
## Run ruff linter
ruff:
	tox -e py-ruff

.PHONY: mypy
## Run mypy linter
mypy:
	tox -e py-mypy

.PHONY: test-frontend
## Run frontend tests
test-frontend:
	$(CMD_FRONTEND) && yarn run test:run

.PHONY: eslint
## Run frontend eslint
eslint:
	$(CMD_FRONTEND) && yarn run eslint src/**/*.ts src/*.ts ./*.ts src/App.vue src/components/*.vue src/views/*.vue

.PHONY: ts-lint
## Run frontend TypeScript linter
ts-lint:
	$(CMD_FRONTEND) && npx vue-tsc --noEmit

.PHONY: shellcheck
## Run shellcheck linter
shellcheck:
	shellcheck scripts/*.sh ./*.sh frontend/*.sh

.PHONY: hadolint
## Run hadolint linter
hadolint:
	hadolint Dockerfile frontend/Dockerfile

.PHONY: actionlint
## Run actionlint linter
actionlint:
	actionlint

.PHONY: prettier-ts-lint
## Run prettier check for ts
prettier-ts-lint:
	$(CMD_FRONTEND) && yarn run prettier --check "src/**/*.ts" "src/*.ts" "./*.ts"

.PHONY: prettier-scss-lint
## Run prettier check for scss
prettier-scss-lint:
	$(CMD_FRONTEND) && yarn run prettier --check "./src/styles/*.scss"

.PHONY: prettier-json-lint
## Run prettier check for json
prettier-json-lint:
	$(CMD_FRONTEND) && yarn run prettier --check "../*.json" "./**/*.json"

.PHONY: prettier-yaml-lint
## Run prettier check for yaml
prettier-yaml-lint:
	$(CMD_FRONTEND) && yarn run prettier --check "../deployment/*.yaml" "../.github/**/*.yaml"

.PHONY: prettier-vue-lint
## Run prettier check for vue
prettier-vue-lint:
	$(CMD_FRONTEND) && yarn run prettier --check "src/App.vue" "src/components/*.vue" "src/views/*.vue"

#------------------------------------
# Development
#------------------------------------
.PHONY: update-venvs
## Sync packages in venv and tox venv | Development
update-venvs:
	uv sync
	tox -e py-requirements

.PHONY: delete-venvs
delete-venvs:
	rm -rf $(VENV_DIR)
	rm -rf .tox

.PHONY: recreate-venvs
## Recreate venvs
recreate-venvs: delete-venvs create-venvs

.PHONY: yarn-build
## Run frontend build
yarn-build:
	$(CMD_FRONTEND) && yarn build

.PHONY: build
## Run frontend build
build: yarn-build

.PHONY: dev
## Run frontend development server
dev:
	$(CMD_FRONTEND) && yarn dev

.PHONY: yarn-build-prod
## Run frontend production build
yarn-build-prod: yarn-build

.PHONY: drop-db
## Drop db
drop-db:
	source $(ENV_FILE) && scripts/drop_db.sh

.PHONY: load-db
## Load db from today's backup
load-db: drop-db create-db
	source $(ENV_FILE) && ./scripts/load_db.sh

.PHONY: uv-update
## Update python packages
uv-update:
	uv lock --upgrade

.PHONY: uv-show-outdated
## Show outdated python packages
uv-show-outdated:
	uv pip list --outdated

#------------------------------------
# Formatting
#------------------------------------
.PHONY: format
## Format Python code | Formatting
format:
	$(SOURCE_CMDS) && ruff format src

.PHONY: format-json
## Format json files
format-json:
	$(CMD_FRONTEND) && yarn run prettier --write "../*.json" "./**/*.json"

.PHONY: format-scss
## Format scss files
format-scss:
	$(CMD_FRONTEND) && yarn run prettier --write "./src/**/*.scss"

.PHONY: format-ts
## Format ts files
format-ts:
	$(CMD_FRONTEND) && yarn run prettier --write "src/**/*.ts" "src/*.ts" "./*.ts"

.PHONY: format-vue
## Format vue files
format-vue:
	$(CMD_FRONTEND) && yarn run prettier --write "src/App.vue" "src/components/*.vue" "src/views/*.vue"

.PHONY: format-yaml
## Format yaml files
format-yaml:
	$(CMD_FRONTEND) && yarn run prettier --write "../deployment/*.yaml" "../.github/**/*.yaml"

.PHONY: format-all
## Format code
format-all: format format-ts format-vue format-scss format-sh format-json format-yaml

#------------------------------------
# Django management commands
#------------------------------------
MANAGE_CMD := src/manage.py

.PHONY: runserver
## Run backend server for development
runserver:
	$(SOURCE_CMDS) && $(MANAGE_CMD) runserver 0.0.0.0:8000

.PHONY: run
## Run backend server for development
run: runserver

.PHONY: migrate
## Run data migration
migrate:
	$(SOURCE_CMDS) && $(MANAGE_CMD) migrate

.PHONY: collectstatic
## Collect backend static files
collectstatic:
	$(SOURCE_CMDS) && export IS_DEV= && $(MANAGE_CMD) collectstatic --no-input

.PHONY: createsuperuser
## Create super user
createsuperuser:
	$(SOURCE_CMDS) && $(MANAGE_CMD) createsuperuser

.PHONY: shell
## Run shell
shell:
	$(SOURCE_CMDS) && $(MANAGE_CMD) shell

.PHONY: manage
## Run management command. `make manage command_name arguments="arg1 arg2"`
manage:
	$(SOURCE_CMDS) && $(MANAGE_CMD) $(command_name) $(arguments)
