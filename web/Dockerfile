FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN apt update && apt install -y docker.io && \
    pip install --no-cache-dir flask python-dotenv bcrypt requests

CMD ["python", "app.py"]
