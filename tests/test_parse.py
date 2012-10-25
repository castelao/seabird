import os
from glob import glob

from cnv import cnv


def test():
    datadir = os.path.join(os.path.dirname(__file__), 'test_data')
    for f in glob(os.path.join(datadir, "*.cnv.OK")):
        profile = cnv.fCNV(f)
