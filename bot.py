from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN
from handlers.commands import start_command, help_command, define_command, synonym_command
from handlers.message_router import handle_message
from telegram import BotCommand
import logging
import nest_asyncio
nest_asyncio.apply()

if __name__ == "__main__":
    import asyncio

async def main():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO 
    )

    print("Starting English Learner Assistant Bot...")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("define", define_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("help", "Show help guide"),
        BotCommand("define", "Define a word"),
    ]
    await app.bot.set_my_commands(commands)

    print("Bot is polling...")
    await app.run_polling(poll_interval=3)

if __name__ == "__main__":
    asyncio.run(main())
