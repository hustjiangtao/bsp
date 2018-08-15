# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Momentjs"""


from jinja2 import Markup


class momentjs:
    """Momentjs"""

    def __init__(self, timestamp):
        self.timestamp = timestamp

    def render(self, fmt):
        return Markup(f"<script>document.write(moment(\"{self.timestamp.strftime('%Y-%m-%dT%H:%M:%S Z')}\").{fmt});</script>")

    def format(self, fmt):
        return self.render(f"format('{fmt}')")

    def calendar(self):
        return self.render("calendar()")

    def fromNow(self):
        return self.render("fromNow()")
