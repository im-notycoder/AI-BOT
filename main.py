from telegram.ext import ApplicationBuilder
from plugins.start import setup_start_handlers
from plugins.user_commands import setup_user_handlers
from plugins.admin_commands import setup_admin_handlers
from plugins.model_selection import setup_model_handlers

# Environment variables
TELEGRAM_BOT_TOKEN = "8199859768:AAEcIc-qmh3IHAwetaZS-nSdPVoKcpbcvdA"

def main():
    """Start the Telegram bot."""
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Setup all handlers
    setup_start_handlers(application)
    setup_user_handlers(application)
    setup_admin_handlers(application)
    setup_model_handlers(application)

    # Start polling
    application.run_polling()


if __name__ == "__main__":
    main()
