SETTINGS = goods_delivery.settings
env = dev 

# -- helpers

.PHONY: help requirements
help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

clean: ## Remove compiled files and cached folders
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf

# -- database

migrate:  ## Run migrate
	@python manage.py migrate

createsuperuser:  ## Create superuser for project
	@python manage.py createsuperuser

# -- installation

requirements:  ## Install requirements for run project on development env
	@pip install -r requirements/dev.txt

install: .env requirements migrate ## Install local project

# -- execution

run: clean .env  ## Run development server
	@python manage.py runserver

.env: SHELL:=/bin/bash
.env: required-env
	@if [ $(env) == "dev" -a ! -e .env ]; then cp contrib/localenv .env; fi
	@if [ $(env) == "test" -a ! -e .env ]; then cp contrib/testenv .env; fi

required-env: SHELL:=/bin/bash
required-env:
	@if [ -z $(env) ]; then echo "env paramether is not set"; exit 1; fi
	@if [ $(env) != "prod" -a $(env) != "dev" -a $(env) != "test" ]; then echo "env paramether is not a valid value: dev, prod or test"; e    xit 1; fi

# -- test

test:  ## Run simple test
	py.test goods_delivery --ds=$(SETTINGS) --pdb

test-travis: clean check check-debugger ## Test on travis CI
	@py.test -n 2 goods_delivery --ds=$(SETTINGS)
	@py.test --cov-config .coveragerc --cov goods_delivery goods_delivery --ds=$(SETTINGS) --cov-report term-missing --cov-fail-under=90

check:  ## Run code static checks
	@flake8 .
	@isort --check

check-debugger: ## Check if has set_trace on files
	@find goods_delivery -type f -exec egrep -iH "set_trace" {} \+ && echo "Ooops! Found 1 set_trace on your source code!" && exit 1 ||     exit 0

coverage: clean ## Basic test with coverage
	@py.test --cov-config .coveragerc --cov goods_delivery goods_delivery --ds=$(SETTINGS) --cov-report term-missing --cov-fail-under=90

