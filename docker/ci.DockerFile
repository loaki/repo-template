ARG PYTHON_VERSION

FROM python:${PYTHON_VERSION}

WORKDIR /project/

RUN pip install poetry

COPY pyproject.toml .
COPY poetry.toml .
COPY poetry.lock .

RUN poetry install

COPY docker/run_tests.sh run_tests.sh
COPY project project
COPY tests tests
