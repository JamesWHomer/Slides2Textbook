import logging
from pathlib import Path

def configure_logging(verbosity: int, quietness: int, log_file: Path | None) -> None:
    base_level = logging.INFO
    level = base_level - (verbosity * 10) + (quietness * 10)
    level = min(max(level, logging.DEBUG), logging.CRITICAL)
    handlers: list[logging.Handler] = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))

    logging.basicConfig(
        level=level,
        handlers=handlers,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )