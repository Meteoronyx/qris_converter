import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from qris_generator import generate_qris_qr

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Gunakan /nominal untuk generate QRIS dengan nominal tertentu. Contoh /20000\n"
    )

ERROR_MESSAGES = {
    "invalid_amount": "Kesalahan format nominal. Harap masukkan angka yang valid.",
    "negative_amount": "Nominal tidak boleh negatif.",
    "exceed_limit": "Nominal tidak boleh lebih dari IDR 500.000.",
    "generation_error": "Terjadi kesalahan saat membuat QRIS. Silakan coba lagi.",
}

async def generate_qr(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    command_text = update.message.text
    amount_str = command_text.lstrip('/')
    
    try:
        amount = int(amount_str)
        if amount <= 0:
            await update.message.reply_text(ERROR_MESSAGES["negative_amount"])
            return
        if amount > 500000:
            await update.message.reply_text(ERROR_MESSAGES["exceed_limit"])
            return
    except ValueError:
        await update.message.reply_text(ERROR_MESSAGES["invalid_amount"])
        return
    
    try:
        qr_image_path = generate_qris_qr(amount)
        with open(qr_image_path, 'rb') as photo:
            await update.message.reply_photo(photo, caption=f"QRIS for IDR {amount:,}")
    except Exception as e:
        logger.error(f"Error generating QRIS: {e}")
        await update.message.reply_text(ERROR_MESSAGES["generation_error"])

def main() -> None:
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        raise ValueError("Bot token not found in environment variables. Please set BOT_TOKEN in .env file.")
    
    application = Application.builder().token(bot_token).build()

    application.add_handler(CommandHandler("start", start))
    
    from telegram.ext import MessageHandler, filters
    application.add_handler(MessageHandler(filters.COMMAND & ~filters.Regex('^start$'), generate_qr))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
