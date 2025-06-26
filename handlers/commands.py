from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.dictionary import define_word, get_synonyms
from telegram.constants import ParseMode

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! I’m your English Assistant Bot.\n\n"
        "I can help you with:\n"
        "• Word meanings\n"
        "• Synonyms\n"
        "Type anything to get started, or use /help for details."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 **English Learning Assistant - Help Guide**\n\n"
        "**Available Commands:**\n"
        "• `/start` - Welcome message\n"
        "• `/help` - Show this help guide\n"
        "• `/Define [word]` - Get word definition\n"
        "• `/Synonym [word]` - Find similar words\n"
        "• `/Grammar [sentence]` - Check grammar\n\n"
        "**Natural Language Examples:**\n"
        "• \"Define serendipity\"\n"
        "• \"What does perseverance mean?\"\n"
        "• \"Synonyms of brave\"\n"
        "• \"Grammar check: he go to school\"\n\n"
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

async def synonym_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a word to find synonyms. Example: /Synonym brave")
        return

    word = context.args[0]
    reply = await get_synonyms(word)
    await update.message.reply_text(reply)

