FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

WORKDIR /app

COPY . .

# Installiere python-dotenv UND playwright (Python-Paket)
RUN pip install --no-cache-dir python-dotenv requests Pillow playwright && \
    python -m playwright install

CMD ["python", "main.py"]
