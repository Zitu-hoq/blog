FROM python:3.9

WORKDIR /app
COPY . /app

RUN pip install poetry
RUN poetry install

CMD ["poetry", "run", "gunicorn", "main:app"]