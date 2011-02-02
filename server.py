"""
screenshot_queue server
=======================

Runs the screenshot_queue consumer as a daemon.

Usage
-----

    python server.py start
    python server.py stop
    python server.py restart

"""

from daemon.runner import DaemonRunner
from consumer import ScreenshotConsumer

screenshot_app = ScreenshotConsumer()
screenshot_daemon = DaemonRunner(screenshot_app)
screenshot_daemon.do_action()
