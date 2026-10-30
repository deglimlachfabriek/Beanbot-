# 🤖 BoonesBot — Powered by De Glimlach Fabriek

**BoonesBot** wordt een assistent voor non-profits, vrijwilligersorganisaties en maatschappelijke initiatieven. Het doel is om dagelijkse communicatie en administratie te ondersteunen, met privacy als uitgangspunt.

---

## Huidige stand (Pre-Alpha / MVP)

Wat de bot nu doet:
* Antwoordt op `/start` en `/id` (toont je Telegram-ID).
* Herhaalt tekstberichten als test van de verbinding.
* Kan beperkt worden tot opgegeven gebruikers via `ALLOWED_USER_IDS`.

Wat er nog niet is: AI-antwoorden, projectplanning, taakbeheer en WhatsApp. Dat staat op de roadmap.

---

## Privacy

* De bot slaat geen berichten op en schrijft de inhoud van berichten niet naar de logs.
* Gesprekken met een Telegram-bot lopen via de servers van Telegram en zijn niet end-to-end versleuteld. Deel er geen gevoelige persoonsgegevens mee.
* Zet `ALLOWED_USER_IDS` in je `.env`, zodat alleen de personen die je kiest de bot kunnen gebruiken.

---

## Starten met Docker

```bash
cp .env.example .env        # vul TELEGRAM_BOT_TOKEN in (via @BotFather)
docker compose up -d --build
docker compose logs -f
```

Stuur `/id` naar de bot om je Telegram-ID te zien en voeg die toe aan `ALLOWED_USER_IDS`.

---

## Status & Roadmap
- [x] Accountbeveiliging & 2FA geactiveerd
- [x] Basis repository structuur en Docker-setup
- [ ] Eerste functionele AI-workflow (Demo)
- [ ] Landing page & Sponsor-pitch lancering

---

## Bijdragen of sponsor worden?
Wil je als AI-talent meebouwen, of dit project financieel of praktisch steunen? Open een Issue in deze repository.

* **Organisatie:** De Glimlach Fabriek
* **Status:** Vrijwilligers en sponsors gezocht

---
*© 2026 De Glimlach Fabriek.*
