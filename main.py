import disnake
from disnake.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()
from botlog import setup_logging
import asyncio

token = os.getenv("token")
webhook_url = os.getenv("LOGGING_WEBHOOK_URL")

# logging 
logger = setup_logging(webhook_url)

# Inital setup
intents = disnake.Intents.default()
intents.message_content = True
intents.messages = True 

activity = disnake.CustomActivity(name="Ask me anything...!")
bot = commands.InteractionBot(intents=intents,activity=activity)


# starting the bot
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    logger.info(f"Logged in as {bot.user}")
   


# loading cogs
cog_modules = [
  "groq" ,"ping","uptime"
]
for module in cog_modules:
    try:
        bot.load_extension(f"cogs.{module}")
    except Exception as e:
        logger.error(f"Error loding cog {module} : {e}")
        print(f"Error : {e}")

#token 
bot.run(token) 
