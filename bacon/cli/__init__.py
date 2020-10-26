import logging.config
import sys

from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install as rich_traceback_install


TRUTHY = ["1", "t", "true", "y", "yes"]


console = Console(file=sys.stderr)

# Weirdly, this didn't work.  Had to "install" the rich traceback.
# handler = RichHandler(console=console, rich_tracebacks=True)

handler = RichHandler(console=console)
rich_traceback_install(console=console)

logging.basicConfig(
    level=logging.INFO,
    format="{message}",
    style="{",
    # datefmt="[%X]",
    datefmt="[%F %r]",
    handlers=[handler],
)
