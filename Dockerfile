FROM python:3.10-slim AS builder

ENV ENV=${ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONPATH=/app/ \
  # Disable pip cache to make docker image smaller
  PIP_NO_CACHE_DIR=1 \
  # Disable pip version check
  PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y \
    build-essential \
    cron \
    # Cleaning cache:
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip -r requirements.txt

ADD ./app /app
WORKDIR /app

USER root

ENTRYPOINT ["python3"]
CMD ["app.py"]
