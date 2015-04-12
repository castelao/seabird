import os
import re
import logging


def make_file_list(inputdir, inputpattern=".*\.cnv"):
    """ Search inputdir recursively for inputpattern
    """
    inputfiles = []
    for dirpath, dirnames, filenames in os.walk(inputdir):
        for filename in filenames:
            if re.match(inputpattern, filename):
                inputfiles.append(os.path.join(dirpath,filename))
    inputfiles.sort()
    return inputfiles

def basic_logger(logger=None):
    if logger is not None:
        assert type(logger) is logging.Logger
    else:
        # create logger
        logger = logging.getLogger('CNV logger')
        logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

    return logger


