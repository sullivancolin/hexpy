# -*- coding: utf-8 -*-
"""Module for working with dates and times."""

from datetime import datetime


class Timestamp(object):
    """Class for working with dates and times.

    # Example Usage

    ```python
    >>> from hexpy import Timestamp
    >>> stamp = Timestamp(2017, 9, 26)
    >>> stamp.to_string()
    '2017-09-29T00:00:00'
    ```
    """

    def __init__(self, year, month, day, hour=0, minute=0, second=0,
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
        """Convert timestamp object to ISO format string."""
        return self.datetime.isoformat()

    @classmethod
    def from_string(cls, timestamp):
        """Instantiate Timestamp object from ISO format String."""
        t = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
        return cls(t.year, t.month, t.day, t.hour, t.minute, t.second)
