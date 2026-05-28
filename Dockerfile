FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir pytest pytest-json-report

ENV PYTHONPATH=/app/src

CMD ["pytest", "--json-report"]