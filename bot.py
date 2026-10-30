import logging
import os

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Logging aan, maar zonder inhoud van berichten.
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# Voorkom dat de HTTP-bibliotheek de bot-token (staat in de URL) in de logs schrijft
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Telegram staat maximaal 4096 tekens per bericht toe; we houden marge.
MAX_REPLY_LENGTH = 4000


def parse_allowed_ids(raw: str) -> set[int]:
    """Zet '123, 456' om naar {123, 456}. Ongeldige delen worden genegeerd."""
    ids = set()
    for part in (raw or "").split(","):
        part = part.strip()
        if part.isdigit():
            ids.add(int(part))
    return ids


def build_reply(user_text: str) -> str:
    """Maak het antwoord en kap het af zodat het binnen de Telegram-limiet blijft."""
    prefix = "Bericht ontvangen door BoonesBot. U schreef: "
    return prefix + user_text[: MAX_REPLY_LENGTH - len(prefix)]


def is_allowed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Is de lijst leeg, dan mag iedereen. Anders alleen de opgegeven gebruikers-ID's."""
    allowed = context.application.bot_data.get("allowed_ids", set())
    if not allowed:
        return True
    user = update.effective_user
    return user is not None and user.id in allowed


# Welkomstcommando voor gebruikers (/start)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_allowed(update, context):
        await update.message.reply_text("Deze bot is niet openbaar.")
        return
    await update.message.reply_text(
        "Hallo! Ik ben BoonesBot, de assistent van De Glimlachfabriek. "
        "Ik ben opgestart en klaar om non-profits te ondersteunen.\n\n"
        "Let op: dit gesprek loopt via Telegram. Deel hier geen gevoelige persoonsgegevens."
    )


# Toont het eigen Telegram-ID, nodig om jezelf aan de toegangslijst toe te voegen
async def show_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Jouw Telegram-ID is: {update.effective_user.id}")


# Verwerking van tekstberichten
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_allowed(update, context):
        await update.message.reply_text("Deze bot is niet openbaar.")
        return
    await update.message.reply_text(build_reply(update.message.text))


async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log fouten zonder berichtinhoud en zonder de bot-token."""
    message = str(context.error)
    token = getattr(context.application.bot, "token", "")
    if token:
        message = message.replace(token, "***")
    logger.error("Fout bij verwerken van een update: %s: %s", type(context.error).__name__, message)


def main() -> None:
    # VEILIGHEID: De geheime token wordt uit de afgeschermde omgevingsvariabelen geladen
    token = os.environ.get("TELEGRAM_BOT_TOKEN")

    if not token:
        print("Fout: Geen TELEGRAM_BOT_TOKEN gevonden in de omgevingsvariabelen!")
        raise SystemExit(1)

    allowed_ids = parse_allowed_ids(os.environ.get("ALLOWED_USER_IDS", ""))
    if not allowed_ids:
        logger.warning("ALLOWED_USER_IDS is niet ingesteld: iedereen die de bot vindt kan hem gebruiken.")

    # Start de applicatie op met de token
    application = Application.builder().token(token).build()
    application.bot_data["allowed_ids"] = allowed_ids

    # Koppel de acties aan de bot
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("id", show_id))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(on_error)

    # Activeer de luisterstand (long-polling: geen open poort)
    print("BoonesBot is actief en luistert...")
    application.run_polling()


if __name__ == '__main__':
    main()
