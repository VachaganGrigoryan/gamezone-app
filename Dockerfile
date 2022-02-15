### Build and install packages
FROM python:3.10 as python-base

# Install Python dependencies
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.1.12 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base as build-python
# `build-python` stage is used to build deps + create our virtual environment
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        gettext \
        apt-utils \
        # deps for installing poetry  \
        curl \
        # deps for building python deps
        build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

# We copy our Python requirements here to cache them
# and install only runtime deps using poetry
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev  # respects


# 'development' stage installs all dev deps and can be used to develop code.
# For example using docker-compose to mount local volume under /app
FROM python-base as development
ENV FASTAPI_ENV=development

RUN groupadd -r gamezone && useradd -r -g gamezone gamezone

RUN apt-get update \
  && apt-get install -y \
  libcairo2 \
  libgdk-pixbuf2.0-0 \
  liblcms2-2 \
  libopenjp2-7 \
  libpango-1.0-0 \
  libpangocairo-1.0-0 \
  libssl1.1 \
  libtiff5 \
  libwebp6 \
  libxml2 \
  libpq5 \
  shared-mime-info \
  mime-support \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/media /app/static \
  && chown -R gamezone:gamezone /app/

# Copying poetry and venv into image
COPY --from=build-python $POETRY_HOME $POETRY_HOME
COPY --from=build-python $PYSETUP_PATH $PYSETUP_PATH

# Copying in our entrypoint
COPY ./scripts/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# venv already has runtime deps installed we get a quicker install
WORKDIR $PYSETUP_PATH
RUN poetry install

COPY . /app
WORKDIR /app

EXPOSE 8000
ENTRYPOINT /docker-entrypoint.sh $0 $@
CMD ["gunicorn", "--bind", ":8000", "--workers", "4", "--worker-class", "server.asgi.gunicorn_worker.UvicornWorker", "server.asgi:application"]


# 'lint' stage runs black and isort
# running in check mode means build will fail if any linting errors occur
#FROM development AS lint
#RUN black --config ./pyproject.toml --check app tests
#RUN isort --settings-path ./pyproject.toml --recursive --check-only
#CMD ["tail", "-f", "/dev/null"]


# 'test' stage runs our unit tests with pytest and
# coverage.  Build will fail if test coverage is under 95%
#FROM development AS test
#RUN coverage run --rcfile ./pyproject.toml -m pytest ./tests
#RUN coverage report --fail-under 95


# 'production' stage uses the clean 'python-base' stage and copyies
# in only our runtime deps that were installed in the 'builder-base'
#FROM python-base as production
#ENV FASTAPI_ENV=production
#
#COPY --from=build-python $VENV_PATH $VENV_PATH
#
#COPY ./scripts/docker-entrypoint.sh /docker-entrypoint.sh
#RUN chmod +x /docker-entrypoint.sh
#
#COPY . /app
#WORKDIR /app
#
#ENTRYPOINT /docker-entrypoint.sh $0 $@
#CMD ["gunicorn", "--bind", ":8000", "--workers", "4", "--worker-class", "server.asgi.gunicorn_worker.UvicornWorker", "server.asgi:application"]
