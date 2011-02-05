"""
screenshot_queue consumer
=========================

The screenshot_queue consumer listens to a RabbitMQ queue to listen for
requests to generate website screenshots.

"""

import os
from pika import (AsyncoreConnection, ConnectionParameters, PlainCredentials,
                  asyncore_loop)
from webkit2png import WebkitRenderer, init_qtgui
from settings import (RABBITMQ_HOST, RABBITMQ_USERNAME, RABBITMQ_PASSWORD,
                      RABBITMQ_QUEUE, SCREENSHOT_ROOT)

class ScreenshotConsumer(object):
    """A consumer for screenshot queue messages."""
    def __init__(self):
        # Initialize a QApplication
        self.application = init_qtgui()

        # Set up the renderer
        self.renderer = WebkitRenderer()
        self.renderer.width = 1024
        self.renderer.height = 768
        self.renderer.timeout = 10
        self.renderer.format = 'png'

    def _capture_screenshot(self, ch, method, properties, body):
        """Captures a website screenshot."""
        parameters = body.split()
        image = open(os.path.join(SCREENSHOT_ROOT, parameters[0]), 'w')
        self.renderer.render_to_file(url=parameters[1], file=image)
        image.close()

    def run(self):
        # Open RabbitMQ connection
        connection = AsyncoreConnection(ConnectionParameters(
            host=RABBITMQ_HOST, credentials=PlainCredentials(
            RABBITMQ_USERNAME, RABBITMQ_PASSWORD)))
        channel = connection.channel()

        # Declare the queue
        channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

        # Subscribe to the queue
        channel.basic_consume(self._capture_screenshot, queue=RABBITMQ_QUEUE,
                              no_ack=True)

        # Wait for data
        asyncore_loop()
