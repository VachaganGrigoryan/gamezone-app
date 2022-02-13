### Build and install packages
FROM python:3.10 as build-python

RUN apt-get -y update \
  && apt-get install -y gettext \
  # Cleanup apt cache
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

### Final image
FROM python:3.10-slim

RUN groupadd -r allof && useradd -r -g allof allof

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
  && chown -R allof:allof /app/

COPY --from=build-python /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=build-python /usr/local/bin/ /usr/local/bin/
COPY . /app
WORKDIR /app

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "4", "--worker-class", "server.asgi.gunicorn_worker.UvicornWorker", "server.asgi:application"]