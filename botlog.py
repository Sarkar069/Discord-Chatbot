import logging
import random
import disnake
import aiohttp
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
webhook_url = os.getenv('LOGGING_WEBHOOK_URL')

class DiscordHandler(logging.Handler):
    def __init__(self, webhook_url, emit_as_code_block=False, max_size=2000):
        super().__init__()
        self.webhook_url = webhook_url
        self.emit_as_code_block = emit_as_code_block
        self.max_size = max_size

    def emit(self, record):
        try:
            msg = self.format(record)
            if self.emit_as_code_block:
                msg = f"```{msg}```"

            random_color = random.randint(0, 0xFFFFFF)
            embed = disnake.Embed(
                description=msg[:self.max_size],
                color=random_color
            )
            data = {"embeds": [embed.to_dict()]}

            asyncio.create_task(self.send_log(data))
        except Exception as e:
            print(f"Exception in DiscordHandler emit: {e}")

    async def send_log(self, data):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=data) as response:
                    if response.status != 204:
                        text = await response.text()
                        print(f"Failed to send log to Discord: {response.status}, {text}")
        except Exception as e:
            print(f"Exception in DiscordHandler send_log: {e}")

def setup_logging(webhook_url):
    logger = logging.getLogger("Your bot's name")
    logger.setLevel(logging.DEBUG)

    FORMAT = logging.Formatter(
        "%(asctime)s | 📝 **Module:** %(name)s | 🔔 **Level:** %(levelname)s | ✨ **Message:** %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    discord_handler = DiscordHandler(webhook_url, emit_as_code_block=False, max_size=2000)
    discord_handler.setLevel(logging.DEBUG)
    discord_handler.setFormatter(FORMAT)

    logger.addHandler(discord_handler)
    return logger
