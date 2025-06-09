from confluent_kafka import Producer
import json
import time

producer = Producer({'bootstrap.servers': 'localhost:9092'})

operations = [
    {
        "id": "op1",
        "operation": "sum",
        "args": {"op1": 5.0, "op2": 3.0}
    },
    {
        "id": "op2",
        "operation": "sub",
        "args": {"op1": 10.0, "op2": 4.0}
    },
    {
        "id": "op3",
        "operation": "mult",
        "args": {"op1": 2.0, "op2": 3.5}
    },
    {
        "id": "op4",
        "operation": "div",
        "args": {"op1": 8.0, "op2": 2.0}
    },
    {
        "id": "op5",
        "operation": "div",
        "args": {"op1": 5.0, "op2": 0.0}  # division by 0 - to check for errors
    },
    {
        "id": "op6",
        "operation": "pow",  # unknown operation - should return an error
        "args": {"op1": 2.0, "op2": 3.0}
    },
    {
        "id": "op7",
        "operation": "sum",
        "args": {"op1": "a", "op2": 1.0}  # wrong type - error
    },
    {
        "id": "op8",
        "args": {"op1": 1.0, "op2": 1.0}  # "operation" is missing
    },
    {
        "id": "op9",
        "operation": "sub"  # no arguments
    }
]

for op in operations:
    producer.produce('topic-request', json.dumps(op).encode("utf-8"))
    print(f"📤 sended: {op['id']}")
    time.sleep(0.2)  # a small interval so as not to clog the queue

producer.flush()
print("✅ All message were send.")


