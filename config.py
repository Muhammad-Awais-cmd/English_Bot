import os
from dotenv import load_dotenv
from typing import Final

# Load environment variables
load_dotenv()

BOT_TOKEN: Final = os.getenv("BOT_TOKEN")
BOT_USERNAME: Final = os.getenv("BOT_USERNAME")

# Validate required environment variables
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in environment variables")
if not BOT_USERNAME:
    raise ValueError("BOT_USERNAME not found in environment variables")