"""
This file contains code for displaying a progress indicator while running scripts

ProgressIndicator optionally takes in db, from django.db which it will occasionally
call to reset SQL queries.
"""
import math
import sys
import time

class ProgressIndicator():
    def __init__(self, total_count, db = None):
        self.total_count = total_count
        self.count = 0
        self.last_percent = 0
        self.start_time = time.time()
        self.db = db

        self.print_status(0, 0.0)

    def calculate_percent(self):
        return int(math.floor(1.0 * self.count / self.total_count * 100))

    def next(self):
        self.count += 1
        percent = self.calculate_percent()
        if percent != self.last_percent or self.count % 50 == 0:
            current_elapsed = time.time() - self.start_time
            self.print_status(percent, current_elapsed)
        if self.count == self.total_count:
            self.finish()
        self.last_percent = percent
        return self.count

    def print_status(self, percent, current_elapsed):
        print percent,"% - ",self.count,"iterations - ",current_elapsed,"seconds     \r",
        sys.stdout.flush()
        if self.db != None:
            self.db.reset_queries()

    def finish(self):
        # Need to print a new line so that future text won't be on the same line
        print ""

