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
PYTHON_VERSION := 3.12
PYTHON := python$(PYTHON_VERSION)

#------------------------------------
# Installation
#------------------------------------

.PHONY: install-linters-binaries
## Install linters binaries | Installation
install-linters-binaries: .install-shfmt .install-hadolint .install-actionlint .install-shellcheck

.PHONY: install-deps
## Install dependencies
install-deps: install-linters-binaries
	# Install Python
	sudo apt install $(PYTHON) $(PYTHON)-venv $(PYTHON)-dev -y
	# Install MySQL dependencies
	sudo apt install libmysqlclient-dev -y
	# Install dependency for makemessages
	sudo apt install gettext -y
	# Install Python tooling
	pip3 install uv tox

.PHONY: create-venv
## Create venv and sync dependencies
create-venv:
	uv venv --python $(PYTHON_VERSION)
	uv sync

.PHONY: create-tox-venv
## Create tox venv and sync dependencies
create-tox-venv:
	tox -e py-requirements

.PHONY: create-venvs
## Create venv and tox venv and sync dependencies
create-venvs: create-venv create-tox-venv

.PHONY: yarn-install-locked
## Run yarn install using lockfile
yarn-install-locked:
	yarn install --frozen-lockfile

.PHONY: create-db
## Create db
create-db:
	source $(ENV_FILE) && \
	scripts/create_db.sh

.PHONY: bootstrap
## Bootstrap project
bootstrap: yarn-install-locked create-env-files create-venvs create-db migrate yarn-build

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

.PHONY: djhtml-script
djhtml-script:
	scripts/djhtml.sh lint

.PHONY: backup-db
backup-db:
	scripts/backup_db.sh

.PHONY: flush-cdn-cache
flush-cdn-cache:
	scripts/flush_cdn_cache.sh
#------------------------------------

#------------------------------------
# Tests
#------------------------------------
.PHONY: test
## Run tests | Tests
test: shellcheck hadolint shfmt actionlint tox eslint prettier-json-lint prettier-scss-lint prettier-yaml-lint

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

.PHONY: eslint
## Run eslint linter
eslint:
	yarn run eslint "./*.js" "src/$(APP)/js/*.js"

.PHONY: shfmt
## Run shfmt linter
shfmt:
	shfmt -l -d .

.PHONY: shellcheck
## Run shellcheck linter
shellcheck:
	shellcheck scripts/*.sh ./*.sh

.PHONY: hadolint
## Run hadolint linter
hadolint:
	hadolint Dockerfile

.PHONY: actionlint
## Run actionlint linter
actionlint:
	actionlint

.PHONY: djhtml-lint
## Run djhtml linter
djhtml-lint:
	tox -e py-djhtml

.PHONY: prettier-html-lint
## Run html linter. This linter is used manually to verify that html is valid. It is not used in CI.
prettier-html-lint:
	yarn run prettier --check ./**/*.html

.PHONY: prettier-scss-lint
## Run scss linter
prettier-scss-lint:
	yarn run prettier --check ./**/*.scss

.PHONY: prettier-json-lint
## Run json linter
prettier-json-lint:
	yarn run prettier --check ./**/*.json

.PHONY: prettier-yaml-lint
## Run yaml linter
prettier-yaml-lint:
	yarn run prettier --check ./deployment/*.yaml ./.github/**/*.yaml
#------------------------------------

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

.PHONY: yarn-install-refresh
## Run yarn install (refresh)
yarn-install-refresh:
	rm yarn.lock
	yarn install

.PHONY: yarn-build
## Run yarn build
yarn-build:
	yarn build

.PHONY: yarn-build-prod
## Run yarn build for prod
yarn-build-prod:
	yarn build-prod

.PHONY: build
## Run yarn build for development
build:
	yarn build --watch

.PHONY: drop-db
## Drop db
drop-db:
	source $(ENV_FILE) \
		&& scripts/drop_db.sh

.PHONY: load-db
## Load db from today's backup
load-db: drop-db create-db
	source $(ENV_FILE) \
		&& ./scripts/load_db.sh

.PHONY: uv-update
## Update python packages
uv-update:
	uv lock --upgrade

.PHONY: uv-show-outdated
## Show outdated python packages
uv-show-outdated:
	uv pip list --outdated
#------------------------------------

#------------------------------------
# Formatting
#------------------------------------
.PHONY: format
## Format python code | Formatting
format:
	$(SOURCE_CMDS) \
		&& ruff format src

.PHONY: format-json
## Format json files
format-json:
	yarn run prettier --write ./**/*.json

.PHONY: format-scss
## Format scss files
format-scss:
	yarn run prettier --write ./src/**/*.scss

.PHONY: format-js
## Format js files
format-js:
	yarn run eslint ./*.js src/$(APP)/js/*.js --fix

.PHONY: format-sh
## Format sh files
format-sh:
	shfmt -l -w .

.PHONY: format-html
## Format html files
format-html:
	scripts/djhtml.sh format

.PHONY: format-yaml
## Format yaml files
format-yaml:
	yarn run prettier --write ./deployment/*.yaml ./.github/**/*.yaml

.PHONY: format-all
## Format code
format-all: format format-html format-js format-scss format-sh format-json format-yaml
#------------------------------------

#------------------------------------
# Django management commands
#------------------------------------
MANAGE_CMD := src/manage.py

.PHONY: makemessages
## Run makemessages | Django
makemessages:
	$(SOURCE_CMDS) \
	&& $(MANAGE_CMD) makemessages -a --ignore=$(VENV_DIR) --ignore=.tox --ignore=static \
	&& $(MANAGE_CMD) makemessages -a -d djangojs --ignore=src/$(APP)/static --ignore=node_modules --ignore=$(VENV_DIR) --ignore=.tox --ignore=static

.PHONY: runserver
## Run server for development
runserver:
	$(SOURCE_CMDS) \
		&& $(MANAGE_CMD) runserver 0.0.0.0:8000

.PHONY: run
## Run server for development
run: runserver

.PHONY: migrate
## Run data migration
migrate:
	$(SOURCE_CMDS) \
		&& $(MANAGE_CMD) migrate

.PHONY: collectstatic
## Collect static files
collectstatic:
	$(SOURCE_CMDS) \
		&& export IS_DEV= \
		&& $(MANAGE_CMD) collectstatic --no-input

.PHONY: createsuperuser
## Create super user
createsuperuser:
	$(SOURCE_CMDS) \
		&& $(MANAGE_CMD) createsuperuser

.PHONY: shell
## Run shell
shell:
	$(SOURCE_CMDS) \
		&& $(MANAGE_CMD) shell

.PHONY: makemigrations
## Run makemigrations command. Usage: make makemigrations arguments="[arguments]"
makemigrations:
	$(SOURCE_CMDS) \
		&& $(MANAGE_CMD) makemigrations $(arguments) $(APP)

ifeq (manage,$(firstword $(MAKECMDGOALS)))
  # Use the rest as arguments
  MANAGE_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # Turn them into do-nothing targets
  $(eval $(MANAGE_ARGS):;@:)
endif

.PHONY: manage
## Run management command. Usage: make manage [command] arguments="[arguments]"
manage:
	$(SOURCE_CMDS) \
		&& $(MANAGE_CMD) ${MANAGE_ARGS} $(arguments)
#------------------------------------

#------------------------------------
# Docker commands
#------------------------------------
export DOCKER_ENV_FILE := docker.env

.PHONY: docker-build
## Build image | Docker
docker-build:
	docker build -t $(PROJECT):backend .

.PHONY: docker-run
## Run server in docker
docker-run: collectstatic
	docker-compose up

.PHONY: docker-sh
## Run docker shell
docker-sh:
	docker run -ti --env-file $(DOCKER_ENV_FILE) --env-file $(DOCKER_SECRETS_ENV_FILE) $(PROJECT):backend sh
#------------------------------------

#------------------------------------
# Production commands
#------------------------------------
.PHONY: prod-create-db
## Create prod db | Production
prod-create-db:
	source $(DB_ENV_PROD_FILE) \
		&& scripts/create_db.sh

.PHONY: prod-drop-db
## Drop prod db
prod-drop-db:
	source $(DB_ENV_PROD_FILE) \
		&& scripts/drop_db.sh

.PHONY: prod-load-db
## Load db to prod from today's backup
prod-load-db: prod-drop-db prod-create-db
	source $(DB_ENV_PROD_FILE) \
		&& ./scripts/load_db.sh

.PHONY: prod-connect-db
## Connect to prod db
prod-connect-db:
	source $(DB_ENV_PROD_FILE) \
		&& scripts/connect_db.sh

ifeq (prod-manage,$(firstword $(MAKECMDGOALS)))
  # Use the rest as arguments
  PROD_MANAGE_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # Turn them into do-nothing targets
  $(eval $(PROD_MANAGE_ARGS):;@:)
endif

.PHONY: prod-manage
## Run management command in prod. Usage: make prod-manage [command] arguments="[arguments]"
prod-manage:
	scripts/run_management_command_prod.sh $(PROD_MANAGE_ARGS) $(arguments)

ifeq (prod-manage-interactive,$(firstword $(MAKECMDGOALS)))
  # Use the rest as arguments
  PROD_MANAGE_INTERACTIVE_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # Turn them into do-nothing targets
  $(eval $(PROD_MANAGE_INTERACTIVE_ARGS):;@:)
endif

.PHONY: prod-manage-interactive
## Run management command in prod (interactive). Usage: make prod-manage [command] arguments="[arguments]"
prod-manage-interactive:
	scripts/run_management_command_interactive_prod.sh $(PROD_MANAGE_INTERACTIVE_ARGS) $(arguments)

.PHONY: prod-shell
## Run shell in prod
prod-shell:
	scripts/run_shell_prod.sh

.PHONY: prod-migrate
## Run data migration for prod
prod-migrate:
	scripts/run_management_command_prod.sh migrate

.PHONY: prod-enable-debug
## Enable debug in prod. It will be reset with the next deployment
prod-enable-debug:
	yq eval '.data.DEBUG="True"' deployment/configmap.yaml | kubectl apply -f -
	kubectl rollout restart deployment/$(PROJECT)
#------------------------------------
