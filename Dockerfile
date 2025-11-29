FROM python:3.9

WORKDIR /app
COPY . /app

RUN pip install poetry
RUN poetry install

COPY README.md /app/README.md

CMD ["poetry", "run", "gunicorn", "main:app"]