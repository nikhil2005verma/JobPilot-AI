"""Logging setup that redacts secrets."""
import logging
import re

from backend.config import get_settings

_PATTERNS = [re.compile(r"AIza[0-9A-Za-z_\-]{20,}"), re.compile(r"(?i)(api[_-]?key|token)=\S+")]


class RedactFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        for p in _PATTERNS:
            msg = p.sub("[REDACTED]", msg)
        record.msg, record.args = msg, ()
        return True


def setup_logging() -> None:
    root = logging.getLogger()
    if root.handlers:
        return
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    h.addFilter(RedactFilter())
    root.addHandler(h)
    root.setLevel(get_settings().log_level.upper())
