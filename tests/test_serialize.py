#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Check if pickle can serialize seabird's data objects

"""

import os
from glob import glob
import pickle

from seabird.cnv import fCNV


def test_serialize_CNV():
        """ Serialize CNV
        """
        datadir = os.path.join(os.path.dirname(__file__), 'test_data')
        for f in glob(os.path.join(datadir, "*.cnv.OK")):
            profile = fCNV(f)
            profile2 = pickle.loads(pickle.dumps(profile))
            assert profile.attributes == profile2.attributes
            assert (profile.data == profile.data)


def test_serialize_fCNV():
        """ Serialize fCNV
        """
        datadir = os.path.join(os.path.dirname(__file__), 'test_data')
        for f in glob(os.path.join(datadir, "*.cnv.OK")):
            profile = fCNV(f)
            profile2 = pickle.loads(pickle.dumps(profile))
            assert profile.attributes == profile2.attributes
            assert (profile.data == profile.data)
