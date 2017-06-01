# -*- coding: utf-8 -*-

import os
import sys
import runpy
import threading
import schedule
import time

class Ticker(threading.Thread):
    def run(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

ticker = Ticker(name="Ticker")
ticker.daemon = True
ticker.start()

script_path = os.path.join(os.path.dirname(__file__), "jasper.py")
runpy.run_path(script_path, run_name="__main__")
