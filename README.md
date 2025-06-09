# Calculator repository template

Template for the extra SSDD laboratory 2024-2025 Alibek Tugel

## Installation

To locally install the package, just run

```
pip install .
```
For installing kafka
```
pip install confluent-kafka
```

```
sudo apt install kafkacat
```

Or, if you want to modify it during your development,

```
pip install -e .
```

Create virtual environmen
```
python3 -m venv .venv
```
## Execution
Step 1: Start the Ice server
Activate the virtual environment:
```
source .venv/bin/activate
```
Run the server:
```
ssdd-calculator --Ice.Config=config/calculator.config
```
Step 2: Start Kafka via Docker
Open a second terminal:
```
docker-compose down        # stop containers if needed
```
```
docker-compose up -d       # start kafka
```
```
docker-compose ps          # Show the status of all containers defined in docker-compose.yml
```
Then:
```
source .venv/bin/activate
```

Listen to response topic:
```
kafkacat -b localhost:9092 -C -t topic-response
```
Step 3: Start Kafka client
Open a third terminal:
```
source .venv/bin/activate
kafka-calculator-client
```
Step 4: Send operations via Kafka
Open a fourth terminal and send test operations:
```
source .venv/bin/activate
```
Example (addition):
```
echo '{"id": "op1", "operation": "sum", "args": {"op1": 2.5, "op2": 3.0}}' | kafkacat -b localhost:9092 -P -t topic-request
```
Valid Operation Examples:
Addition: 
```
echo '{"id": "op1", "operation": "sum", "args": {"op1": 2.5, "op2": 3.0}}' | kafkacat -b localhost:9092 -P -t topic-request
```
Subtraction:
```
echo '{"id": "op2", "operation": "sub", "args": {"op1": 10.0, "op2": 4.0}}' | kafkacat -b localhost:9092 -P -t topic-request
```
Multiplication:
```
echo '{"id": "op3", "operation": "mult", "args": {"op1": 2.0, "op2": 5.0}}' | kafkacat -b localhost:9092 -P -t topic-request
```
Division:
```
echo '{"id": "op4", "operation": "div", "args": {"op1": 8.0, "op2": 2.0}}' | kafkacat -b localhost:9092 -P -t topic-request
```
## Send invalid messages to test error handling:
```
echo '{"id": "op5", "operation": "div", "args": {"op1": 5.0, "op2": 0.0}}' | kafkacat -b localhost:9092 -P -t topic-request
```
Division by zero:
```
echo '{"id": "op5", "operation": "div", "args": {"op1": 5.0, "op2": 0.0}}' | kafkacat -b localhost:9092 -P -t topic-request
```
Unsupported operation:
```
echo '{"id": "op6", "operation": "sqrt", "args": {"op1": 9.0}}' | kafkacat -b localhost:9092 -P -t topic-request
```
Invalid argument type:
```
echo '{"id": "op7", "operation": "sum", "args": {"op1": "abc", "op2": 2.0}}' | kafkacat -b localhost:9092 -P -t topic-request
```
Invalid (non-JSON) message:
```
echo hola | kafkacat -b localhost:9092 -P -t topic-request
```


## Configuration

This template only allows to configure the server endpoint. To do so, you need to modify
the file `config/calculator.config` and change the existing line.

For example, if you want to make your server to listen always in the same TCP port, your file
should look like

```
calculator.Endpoints=tcp -p 10000
```

## Slice usage

The Slice file is provided inside the `calculator` directory. It is only loaded once when the `calculator`
package is loaded by Python. It makes your life much easier, as you don't need to load the Slice in every module
or submodule that you define.

The code loading the Slice is inside the `__init__.py` file.



