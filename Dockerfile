# Stage 1: build dependencies
FROM python:3.11-slim as builder

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy only dependency files
COPY pyproject.toml poetry.lock* ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Stage 2: runtime
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies if needed (e.g., for psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]