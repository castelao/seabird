# Licensed under a 3-clause BSD style license - see LICENSE.rst

import logging
from os.path import basename

from cotede.qc import ProfileQC

from . import fCNV
from .exceptions import CNVError

module_logger = logging.getLogger("seabird.qc")


class fProfileQC(ProfileQC):
    """Apply ProfileQC from CoTeDe straight from a file."""

    def __init__(
        self, inputfile, cfg=None, saveauxiliary=True, verbose=True, logger=None
    ):
        """ """
        self.logger = logging.getLogger(logger or "seabird.qc.fProfileQC")
        self.name = "fProfileQC"

        try:
            # Not the best way, but will work for now. I should pass
            #   the reference for the logger being used.
            profile = fCNV(inputfile)
        except CNVError as e:
            self.attributes["filename"] = basename(inputfile)
            logging.error(e.msg)
            raise

        super().__init__(profile, cfg=cfg, saveauxiliary=saveauxiliary, verbose=verbose)
