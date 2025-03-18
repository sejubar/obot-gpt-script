export RABBITMQ_QUEUE=test-queue
export RABBITMQ_BROKER_URL='amqp://guest:guest@127.0.0.1:5672/%2F'
export RABBITMQ_USERNAME='guest'
export RABBITMQ_PASSWORD='guest'
export RABBITMQ_MESSAGE='{"d": "test"}'
export RABBITMQ_ACTION='publish'
python rabbitmq_message_executor.py