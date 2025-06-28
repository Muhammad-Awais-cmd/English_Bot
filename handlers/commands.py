from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.dictionary import define_word
from telegram.constants import ParseMode

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! I’m your English Assistant Bot.\n\n"
        "I can help you with:\n"
        "• Word meanings\n"
        "• Definitions\n"
        "Type anything to get started, or use /help for details."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 **English Learning Assistant - Help Guide**\n\n"
        "**Available Commands:**\n"
        "• `/start` - Welcome message\n"
        "• `/help` - Show this help guide\n"
        "• `/Define [word]` - Get word definition\n"
        "**Natural Language Examples:**\n"
        "• \"Define serendipity\"\n"
        "💡 **Pro Tip:** Just type naturally - I understand conversational requests!",
        parse_mode="Markdown"
    )

async def define_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a word to define. Example: /Define benevolent")
        return

    word = context.args[0]
    reply = await define_word(word)
    await update.message.reply_text(reply)
