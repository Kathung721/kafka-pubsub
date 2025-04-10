from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError, KafkaError
import json
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("producer")

KAFKA_BOOTSTRAP_SERVERS = 'kafka:9093'
TOPIC_NAME = 'timelyMessage'
CONSUMER_GROUP = 'hw-consumer-group'

# Creating topic
while True:
    try:
        logger.info("Trying to connect to Kafka Admin to create topic.")

        admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
        topic = NewTopic(name=TOPIC_NAME, num_partitions=1, replication_factor=1)

        admin_client.create_topics([topic])
        logger.info(f"Topic '{TOPIC_NAME}' created successfully.")
        admin_client.close()
        break
    except TopicAlreadyExistsError:
        logger.info(f"Topic '{TOPIC_NAME}' already exists.")
        break
    except Exception as e:
        logger.warning(f"Kafka not ready or topic creation failed: {e}")
        time.sleep(10)

# Connecting to Kafka Producer
while True:
    try:
        logger.info("Trying to connect to Kafka Producer.")

        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all',
            retries=5
        )
        logger.info("Kafka Producer connection established.")
        break
    except Exception as e:
        logger.warning(f"Kafka Producer not ready yet: {e}")
        time.sleep(10)

# Sending messages
for i in range(5):
    data = {'message': f'This is message {i}'}
    producer.send(TOPIC_NAME, value=data)
    print(f"Sent: {data}")
    time.sleep(10)

producer.flush()
producer.close()