# ===============================
# Stage 1: Base build stage
# ===============================
FROM python:3.13-slim AS base

# Create working directory
WORKDIR /app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt


# ===============================
# Stage 2: Production build stage
# ===============================
FROM python:3.13-slim

# --- Create non-root user ---
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Create application directory
RUN mkdir -p /app/staticfiles && chown -R appuser:appuser /app

# Set working directory
WORKDIR /app

# --- Copy dependencies from base stage ---
COPY --from=base /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=base /usr/local/bin /usr/local/bin

# --- Copy project source code ---
COPY --chown=appuser:appuser . .

# --- Set environment variables ---
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# --- Make entrypoint executable ---
RUN chmod +x /app/entrypoint.sh

# --- Expose Django/Gunicorn port ---
EXPOSE 8000

# --- Important: Run container as root initially ---
# This allows the entrypoint to fix permissions and perform collectstatic.
USER root

# --- Start application ---
CMD ["/app/entrypoint.sh"]