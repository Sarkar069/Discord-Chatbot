import os
from dotenv import load_dotenv

load_dotenv()

DEV_GUILD_ID = int(os.getenv("DEV_GUILD_ID", 0)) if os.getenv("DEV_GUILD_ID") else None

def dev_guild_only():
    """Return [DEV_GUILD_ID] if set, else None."""
    return [DEV_GUILD_ID] if DEV_GUILD_ID else None
