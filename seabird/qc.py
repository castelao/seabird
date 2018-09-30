# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst

from cotede.qc import ProfileQC
from . import fCNV


class fProfileQC(ProfileQC):
    """ Apply ProfileQC from CoTeDe straight from a file.
    """
    def __init__(self, inputfile, cfg=None, saveauxiliary=True, verbose=True,
            logger=None):
        """
        """
        #self.logger = logger or logging.getLogger(__name__)
        logging.getLogger(logger or __name__)
        self.name = 'fProfileQC'

        try:
            # Not the best way, but will work for now. I should pass
            #   the reference for the logger being used.
            input = fCNV(inputfile, logger=None)
        except CNVError as e:
            #self.attributes['filename'] = basename(inputfile)
            logging.error(e.msg)
            raise

        super(fProfileQC, self).__init__(input, cfg=cfg,
                saveauxiliary=saveauxiliary, verbose=verbose,
                logger=logger)
