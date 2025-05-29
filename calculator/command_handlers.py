"""Module containing the handler functions for CLI commands."""

import logging
import os
import sys

from calculator.server import Server
from calculator.kafka_handler import KafkaHandler

def calculator() -> None:
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(os.path.basename(sys.argv[0]))

    logger.info("Starting Ice server...")
    server = Server()
    sys.exit(server.main(sys.argv))


def kafka_client():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(os.path.basename(sys.argv[0]))

    try:
        input_topic = os.getenv("KAFKA_INPUT_TOPIC", "topic-request")
        output_topic = os.getenv("KAFKA_OUTPUT_TOPIC", "topic-response")
        kafka_bootstrap = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        ice_proxy = os.getenv("ICE_PROXY", "calculator:default -p 10000")

        logger.info(f"KafkaHandler starting with topics [{input_topic} → {output_topic}], "
                    f"Kafka at {kafka_bootstrap}, ICE proxy '{ice_proxy}'")

        kafka_handler = KafkaHandler(
            input_topic=input_topic,
            output_topic=output_topic,
            bootstrap_servers=kafka_bootstrap,
            ice_proxy=ice_proxy
        )
        kafka_handler.process_messages()
    except ImportError as e:
        logger.warning("Kafka disabled: %s", str(e))
    except Exception as e:
        logger.error("Kafka handler failed: %s", str(e), exc_info=True)
