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
        "args": {"op1": 5.0, "op2": 0.0}  # деление на 0 — для проверки ошибки
    },
    {
        "id": "op6",
        "operation": "pow",  # неизвестная операция — должно вернуть ошибку
        "args": {"op1": 2.0, "op2": 3.0}
    },
    {
        "id": "op7",
        "operation": "sum",
        "args": {"op1": "a", "op2": 1.0}  # неправильный тип — ошибка
    },
    {
        "id": "op8",
        "args": {"op1": 1.0, "op2": 1.0}  # отсутствует "operation"
    },
    {
        "id": "op9",
        "operation": "sub"  # отсутствуют аргументы
    }
]

for op in operations:
    producer.produce('topic-request', json.dumps(op).encode("utf-8"))
    print(f"📤 Отправлено: {op['id']}")
    time.sleep(0.2)  # небольшой интервал, чтобы не забивать очередь

producer.flush()
print("✅ Все сообщения отправлены.")


