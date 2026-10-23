import logging
import re

from backend.config import settings

_SECRET = re.compile(r"(AIza[0-9A-Za-z_\-]{20,}|ya29\.[0-9A-Za-z_\-]+|Bearer\s+[0-9A-Za-z_\-\.]+)")


class RedactFilter(logging.Filter):
    """Masks API keys / OAuth tokens if they ever reach a log line."""
    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = _SECRET.sub("[REDACTED]", str(record.msg))
        return True


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
        handler.addFilter(RedactFilter())
        logger.addHandler(handler)
        logger.setLevel(settings.log_level)
    return logger
