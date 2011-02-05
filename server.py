"""
screenshot_queue server
=======================

The screenshot_queue server starts the screenshot_queue consumer loop.

Usage (xvfb optional)
---------------------

    xvfb-run -a --server-args='-screen 0, 1024x768x24' python server.py &

"""

from consumer import ScreenshotConsumer

consumer = ScreenshotConsumer()
consumer.run()
