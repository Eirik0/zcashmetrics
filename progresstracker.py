#!/usr/bin/env python2

import sys, time

class ProgressTracker:
    def __init__(self):
        self.last_progress = 0
        self.start_time = time.time()
        self.last_update_time = self.start_time

    def setProgress(self, current, total):
        current_progress = 100 * current / total
        while self.last_progress < current_progress:
            sys.stdout.write(".")
            self.last_progress += 1
            if self.last_progress % 5 == 0:
                sys.stdout.write(" ")
            if self.last_progress % 10 == 0:
                current_time = time.time()
                elapsed = int(current_time - self.last_update_time)
                sys.stdout.write("+{}\n".format(formatTime(elapsed)))
                self.last_update_time = current_time
        sys.stdout.flush()

    def getTimeElapsed(self):
        return int(time.time() - self.start_time)

def formatTime(elapsed):
    return "{:02d}:{:02d}:{:02d}".format(elapsed // 3600, elapsed % 3600 // 60, elapsed % 60)