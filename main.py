#!.venv/bin/python3

import argparse
from manager import Manager
from logging_config import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Automated Code Management with OpenAI")
        parser.add_argument('-g', '--git', type=str, required=True, help="Live Git URL")
        parser.add_argument('-n', '--num_workers', type=int, required=True, help="Number of workers")
        args = parser.parse_args()

        logger.info("Starting manager with Git URL: %s and %d workers", args.git, args.num_workers)
        manager = Manager(args.git, args.num_workers)
        manager.start()

    except Exception as e:
        logger.error("An error occurred in main execution: %s", e)
        raise
