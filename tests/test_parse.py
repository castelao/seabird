#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Parse some references with fCNV

"""

import os
from glob import glob

from seabird import cnv


def test_answer():
        """ Load different .cnv versions with fCNV
        """
        datadir = os.path.join(os.path.dirname(__file__), 'test_data')
        for f in glob(os.path.join(datadir, "*.cnv.OK")):
            print("Loading file: %s" % f)
            profile = cnv.fCNV(f)
