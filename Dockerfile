# syntax=docker/dockerfile:latest
FROM python:3.11-alpine

WORKDIR /bot

RUN --mount=type=bind,source=Pipfile,target=Pipfile,ro \
    --mount=type=bind,source=Pipfile.lock,target=Pipfile.lock,ro \
    pip install pipenv && pipenv install --system --deploy

COPY src/ .

# Attention: you need to put config.json into the container via a volume!
CMD ["python3", "main.py"]
