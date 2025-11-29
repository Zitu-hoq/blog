FROM python:3.9

WORKDIR /app
COPY . /app

COPY README.md /app/README.md

RUN pip install poetry
RUN poetry install

CMD ["poetry", "run", "gunicorn", "main:app"]