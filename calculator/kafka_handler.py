import json
import Ice
from confluent_kafka import Consumer, Producer, KafkaError
from RemoteCalculator import CalculatorPrx

class KafkaHandler:
    def __init__(
        self,
        input_topic,
        output_topic,
        ice_proxy="calculator:default -p 10000",
        bootstrap_servers="localhost:9092"
    ):
        self.input_topic = input_topic
        self.output_topic = output_topic
        self.ice_proxy = ice_proxy
        self.bootstrap_servers = bootstrap_servers

        # Kafka
        self.consumer = Consumer({
            'bootstrap.servers': self.bootstrap_servers,
            'group.id': 'calculator-group',
            'auto.offset.reset': 'earliest'
        })
        self.consumer.subscribe([self.input_topic])
        self.producer = Producer({'bootstrap.servers': self.bootstrap_servers})

        # Ice
        self.communicator = Ice.initialize()
        self.ice_client = CalculatorPrx.checkedCast(
            self.communicator.stringToProxy(self.ice_proxy)
        )

    def process_messages(self):
        print(f" KafkaHandler listen topic '{self.input_topic}'...")

        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() != KafkaError._PARTITION_EOF:
                        print(f" Kafka error: {msg.error()}")
                    continue

                raw_value = msg.value()
                if not raw_value:
                    print(" Empty message.")
                    continue

                try:
                    payload = json.loads(raw_value.decode('utf-8'))
                except json.JSONDecodeError:
                    self._send_error("unknown", "format error")
                    continue

                msg_id = payload.get("id", "unknown")

                if not all(k in payload for k in ("id", "operation", "args")):
                    self._send_error(msg_id, "missing fields")
                    continue

                args = payload["args"]
                op = payload["operation"]

                if op not in ("sum", "sub", "mult", "div"):
                    self._send_error(msg_id, "operation not found")
                    continue

                try:
                    op1 = float(args["op1"])
                    op2 = float(args["op2"])
                except (KeyError, TypeError, ValueError):
                    self._send_error(msg_id, "invalid operands")
                    continue

                try:
                    result = getattr(self.ice_client, op)(op1, op2)
                    self._send_response(msg_id, result)
                    print(f" Operation completed {op}({op1}, {op2}) = {result}")
                except Exception as ice_error:
                    self._send_error(msg_id, f"ICE error: {str(ice_error)}")

        except KeyboardInterrupt:
            print(" Stopped by user.")
        finally:
            self.consumer.close()
            self.communicator.destroy()

    def _send_response(self, msg_id, result):
        message = {
            "id": msg_id,
            "status": True,
            "result": result
        }
        self.producer.produce(self.output_topic, json.dumps(message).encode('utf-8'))
        self.producer.flush()

    def _send_error(self, msg_id, reason):
        message = {
            "id": msg_id,
            "status": False,
            "error": reason
        }
        self.producer.produce(self.output_topic, json.dumps(message).encode('utf-8'))
        self.producer.flush()
        print(f"Error [{msg_id}]: {reason}")
