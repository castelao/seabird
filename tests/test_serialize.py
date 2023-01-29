#!/usr/bin/env python

""" Check if pickle can serialize seabird's data objects

"""

import os.path
from glob import glob
import pickle

from seabird.cnv import fCNV
from seabird.utils import sampledata


def test_serialize_fCNV():
    """Serialize fCNV"""
    datafiles = sampledata()
    assert len(datafiles) > 0, "No files available for testing at: %s" % datafiles
    for f in datafiles:
        profile = fCNV(f)
        profile2 = pickle.loads(pickle.dumps(profile))
        assert profile.attrs == profile2.attrs
        assert profile.data == profile.data
