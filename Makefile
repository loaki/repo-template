LOCAL_ENV ?= .venv
PYTHON_VERSION ?= python3.10

dev-install:
	pip install --upgrade pip
	pip install virtualenv
	test -d ${LOCAL_ENV} || (echo 'create ${LOCAL_ENV}';${PYTHON_VERSION} -m virtualenv ${LOCAL_ENV})
	. ${LOCAL_ENV}/bin/activate ; ${LOCAL_ENV}/bin/${PYTHON_VERSION} -m pip install --upgrade pip
	. ${LOCAL_ENV}/bin/activate ; ${LOCAL_ENV}/bin/${PYTHON_VERSION} -m pip install -r requirements_dev.txt
	. ${LOCAL_ENV}/bin/activate ; ${LOCAL_ENV}/bin/${PYTHON_VERSION} -m pip install -r requirements.txt

lint/isort:
	${LOCAL_ENV}/bin/isort .

lint/flake8:
	${LOCAL_ENV}/bin/flake8 .

lint/black:
	${LOCAL_ENV}/bin/black .

lint/mypy:
	mkdir -p .mypy_cache/
	${LOCAL_ENV}/bin/mypy --install-types --non-interactive .

lint/bandit:
	${LOCAL_ENV}/bin/bandit  -c .bandit  -r .

lint/safety:
	${LOCAL_ENV}/bin/safety check -i 42194 -i 44715 -i 51668 --full-report

lint: lint/mypy lint/black lint/isort lint/flake8 lint/bandit lint/safety lint/licences

test:
	${LOCAL_ENV}/bin/pytest -vvv tests

test-all: lint test

coverage:
	${LOCAL_ENV}/bin/coverage run --source . -m pytest -vvv tests
	${LOCAL_ENV}/bin/coverage report -m
	${LOCAL_ENV}/bin/coverage html
	$(BROWSER) htmlcov/index.html
