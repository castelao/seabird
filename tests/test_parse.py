#!/usr/bin/env python

""" Parse some references with fCNV

"""

import os.path
from glob import glob

from seabird.cnv import CNV, fCNV
from seabird.utils import sampledata


def test_answer():
    """Load different .cnv versions with fCNV"""
    datafiles = sampledata()
    assert len(datafiles) > 0, "No files available for testing at: %s" % datafiles
    for f in datafiles:
        print("Loading file: %s" % f)
        profile = fCNV(f)
        assert len(profile.keys()) > 0
        assert len(profile.attrs.keys()) > 0


def test_blank_note_line():
    """Temporary solution to avoid #37 & #40

    Guarantee that issues #37 & #40 will not repeat. Maybe change this
      to test with load_rule instead?
    """
    blank_note_line = "* Sea-Bird SBE9  Data File:\n*\n* \n# name 3 = depSM\n# file_type = ascii\n*END*\n1\n"
    from seabird.utils import load_rule

    load_rule(blank_note_line)


def test_column_header():
    """Parse with or without the data columns headers

    The data columns usually have a header, like:
    ...
    # file_type = ascii
    *END*
    Depth      Press
    3.973      3.995
    ...

    Parse the data even without the column header (Depth & Press).
    """
    raw = "* Sea-Bird SBE 9 Data File:\n* System UpLoad Time = Aug 01 2011 11:34:32\n# nquan = 2\n# nvalues = 3\n# name 0 = depSM: Depth [salt water, m]\n# name 1 = prDM: Pressure, Digiquartz [db]\n# start_time = Aug 01 2011 11:34:32\n# bad_flag = -9.990e-29\n# datcnv_date = Aug 02 2011 04:16:47, 7.18c\n# file_type = ascii\n*END*\n     Depth      Press  \n      3.973      3.995\n      4.079      4.102\n      3.902      3.924\n"
    profile = CNV(raw)
    assert len(profile["DEPTH"]) == 3
    assert profile["DEPTH"][0] == 3.973

    # Now without the headers
    profile = CNV(raw.replace("     Depth      Press  \n", ""))
    assert len(profile["DEPTH"]) == 3
    assert profile["DEPTH"][0] == 3.973


def test_empty_lines():
    """Ignore corrupted empty lines"""
    raw = "* Sea-Bird SBE 9 Data File:\n\n* System UpLoad Time = Aug 01 2011 11:34:32\n \n# nquan = 2\n# nvalues = 3\n# name 0 = depSM: Depth [salt water, m]\n# name 1 = prDM: Pressure, Digiquartz [db]\n# start_time = Aug 01 2011 11:34:32\n# bad_flag = -9.990e-29\n# datcnv_date = Aug 02 2011 04:16:47, 7.18c\n# file_type = ascii\n*END*\n     Depth      Press  \n      3.973      3.995\n      4.079      4.102\n      3.902      3.924\n"
    profile = CNV(raw)
