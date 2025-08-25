FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir uv
COPY pyproject.toml ./
RUN uv sync --frozen
COPY . .
CMD ["uv", "run", "celery", "-A", "celery.app", "worker", "-l", "INFO"]
