import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Schakel logging in om fouten veilig te monitoren
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Welkomstcommando voor gebruikers (/start)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hallo! Ik ben Beanbot, de privacy-first assistent van De Glimlachfabriek. "
        "Ik ben succesvol opgestart en klaar om non-profits veilig te ondersteunen."
    )

# Veilige verwerking van berichten
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    
    # Standaard respectvolle en mensgerichte reactie
    reply = f"Bericht veilig ontvangen door Beanbot. Samen bouwen we aan een ondersteunende toekomst. U schreef: {user_text}"
    
    await update.message.reply_text(reply)

def main() -> None:
    # VEILIGHEID: De geheime token wordt uit de afgeschermde omgevingsvariabelen geladen
    TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    
    if not TOKEN:
        print("Fout: Geen TELEGRAM_BOT_TOKEN gevonden in de veilige omgevingsvariabelen!")
        return

    # Start de applicatie op met de token
    application = Application.builder().token(TOKEN).build()

    # Koppel de acties aan de bot
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Activeer de luisterstand
    print("Beanbot is actief en luistert via een beveiligde verbinding...")
    application.run_polling()

if __name__ == '__main__':
    main()
