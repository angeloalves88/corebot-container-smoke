FROM python:3.11-slim

RUN useradd -u 10001 -m bot
WORKDIR /app
COPY bot.py /app/bot.py
USER 10001

ENTRYPOINT ["python", "/app/bot.py"]
