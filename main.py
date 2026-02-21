import os

import disnake
from dotenv import load_dotenv

from botlogs import setup_logging
from core.bot import BaseBot

load_dotenv()

TOKEN = os.getenv("token")
WEBHOOK_URL = os.getenv("LOGGING_WEBHOOK_URL")

logger, log_worker = setup_logging(WEBHOOK_URL)

intents = disnake.Intents.default()
intents.message_content = True
intents.messages = True

activity = disnake.CustomActivity(name="searching 💕")

bot = BaseBot(activity=activity, logger=logger, intents=intents)
bot.log_worker = log_worker  # 🔑 THIS IS REQUIRED

bot.load_cogs(["groq", "stats"])

bot.run(TOKEN)
