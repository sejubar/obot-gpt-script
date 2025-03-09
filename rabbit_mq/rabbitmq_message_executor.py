# rabbitmq_tool/rabbitmq/rabbitmq_message_executor.py
import os
from kombu import Connection, Queue

# Extract the tool's arguments from the env
queue_name = os.getenv('QUEUE_NAME')
message = os.getenv('MESSAGE')
broker_url = os.getenv('RABBITMQ_BROKER_URL')
action = os.getenv('ACTION', 'publish')  # Default action is publish

# Establish a connection to the RabbitMQ server
with Connection(broker_url) as conn:
    channel = conn.channel

    # Create a queue
    queue = Queue(queue_name)

    try:
        # Declare the queue
        queue.declare(channel=channel())

        if action == 'publish':
            # Produce
            producer = conn.Producer(serializer='json')
            producer.publish(body=message,
                                routing_key=queue_name)
            print("Message published successfully!")
        elif action == 'consume':
            # Consume
            consumed_messages = []

            def callback(body, message):
                consumed_messages.append(body)
                message.ack()

            with conn.Consumer(queues=queue, callbacks=[callback], no_ack=False) as consumer:
                conn.drain_events(timeout=5)
            print(consumed_messages)
        else:
            print("Invalid action. Please set RABBITMQ_ACTION to 'publish' or 'consume'.")
    except Exception as e:
        print(f"Error: {e}")