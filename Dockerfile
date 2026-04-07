FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    gettext \
    build-essential \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install project dependencies
# Copy only requirements first to leverage Docker layer caching
COPY requirements.txt /app/
RUN pip install --upgrade pip \
 && pip install -r /app/requirements.txt

COPY . /app

# Add entrypoint to run migrations and collectstatic at container start
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["sh", "-c", "gunicorn code_levels.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3"]
