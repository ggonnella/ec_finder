# EcFinder package

from .ec_finder import __auto_setup, setup, update, search, __version__
__auto_setup()

# setup loguru by disabling it, as expected for libraries
from loguru import logger
logger.disable(__name__)
import sys

