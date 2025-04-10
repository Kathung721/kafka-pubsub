from kafka import KafkaConsumer
import json
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("consumer")

KAFKA_BOOTSTRAP_SERVERS = "kafka:9093"
TOPIC_NAME = 'timelyMessage'

print("Consumer start")

# Try connecting to Kafka until it's ready 
while True:
    try:
        logger.info("Trying to connect to Kafka.")
        consumer = KafkaConsumer(
            TOPIC_NAME, 
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            group_id='hw-consumer-group',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=False
        )
        logger.info("Connected to Kafka.")
        break
    except Exception as e:
        print("Kafka not ready: {e}")
        time.sleep(5)

# Printing out messages
while True:
    msg_pack = consumer.poll(timeout_ms=1000)
    if msg_pack:
        for tp, messages in msg_pack.items():
            for message in messages:
                print(f"Received: {message.value}")
    else:
        print("No message yet.")