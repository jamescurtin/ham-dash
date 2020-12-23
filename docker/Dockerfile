# ------------------------------------------------------------------------------
#                                  PYTHON BASE
# ------------------------------------------------------------------------------
FROM python:3.8.7-slim as python-base
ENV PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=off \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PYSETUP_PATH="/opt/pysetup" \
    PYTHONDONTWRITEBYTECODE=1 \
    VENV_PATH="/opt/pysetup/.venv" \
    PYTHONUNBUFFERED=1
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# ------------------------------------------------------------------------------
#                                  BUILDER BASE
# ------------------------------------------------------------------------------
FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
ENV POETRY_VERSION=1.0.5
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --no-dev

# ------------------------------------------------------------------------------
#                                  DEVELOPMENT
# ------------------------------------------------------------------------------
FROM python-base as development
ENV FASTAPI_ENV=development

COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY ./docker/docker-entrypoint.sh /docker-entrypoint.sh

WORKDIR $PYSETUP_PATH
RUN poetry install

WORKDIR /app
EXPOSE 8000
ENTRYPOINT /docker-entrypoint.sh $0 $@

# ------------------------------------------------------------------------------
#                                   PRODUCTION
# ------------------------------------------------------------------------------
FROM python-base as production
ENV FASTAPI_ENV=production

COPY --from=builder-base $VENV_PATH $VENV_PATH
COPY ./docker/docker-entrypoint.sh /docker-entrypoint.sh
COPY ./docker/gunicorn_conf.py /gunicorn_conf.py

WORKDIR /app
COPY ./app .


ENTRYPOINT /docker-entrypoint.sh $0 $@
CMD [ "gunicorn", "--worker-class uvicorn.workers.UvicornWorker", "--config /gunicorn_conf.py", "app.main:app"]
