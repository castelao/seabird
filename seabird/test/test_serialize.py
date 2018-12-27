#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Check if pickle can serialize seabird's data objects

"""

import os.path
from glob import glob
import pickle

from seabird.cnv import fCNV
from seabird.utils import seabird_dir


def test_serialize_fCNV():
        """ Serialize fCNV
        """
        datafiles = glob(os.path.join(seabird_dir(), 'data/*', "*.cnv"))
        assert len(datafiles) > 0, \
            "No files available for testing at: %s" % datafiles
        for f in datafiles:
            profile = fCNV(f)
            profile2 = pickle.loads(pickle.dumps(profile))
            assert profile.attrs == profile2.attrs
            assert (profile.data == profile.data)
