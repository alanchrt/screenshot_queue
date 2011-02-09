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

class ScreenshotConsumer(object):
    """A consumer for screenshot queue messages."""
    def __init__(self, screenshot_root=None, username=None, password=None,
                 queue=None, host=None):
        # Save attributes
        self.screenshot_root = screenshot_root
        self.username = username
        self.password = password
        self.queue = queue if queue else 'screenshots'
        self.host = host if host else 'localhost'

        # Set up credentials if applicable
        if self.username and self.password:
            self.credentials = PlainCredentials(self.username, self.password)
        else:
            self.credentials = None

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
        image = open(os.path.join(self.screenshot_root, parameters[0]), 'w')
        self.renderer.render_to_file(url=parameters[1], file=image)
        image.close()

    def run(self):
        # Open RabbitMQ connection
        connection = AsyncoreConnection(ConnectionParameters(
            host=self.host, credentials=self.credentials))
        channel = connection.channel()

        # Declare the queue
        channel.queue_declare(queue=self.queue, durable=True)

        # Subscribe to the queue
        channel.basic_consume(self._capture_screenshot, queue=self.queue,
                              no_ack=True)

        # Wait for data
        asyncore_loop()
