# -*- coding: utf-8 -*-
"""Module for working with dates and times."""

from datetime import datetime


class Timestamp(object):
    """docstring for Timestamp"""

    def __init__(self, day, month, year, hour=0, minute=0, second=0,
                 zone=None):
        super(Timestamp, self).__init__()
        self.day = day
        self.month = month
        self.year = year
        self.hour = hour
        self.minute = minute
        self.second = second
        self.zone = zone
        self.datetime = datetime(self.year, self.month, self.day, self.hour,
                                 self.minute, self.second)

    def to_string(self):
        return self.datetime.isoformat()

    @classmethod
    def from_string(cls, timestamp):
        t = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
        return cls(t.day, t.month, t.year, t.hour, t.minute, t.second)