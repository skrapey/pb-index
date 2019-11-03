#!/usr/bin/env python3
# pb-index.py
# Skräpey
# 2019/11/03

from argparse import ArgumentParser, Namespace
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler

import requests


__author__ = "Skräpey"
logger = logging.getLogger(__name__)


def initialize_logging(log_level: int, log_path: str, stdout: bool) -> None:
    """Initializing logging to either log_path or stdout."""
    logging_format = "{asctime}\t{name}:{lineno}\t{levelname}\t{message}"
    logging_datefmt = "%Y-%m-%d %M:%H:%S"
    if stdout:
        handler = logging.StreamHandler()
    else:
        handler = RotatingFileHandler(log_path, maxBytes=1000000000, backupCount=5, encoding="utf8")
    logging.basicConfig(format=logging_format, datefmt=logging_datefmt, style="{", level=log_level, handlers=[handler])


def pb_index(args: Namespace) -> int:
    """TODO"""
    # Remove func from args
    del args.func
    # Initialize logging
    initialize_logging(args.log_level, args.log_path, args.stdout)
    logger.info("Beginning scraping")
    logger.debug("ARGS: {}".format(args))
    logger.info("Finished scraping")
    return 0


def LogLevel(arg: str) -> int:
    """Parse log level to int according to logging module constants."""
    log_level = arg.upper()
    if hasattr(logging, log_level):
        return getattr(logging, log_level)
    raise ValueError("Received invalid value for log level {}".format(arg))


def initialize_parser() -> ArgumentParser:
    """Create command line parser."""
    parser = ArgumentParser(prog="pb-index.py",
                            description="Script to continuously index Pastebin to an ES cluster.")
    # TODO: Determine if this is required for Scraping API
    parser.add_argument("api_dev_key", type=str, help="Pastebin API developer key")
    parser.add_argument("-L",
                        "--limit",
                        type=int,
                        required=False,
                        default=100,
                        help="Maximum number of pastes to fetch for each iteration (default: 100)",
                        dest="api_limit")
    parser.add_argument("-l",
                        "--log",
                        type=str,
                        required=False,
                        default="{}_pb-index.log".format(datetime.utcnow().strftime("%Y%m%d%M%H")),
                        help="Path to log file (default: <%%Y%%m%%d%%M%%H>.pb-index.log)",
                        dest="log_path")
    parser.add_argument("--level",
                        type=LogLevel,
                        required=False,
                        default=logging.INFO,
                        choices={logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL},
                        help="Minimum logging level (default: INFO)",
                        dest="log_level")
    parser.add_argument("--stdout",
                        action="store_true",
                        help="Log to stdout only (for testing, default: False)",
                        dest="stdout")
    parser.set_defaults(func=pb_index)
    return parser


def main() -> int:
    """Program entry point."""
    parser = initialize_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    main()
