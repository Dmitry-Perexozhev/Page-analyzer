FROM python:3.10-slim

WORKDIR /app

RUN pip install poetry

ENV POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml poetry.lock .

RUN poetry install --no-root --only main

COPY . .

EXPOSE 5000

CMD ["poetry", "run", "gunicorn", "-w", "5", "-b", "0.0.0.0:5000", "page_analyzer:app"]

