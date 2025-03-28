FROM python:3.12-slim

# Set environment variables
ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Create a non-root user and set permissions
RUN mkdir -p /app/data && \
    useradd -m appuser && \
    chown -R appuser:appuser /app && \
    chmod 755 /app/data && \
    mkdir -p /opt/venv && \
    chown -R appuser:appuser /opt/venv

# Set working directory and switch to non-root user
WORKDIR /app
USER appuser

# Copy application files
COPY --chown=appuser:appuser docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh
COPY --chown=appuser:appuser . .

# Create virtual environment and install dependencies
RUN uv venv $VIRTUAL_ENV
ENV UV_PYTHON=$VIRTUAL_ENV/bin/python
RUN uv pip install -e "."

# Expose port
EXPOSE 8000

# Use entrypoint script
ENTRYPOINT ["/app/docker-entrypoint.sh"]
