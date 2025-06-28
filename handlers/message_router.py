from telegram import Update
from telegram.ext import ContextTypes
from utils.dictionary import define_word

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Enhanced message routing with better pattern matching"""

    bot_username = (await context.bot.get_me()).username
    message_text = update.message.text.lower()

    # Only proceed if private chat or bot is mentioned
    if update.message.chat.type in ["group", "supergroup"]:
        if f"@{bot_username.lower()}" not in message_text:
            return  # Ignore group messages unless bot is mentioned
        message_text = message_text.replace(f"@{bot_username.lower()}", "").strip()
    else:
        message_text = message_text.strip()
    
    text = message_text
    
    # Definition patterns
    if any(text.startswith(pattern) for pattern in ["define ", "definition of ", "what is ", "what does ", "meaning of "]):
        word = (text.replace("define ", "", 1)
                   .replace("definition of ", "", 1)
                   .replace("what is ", "", 1)
                   .replace("what does ", "", 1)
                   .replace("meaning of ", "", 1)
                   .replace(" mean", "")
                   .replace("?", "")
                   .strip())
        
        if word:
            response = await define_word(word)
            await update.message.reply_text(response, parse_mode="Markdown")
        else:
            await update.message.reply_text("Please specify a word to define. Example: 'Define happiness'")
        return

    # Default helpful response
    else:
        await update.message.reply_text(
            "🤖 **How can I help you today?**\n\n"
            "I can assist you with:\n"
            "• **Definitions:** 'Define serendipity' or 'What is perseverance?'\n"
            "💡 *Just type naturally - I'll understand what you need!*",
            parse_mode="Markdown"
        )