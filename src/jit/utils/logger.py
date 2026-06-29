import sys
from pathlib import Path

from loguru import logger as _logger

from jit.config.settings import settings

# Create log directory if it doesn't exist
Path(settings.log_file).parent.mkdir(parents=True, exist_ok=True)

# Remove the default Loguru logger
_logger.remove()

# Console logging
_logger.add(
    sys.stdout,
    level=settings.log_level,
    colorize=True,
    backtrace=True,
    diagnose=True,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    ),
)

# File logging
_logger.add(
    settings.log_file,
    level=settings.log_level,
    rotation=settings.log_rotation,
    retention=settings.log_retention,
    compression="zip",
    enqueue=True,
    backtrace=True,
    diagnose=True,
    encoding="utf-8",
)

logger = _logger
