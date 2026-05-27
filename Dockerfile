FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install pyyaml pytest

ENV PYTHONPATH=/app/src

CMD ["pytest"]
