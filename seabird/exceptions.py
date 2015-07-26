# -*- coding: utf-8 -*-


class CNVError(Exception):
    """Base class for exceptions in this module."""
    def __init__(self, tag, msg=None):
        self.tag = tag

        if msg is not None:
            self.msg = msg
        elif tag == 'noparsingrule':
            self.msg = "There are no rules able to parse the input."

    def __str__(self):
        return repr(self.msg)
