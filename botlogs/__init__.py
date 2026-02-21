# botlogs/__init__.py
import logging

from botlogs.discord_logger import DiscordHandler, DiscordLogWorker


def setup_logging(webhook_url: str):
    logger = logging.getLogger("Your bot name")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )

    worker = DiscordLogWorker(webhook_url)

    handler = DiscordHandler(worker)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger, worker
