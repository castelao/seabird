import os
import re
import logging
import pkg_resources

# import codecs
import yaml

from seabird.exceptions import CNVError
## from seabird.utils import basic_logger
#logging.basicConfig(level=logging.DEBUG)


def make_file_list(inputdir, inputpattern=".*\.cnv"):
    """ Search inputdir recursively for inputpattern
    """
    inputfiles = []
    for dirpath, dirnames, filenames in os.walk(inputdir):
        for filename in filenames:
            if re.match(inputpattern, filename):
                inputfiles.append(os.path.join(dirpath, filename))
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
        formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

    return logger


def press2depth(press, latitude):
    """ calculate depth from pressure
        http://www.seabird.com/application_notes/AN69.htm

        ATENTION, move it to fluid.
    """
    x = np.sin((np.pi/180) * latitude / 57.29578)**2
    g = 9.780318 * (1.0 + (5.2788e-3 + 2.36e-5 * x) * x) + 1.092e-6 * press
    depth = -((((-1.82e-15 * press + 2.279e-10) * press - 2.2512e-5) *
               press + 9.72659) * press) / g
    return depth




def load_rule(raw_text):
    """ Load the adequate rules to parse the data

        It should try all available rules, one by one, and use the one
          which fits.
    """
    rules_dir = 'rules'
    rule_files = pkg_resources.resource_listdir(__name__, rules_dir)
    rule_files = [f for f in rule_files if re.match('^cnv.*yaml$', f)]
    for rule_file in rule_files:
        text = pkg_resources.resource_string(
                __name__, os.path.join(rules_dir, rule_file))
        rule = yaml.load(text)
        # Should I load using codec, for UTF8?? Do I need it?
        # f = codecs.open(rule_file, 'r', 'utf-8')
        # rule = yaml.load(f.read())
        r = rule['header'] + rule['sep'] + rule['data']
        content_re = re.compile(r, re.VERBOSE)
        if re.search(r, raw_text, re.VERBOSE):
            #logging.debug("Using rules from: %s" % rule_file)
            #self.rule = rule
            parsed = content_re.search(raw_text).groupdict()
            return rule, parsed

    # If haven't returned a rule by this point, raise an exception.
    #logging.error("No rules able to parse it")
    raise CNVError(tag='noparsingrule')
