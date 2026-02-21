import asyncio
import logging
import random

import disnake


class DiscordLogWorker:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.queue = asyncio.Queue()
        self.session = None
        self.task = None

    async def start(self, session):
        self.session = session
        self.task = asyncio.create_task(self._worker())

    async def stop(self):
        if self.task:
            self.task.cancel()

    async def _worker(self):
        while True:
            embed_dict = await self.queue.get()
            try:
                await self.session.post(
                    self.webhook_url,
                    json={"embeds": [embed_dict]},
                )
            except Exception as e:
                print(f"Discord log send failed: {e}")
            finally:
                self.queue.task_done()

    def submit(self, embed_dict: dict):
        try:
            self.queue.put_nowait(embed_dict)
        except asyncio.QueueFull:
            pass


class DiscordHandler(logging.Handler):
    def __init__(self, worker: DiscordLogWorker, max_size=2000):
        super().__init__()
        self.worker = worker
        self.max_size = max_size

    def emit(self, record):
        try:
            msg = self.format(record)
            embed = disnake.Embed(
                description=msg[: self.max_size],
                color=random.randint(0, 0xFFFFFF),
            )
            self.worker.submit(embed.to_dict())
        except Exception as e:
            print(f"DiscordHandler error: {e}")
