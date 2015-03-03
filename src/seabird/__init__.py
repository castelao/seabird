#from cnv import *

#__all__ = ['CNV', 'fCNV']

class CNVError(Exception):
    """Base class for exceptions in this module."""
    def __init__(self, tag, msg):
        self.tag = tag
        self.msg = msg
