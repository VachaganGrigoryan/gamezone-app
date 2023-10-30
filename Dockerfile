### Build and install packages
FROM python:3.11-slim as python-base

# Add user that will be used in the container.
RUN useradd gamezone

# Port used by this container to serve HTTP.
EXPOSE 8000

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
    POETRY_VERSION=1.4.2 \
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

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

# Set the working directory to /tmp.
WORKDIR /tmp

# Install the application server.
RUN pip install "gunicorn==20.0.4"

# Install poetry.
RUN pip install poetry
# Copy the project requirements files.
COPY ./pyproject.toml ./poetry.lock* /tmp/
# Export the project requirements to a requirements.txt file.
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Upgrade pip.
RUN pip install --upgrade pip

# Install the project requirements.
#COPY ./tmp/requirements.txt /tmp/
RUN pip install -r ./requirements.txt

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Set this directory to be owned by the "fireflies" user. This Wagtail project
# uses SQLite, the folder needs to be owned by the user that
# will be writing to the database file.
RUN chown gamezone:gamezone /app

# Copy the source code of the project into the container.
COPY --chown=gamezone:gamezone . .

# Use user "gamezone" to run the build commands below and the server itself.
USER gamezone

# Collect static files.
RUN #python manage.py collectstatic --noinput --clear

# Runtime command that executes when "docker run" is called, it does the
# following:
#   1. Migrate the database.
#   2. Start the application server.
# WARNING:
#   Migrating database at the same time as starting the server IS NOT THE BEST
#   PRACTICE. The database should be migrated manually or using the release
#   phase facilities of your hosting platform. This is used only so the
#   Wagtail instance can be started with a simple "docker run" command.
CMD set -xe; python manage.py migrate --noinput
#CMD gunicorn config.wsgi:application
#CMD daphne -b $HOST_URL -p $PORT config.asgi:application
CMD ["gunicorn", "--bind", ":8000", "--workers", "4", "--worker-class", "server.asgi.gunicorn_worker.UvicornWorker", "server.asgi:application"]
# gunicorn --bind 0.0.0.0:8000 jwt_berry.asgi -w 4 -k uvicorn.workers.UvicornWorker