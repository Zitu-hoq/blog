FROM python:3.9

WORKDIR /app
COPY . /app

RUN pip install poetry
RUN poetry install --no-root

<<<<<<< HEAD
COPY README.md /app/README.md

CMD ["poetry", "run", "gunicorn", "main:app"]
=======
CMD ["poetry", "run", "gunicorn", "main:app"]
>>>>>>> ce3bb16a104274d62099d39e03ec949498cdcdaf
