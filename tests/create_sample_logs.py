from felling import configure
import logging
import random

configure("./tests/sample_logs")
logger = logging.getLogger(__name__)
logger.info("Ash")

rand_int = random.randint(0, 10)
logger.info(f"{rand_int} has randomly been chosen.")

logger.info(f"{rand_int} squared is {rand_int**2}")

logger.info(f"{rand_int} + 10 is {rand_int+10}")
