"""
screenshot_queue server
=======================

Runs the screenshot_queue consumer as a daemon.

Usage (xvfb optional)
---------------------

    xvfb-run --server-args='-screen 0,1024x768x24' python server.py start
    xvfb-run --server-args='-screen 0,1024x768x24' python server.py stop
    xvfb-run --server-args='-screen 0,1024x768x24' python server.py restart

"""

from daemon.runner import DaemonRunner
from consumer import ScreenshotConsumer

screenshot_app = ScreenshotConsumer()
screenshot_daemon = DaemonRunner(screenshot_app)
screenshot_daemon.do_action()
