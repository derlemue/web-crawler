FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y \
    wkhtmltopdf chromium-driver libx11-6 libnss3 libxss1 libasound2 libxshmfence1 \
    && pip install --no-cache-dir -r requirements.txt

ENV TELEGRAM_TOKEN=7334722252:AAHh32jL_SOyiAdEk32R0bbUVdWu7YWl0Uo7334722252:AAHh32jL_SOyiAdEk32R0bbUVdWu7YWl0Uo
ENV TELEGRAM_CHAT_ID=7977097715

CMD ["python", "afd_watchlist_tool.py"]
