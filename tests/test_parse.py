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
            assert len(profile.attrs.keys()) > 0

def test_blank_note_line():
    """ Temporary solution to avoid #37 & #40

        Guarantee that issues #37 & #40 will not repeat. Maybe change this
          to test with load_rule instead?
    """
    blank_note_line = "* Sea-Bird SBE9  Data File:\n*\n* \n# name 3 = depSM\n# file_type = ascii\n*END*\n1\n"
    from seabird.utils import load_rule
    load_rule(blank_note_line)
