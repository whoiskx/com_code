from kafka import KafkaProducer
from kafka.errors import KafkaError

producer = KafkaProducer(
    bootstrap_servers=[
        "localhost:9093",
  "localhost:9094"
  ]
)

future = producer.send("user-event", b'I am rito yan')
try:
    record_metadata = future.get(timeout=10)
    print(record_metadata)
except KafkaError as e:
    print(e)