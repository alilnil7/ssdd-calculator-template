from confluent_kafka import Producer
import json

producer = Producer({'bootstrap.servers': 'localhost:9092'})

producer.produce('calc_requests', json.dumps({
    "id": "op1",
    "operation": "sum",
    "args": {"op1": 5.0, "op2": 3.0}
}).encode("utf-8"))

producer.flush()
print("✅ Mensaje enviado a Kafka")

