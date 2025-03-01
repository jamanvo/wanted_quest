FROM python:3.13

WORKDIR /app

RUN apt update && apt install -y vim postgresql-client python3-dev

ADD pyproject.toml /app
ADD poetry.lock /app

RUN pip install poetry pip setuptools wheel --upgrade
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-root