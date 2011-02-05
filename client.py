"""
screenshot_queue client
=======================

The screenshot_queue client provides an interface to send requests to the
screenshot queue to generate screenshots.

"""

from pika import (AsyncoreConnection, BasicProperties, ConnectionParameters,
                  PlainCredentials)
from settings import (RABBITMQ_HOST, RABBITMQ_USERNAME, RABBITMQ_PASSWORD,
                      RABBITMQ_QUEUE)

class ScreenshotClient(object):
    """A client for screenshot queue messages."""
    def __init__(self):
        """Sets up the connection."""
        # Open RabbitMQ connection
        connection = AsyncoreConnection(ConnectionParameters(
            host=RABBITMQ_HOST, credentials=PlainCredentials(
            RABBITMQ_USERNAME, RABBITMQ_PASSWORD)))
        self.channel = connection.channel()

        # Declare the queue
        self.channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

    def screenshot(self, filename, url):
        """Sends a screenshot request to the queue."""
        self.channel.basic_publish(exchange='', routing_key=RABBITMQ_QUEUE,
                                   properties=BasicProperties(
                                   delivery_mode=2), body='%s %s' %
                                   (filename, url))
