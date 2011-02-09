"""
screenshot_queue client
=======================

The screenshot_queue client provides an interface to send requests to the
screenshot queue to generate screenshots.

"""

from pika import (AsyncoreConnection, BasicProperties, ConnectionParameters,
                  PlainCredentials)

class ScreenshotClient(object):
    """A client for screenshot queue messages."""
    def __init__(self, username=None, password=None, queue=None, host=None):
        """Sets up the connection."""
        # Save attributes
        self.username = username
        self.password = password
        self.queue = queue if queue else 'screenshots'
        self.host = host if host else 'localhost'

        # Set up credentials if applicable
        if self.username and self.password:
            self.credentials = PlainCredentials(self.username, self.password)
        else:
            self.credentials = None

        # Open RabbitMQ connection
        connection = AsyncoreConnection(ConnectionParameters(host=self.host,
                                        credentials=self.credentials))
        self.channel = connection.channel()

        # Declare the queue
        self.channel.queue_declare(queue=self.queue, durable=True)

    def screenshot(self, filename, url):
        """Sends a screenshot request to the queue."""
        self.channel.basic_publish(exchange='', routing_key=self.queue,
                                   properties=BasicProperties(
                                   delivery_mode=2), body='%s %s' %
                                   (filename, url))
