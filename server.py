"""
screenshot_queue server
=======================

The screenshot_queue server connects to a RabbitMQ queue to listen for requests
to generate website screenshots.

"""

import os
from pika import (AsyncoreConnection, ConnectionParameters, PlainCredentials,
                  asyncore_loop)
from webkit2png import WebkitRenderer, init_qtgui
from settings import (RABBITMQ_HOST, RABBITMQ_USERNAME, RABBITMQ_PASSWORD,
                      RABBITMQ_QUEUE, SCREENSHOT_ROOT)

# Initialize a QApplication
application = init_qtgui()

# Set up the renderer
renderer = WebkitRenderer()
renderer.width = 1024
renderer.height = 768
renderer.timeout = 10
renderer.format = 'png'

def capture_screenshot(ch, method, properties, body):
    """Captures a website screenshot."""
    image = open(os.path.join(SCREENSHOT_ROOT, 'test2.png'), 'w')
    renderer.render_to_file(url=body, file=image)
    image.close()

# Open RabbitMQ connection
connection = AsyncoreConnection(ConnectionParameters(host=RABBITMQ_HOST,
    credentials=PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue=RABBITMQ_QUEUE)

# Subscribe to the queue
channel.basic_consume(capture_screenshot, queue=RABBITMQ_QUEUE, no_ack=True)

# Wait for data
asyncore_loop()
