# ── Beanbot — De Glimlachfabriek ──────────────────────────────────────────────
# Slanke Python-container voor de Telegram-bot.
# Bouw:  docker build -t beanbot .
# Start: docker run --env-file .env beanbot
# ──────────────────────────────────────────────────────────────────────────────

# Gebruik een officiële, lichte Python-image (slim = geen onnodige pakketten)
FROM python:3.12-slim

# Metadata
LABEL org.opencontainers.image.title="Beanbot"
LABEL org.opencontainers.image.description="Privacy-first Telegram-assistent van De Glimlachfabriek"
LABEL org.opencontainers.image.source="https://github.com/deglimlachfabriek/Beanbot-"

# Geen interactieve prompts tijdens installatie
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Werkdirectory in de container
WORKDIR /app

# Kopieer alleen requirements eerst (Docker layer-caching)
COPY requirements.txt .

# Installeer dependencies (zonder onnodige build-cache)
RUN pip install --no-cache-dir -r requirements.txt

# Kopieer de rest van de broncode
COPY bot.py .

# Geen poort nodig: bot gebruikt long-polling (geen webhook)
# Start de bot
CMD ["python", "bot.py"]
