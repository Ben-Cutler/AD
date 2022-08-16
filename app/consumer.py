import logging

logger = logging.getLogger(__name__)
class Consumer:
    def consume(self, payload):
        logger.info(payload)