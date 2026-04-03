FROM python:3.12-slim

# 1. Install minimal runtime dependency for PostgreSQL client
RUN apt-get update && apt-get install -y \
    libpq5 \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Install Playwright browsers
RUN playwright install chromium --with-deps

COPY . .

# 3. Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["python", "main.py"]