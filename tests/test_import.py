#!/usr/bin/env python


def test_ImportShortcut():
    """Test shortcut to import CNV & fCNV

    CNV & fCNV are actually inside seabird.cnv, but to simplify
      I placed a shortcut.
    """
    from seabird import CNV
    from seabird import fCNV
