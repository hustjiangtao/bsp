# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""Momentjs"""


from jinja2 import Markup


class momentjs:
    """Momentjs"""

    def __init__(self, timestamp):
        self.fmt_timestamp = timestamp.strftime('%Y-%m-%dT%H:%M:%S Z')

    def render(self, fmt):
        """render func"""
        return Markup(f"<script>document.write(moment(\"{self.fmt_timestamp}\").{fmt});</script>")

    def format(self, fmt):
        """format func"""
        return self.render(f"format('{fmt}')")

    def calendar(self):
        """calendar func"""
        return self.render("calendar()")

    def fromNow(self):
        """fromNow func"""
        return self.render("fromNow()")
