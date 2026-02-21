import logging

import aiohttp
from disnake.ext import commands


class BaseBot(commands.InteractionBot):
    def __init__(self, *, activity=None, logger=None, log_worker=None, intents=None):
        super().__init__(activity=activity, intents=intents)

        self.logger = logger or logging.getLogger("your bot name")
        self.log_worker = log_worker
        self.http_session: aiohttp.ClientSession | None = None

    # --------------------
    # LIFECYCLE
    # --------------------

    async def on_connect(self):
        if self.http_session is None:
            self.http_session = aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(limit=50, ttl_dns_cache=300),
                timeout=aiohttp.ClientTimeout(total=15),
            )
            self.logger.info("Shared HTTP session created")

        # Start log worker once (reconnect-safe)
        if self.log_worker and not getattr(self.log_worker, "running", False):
            await self.log_worker.start(self.http_session)
            self.logger.info("Discord log worker started")

    async def on_ready(self):
        session_id = getattr(self.ws, "session_id", None)

        self.logger.info(
            "Gateway ready as %s (session_id=%s)",
            self.user,
            session_id,
        )

        # reset counter on a fresh session
        self.reconnects = 0

    async def on_disconnect(self):
        self.reconnects += 1

        self.logger.warning(
            "Gateway disconnected (reconnects=%d)",
            self.reconnects,
        )

    async def on_resumed(self):
        session_id = getattr(self.ws, "session_id", None)

        self.logger.info(
            "Gateway session resumed (session_id=%s, reconnects=%d)",
            session_id,
            self.reconnects,
        )

    # --------------------
    # CLEAN SHUTDOWN
    # --------------------

    async def close(self):
        self.logger.warning("Bot shutdown initiated")

        if self.log_worker:
            self.logger.info("Stopping log worker")
            await self.log_worker.stop()

        if self.http_session and not self.http_session.closed:
            await self.http_session.close()
            self.logger.info("HTTP session closed")

        await super().close()

    # --------------------
    # HELPERS
    # --------------------

    def load_cogs(self, modules):
        for module in modules:
            try:
                self.load_extension(f"cogs.{module}")
                # self.logger.info("Loaded cog: %s", module)
            except Exception:
                self.logger.exception("Failed to load cog: %s", module)
