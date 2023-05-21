# syntax=docker/dockerfile:latest
FROM python:3.9-alpine

WORKDIR /bot

RUN --mount=type=bind,source=Pipfile,target=Pipfile,ro \
    --mount=type=bind,source=Pipfile.lock,target=Pipfile.lock,ro \
    pip install pipenv && pipenv install --system --deploy

COPY . .
# Attention: you need to put config.json into the container via a volume!
CMD ["python", "./main.py"]
