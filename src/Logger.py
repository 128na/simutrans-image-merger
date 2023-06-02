import sys
import logging
from typing import Final

# https://stackoverflow.com/questions/75079148/python-logging-stdout-and-stderr-based-on-level
logging.basicConfig(format="%(funcName)s: %(message)s")

stdoutLogger: Final[logging.Logger] = logging.Logger(
    name="stdoutLogger", level=logging.INFO
)
stderrLogger: Final[logging.Logger] = logging.Logger(
    name="stderrLogger", level=logging.INFO
)

stdoutHandler = logging.StreamHandler(stream=sys.stdout)
stderrHandler = logging.StreamHandler(stream=sys.stderr)

stdoutLogger.addHandler(hdlr=stdoutHandler)
stderrLogger.addHandler(hdlr=stderrHandler)
