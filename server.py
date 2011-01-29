"""
rabbitmqtpy server
====================

The rabbitmqtpy server connects to a RabbitMQ queue to listen for requests to
generate website screenshots.

"""

import os
import pika
from webkit2png import WebkitRenderer, init_qtgui
from settings import RABBITMQ_HOST, SCREENSHOT_ROOT

# Initialize a QApplication
application = init_qtgui()

# Set up the renderer
renderer = WebkitRenderer()
renderer.width = 1024
renderer.height = 768
renderer.timeout = 10
renderer.format = 'png'

# Take a screenshot
image = open(os.path.join(SCREENSHOT_ROOT, 'test2.png'), 'w')
renderer.render_to_file(url='http://stackoverflow.com/', file=image)
image.close()
