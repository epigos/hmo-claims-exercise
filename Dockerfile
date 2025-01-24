FROM python:3.12-slim-bullseye

RUN mkdir /code
WORKDIR /code

# install poetry package manager
RUN pip install -U pip poetry
# install project dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-root
RUN rm -rf ~/.cache/pypoetry/{cache,artifacts}

COPY .. ./

EXPOSE 5000

ENV PYTHONWARNINGS="ignore"

CMD ["flask", "run", "-h", "0.0.0.0"]
