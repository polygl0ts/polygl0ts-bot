FROM python:3.9-alpine

WORKDIR /bot

COPY Pipfile* ./
RUN pip install pipenv && pipenv install --system --deploy

COPY . .
# Attention: you need to put config.json into the container via a volume!
CMD ["python", "./main.py"]
