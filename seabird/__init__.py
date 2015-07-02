# -*- coding: utf-8 -*-

__author__ = 'Guilherme Castelao'
__email__ = 'guilherme@castelao.net'
__version__ = '0.6.0'

#from cnv import *

#__all__ = ['CNV', 'fCNV']

class CNVError(Exception):
    """Base class for exceptions in this module."""
    def __init__(self, tag, msg=None):
        self.tag = tag

        if msg is not None:
            self.msg = msg
        elif tag == 'noparsingrule':
            self.msg = "There are no rules able to parse the input."
