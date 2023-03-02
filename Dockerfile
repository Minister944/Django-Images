FROM python:3.11-slim-buster

WORKDIR /api

RUN pip install poetry==1.3.2
COPY poetry.lock pyproject.toml /api/
RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi

COPY . /api/
