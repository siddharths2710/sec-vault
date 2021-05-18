import sys
import logging
from __future__ import absolute_import, division, print_function

__all__ = [
    "__title__",
    "__summary__",
    "__uri__",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__copyright__",
]

__title__ = "sec-vault"
__summary__ = (
   "SWISS Army-knife password management toolkit"             
)
__uri__ = "https://github.com/siddharths2710/sec-vault"
__version__ = "0.0.1"
__author__ = "Siddharth Srinivasan"
__email__ = "siddharths2710@yahoo.com"
__license__ = "LGPL-2.1 License"
__copyright__ = "Copyright 2021 {0}".format(__author__)


logging.basicConfig(
    format="%(levelname)s %(message)s",
    level=logging.INFO,
    stream=sys.stdout,
)

