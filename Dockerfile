FROM python:3.11-slim AS builder

ENV POETRY_VERSION=1.8.3 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install --no-install-recommends -y build-essential curl git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install "poetry==${POETRY_VERSION}"

COPY pyproject.toml poetry.lock README.md ./
RUN poetry install --with mlops --no-root --sync

COPY src ./src
COPY scripts ./scripts
RUN poetry install --with mlops --only-root

FROM python:3.11-slim AS runtime

ENV POETRY_VERSION=1.8.3 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    PIP_NO_CACHE_DIR=1 \
    PATH="/app/.venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    ENVIRONMENT=local \
    DATA_DIR=data \
    RAW_DATA_DIR=data/raw \
    INTERIM_DATA_DIR=data/interim \
    PROCESSED_DATA_DIR=data/processed \
    MODEL_DIR=models \
    ARTIFACTS_DIR=artifacts \
    MLFLOW_TRACKING_URI=http://mlflow-server:5000 \
    MLFLOW_EXPERIMENT_NAME=ecommerce-recommender-docker

WORKDIR /app

RUN apt-get update \
    && apt-get install --no-install-recommends -y git \
    && rm -rf /var/lib/apt/lists/* \
    && pip install "poetry==${POETRY_VERSION}" \
    && groupadd --system app \
    && useradd --system --gid app --create-home app

COPY --from=builder /app/.venv /app/.venv
COPY --chown=app:app . .

RUN mkdir -p data/raw data/interim data/processed models artifacts mlruns \
    && chown -R app:app /app

USER app

CMD ["poetry", "run", "python", "scripts/validate_env.py"]
