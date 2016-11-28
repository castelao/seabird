#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Parse some references with fCNV

"""

import os.path
from glob import glob

from seabird.cnv import fCNV
from seabird.utils import seabird_dir


def test_answer():
        """ Load different .cnv versions with fCNV
        """
        datafiles = glob(os.path.join(seabird_dir(), 'data/*', "*.cnv"))
        assert len(datafiles) > 0, \
            "No files available for testing at: %s" % datafiles
        for f in datafiles:
            print("Loading file: %s" % f)
            profile = fCNV(f)
            assert len(profile.keys()) > 0
            assert len(profile.attributes.keys()) > 0
