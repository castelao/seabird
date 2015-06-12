#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import re
import pkg_resources
import os
import logging

try:
    import hashlib
    md5 = hashlib.md5
except ImportError:
    # for Python << 2.5
    import md5
    md5 = md5.new

import codecs
import yaml
import numpy as np
from numpy import ma

from seabird import CNVError
from seabird.utils import basic_logger
logging.basicConfig(level=logging.DEBUG)


class CNV(object):
    """ Main class to parse the .cnv style content

        Input:
            raw_text [String]: The full content of the .cnv file.

        Output:
            This class responds as it was a dictionary of variables,
              and each hash has a Masked Array.

        Ex.:
        f = open("CTD.cnv")
        text = f.read()
        profile = CNV(text)
        profile.keys()  # Return the available variables
        profile['temperature'] # Return the temperature sensor as a
          masked array
        profile['timeS'] # Return the time in Seconds
        profile.attributes # Return a dictionary with the file header
    """
    def __init__(self, raw_text, defaults=None, logger=None):

        self.logger = logger or logging.getLogger(__name__)

        self.raw_text = raw_text
        self.defaults = defaults
        self.attributes = {}
        # ----
        self.load_rule()

        if not hasattr(self, 'parsed'):
            return
        self.get_intro()
        self.get_attributes()
        self.prepare_data()
        self.get_datetime()
        self.get_location()

        # Think well how/where to implement this. It should overwrite
        #   the regular attributes input, but might be necessary to load the
        #   real attributes to respond right.
        # It definitely should not be here, but inside some function.
        try:
            for k in defaults['attributes']:
                self.attributes[k] = defaults['attributes'][k]
        except:
            pass

        self.load_data()
        self.products()

        self.check_consistency()

    def keys(self):
        """ Return the available keys in self.data
        """
        return [d.attributes['name'] for d in self.data]

    def __getitem__(self, key):
        """ Return the key array from self.data
        """
        for d in self.data:
            if d.attributes['name'] == key:
                return d
        raise KeyError('%s not found' % key)

    def load_rule(self):
        """ Load the adequate rules to parse the data

            It should try all available rules, one by one, and use the one
              which fits.
        """
        rules_dir = 'rules'
        rule_files = pkg_resources.resource_listdir(__name__, rules_dir)
        rule_files = [f for f in rule_files if re.match('^cnv.*yaml$', f)]
        for rule_file in rule_files:
            text = pkg_resources.resource_string(__name__,
                    os.path.join(rules_dir, rule_file))
            rule = yaml.load(text)
            # Should I load using codec, for UTF8?? Do I need it?
            #f = codecs.open(rule_file, 'r', 'utf-8')
            #rule = yaml.load(f.read())
            r = rule['header'] + rule['sep'] + rule['data']
            content_re = re.compile(r, re.VERBOSE)
            if re.search(r, self.raw_text, re.VERBOSE):
                self.logger.debug("Using rules from: %s" % rule_file)
                self.rule = rule
                self.parsed = content_re.search(self.raw_text).groupdict()
                return

        # If haven't returned a rule by this point, raise an exception.
        self.logger.error("No rules able to parse it")
        raise CNVError(tag='noparsingrule')

    def raw_header(self):
        r = self.rule['header'] + self.rule['sep']
        content_re = re.compile(r, re.VERBOSE)
        return content_re.search(self.raw_text).groupdict()

    def raw_data(self):
        r = self.rule['sep'] + self.rule['data']
        content_re = re.compile(r, re.VERBOSE)
        return content_re.search(self.raw_text).groupdict()

    def get_intro(self):
        """ Parse the intro part of the header
        """
        for k in self.rule['intro'].keys():
            pattern = re.compile(self.rule['intro'][k], re.VERBOSE)
            if pattern.search(self.parsed['intro']):
                self.attributes[k] = pattern.search(self.parsed['intro']).groupdict()['value']
                self.parsed['intro'] = pattern.sub('', self.parsed['intro'], count=1)
        if 'sbe_model' in self.attributes:
            if self.attributes['sbe_model'] in [9, '19plus V2']:
                self.attributes['instrument_type'] = 'CTD'
            elif self.attributes['sbe_model'] in [21, 45]:
                self.attributes['instrument_type'] = 'TSG'

    def get_attributes(self):
        """
        """
        for k in self.rule['descriptors'].keys():
            pattern = re.compile(self.rule['descriptors'][k], re.VERBOSE)
            if pattern.search(self.parsed['descriptors']):
                self.attributes[k] = \
                    pattern.search(self.parsed['descriptors']).groupdict()['value']
                self.parsed['descriptors'] = \
                    pattern.sub('', self.parsed['descriptors'], count=1)
        # ----
        self.attributes['md5'] = md5(self.raw_text).hexdigest()

    def prepare_data(self):
        """
        """
        attrib_text = self.parsed['descriptors']
        self.data = []
        self.ids = []
        # ----
        rule_file = "rules/refnames.yaml"
        text = pkg_resources.resource_string(__name__, rule_file)
        refnames = yaml.load(text)
        # ---- Parse fields
        pattern = re.compile(self.rule['fieldname'], re.VERBOSE)
        for x in pattern.finditer(str(attrib_text)):
            self.ids.append(int(x.groupdict()['id']))
            try:
                reference = refnames[x.groupdict()['name']]
                name = reference['name']
            except:
                name = x.groupdict()['name']
            self.data.append(ma.array([]))
            self.data[-1].attributes = {
                    'id': (x.groupdict()['id']),
                    'name': name,
                    'longname': x.groupdict()['longname'],
                    }
        attrib_text = pattern.sub('', attrib_text)

        # ---- Load span limits on each list item
        pattern = re.compile(self.rule['fieldspan'], re.VERBOSE)
        for x in pattern.finditer(str(attrib_text)):
            i = self.ids.index(int(x.groupdict()['id']))
            self.data[i].attributes['span'] = \
                [x.groupdict()['valuemin'].strip(), x.groupdict()['valuemax'].strip()]
        attrib_text = pattern.sub('', attrib_text)

    def load_data(self):
        """

            Sure there is a better way to do it.

            Think about, should I do things using nvalues as expected
              number of rows? Maybe do it free, and on checks, validate it.
              In the case of an incomplete file, I think I should load it
              anyways, and the check alerts me that it is missing data.

            There is a problem here. This atol is just a temporary solution,
              but it's not the proper way to handle it.
        """
        #data = ma.masked_values([d.split() for d in self.raw_data()['data'].split('\r\n')[:-1]],  float(self.attributes['bad_flag']))
        data_rows = re.sub('(\r\n\s*)+\r\n', '\r\n',
                self.raw_data()['data']).split('\r\n')[:-1]
        data = ma.masked_values(
                np.array(
                    [d.split() for d in data_rows], dtype=np.float),
                float(self.attributes['bad_flag']),
                atol = 1e-30)
        # Talvez usar o np.fromstring(data, sep=" ")
        for i in self.ids:
            attributes = self.data[i].attributes
            self.data[i] = data[:, i]
            self.data[i].attributes = attributes

            #ma.masked_all(int(self.attributes['nvalues']))

    def products(self):
        """
            To think about, should I really estimate the products,
              or should they be estimated on the fly, on demand?

            To Think About!! :
              I'm not sure what would be the best way to handle,
              timeQ. I actually couldn't find a definition of what
              is that. PyCurrents (Eric) considers the seconds from
              2010-1-1. It's probably a good solution.
              For now, I'll use the just the incremental time. At
              some point I defined the datetime before, so what
              matters now is the increment.
              If I have the timeQ, I must have a NMEA (Time), and
              Wait a minute, the NMEA Time is probably when the
              header is opened, not necessarily when the rossette was
              switched on. I'll just follow Eric for now.
        """
        if ('timeS' not in self.keys()):
            if ('timeJ' in self.keys()):
                j0 = int(self.attributes['datetime'].date().strftime('%j'))
                t0 = self.attributes['datetime'].time()
                t0 = (t0.hour*60+t0.minute)*60+t0.second
                # I need to subtract one day, but I'm not so sure why should I.
                #dref = datetime(self.attributes['datetime'].year,1,1) \
                #        - timedelta(days=1) \
                #        - self.attributes['datetime']
                #dJ0 = datetime(dref.year,1,1)
                timeS = ma.masked_all(self['timeJ'].shape,
                        self['timeJ'].dtype)
                timeS.set_fill_value(float(self.attributes['bad_flag']))
                ind = np.nonzero(~ma.getmaskarray(self['timeJ']))[0]
                try:
                    timeS[ind] = ma.array([timedelta(days=t).total_seconds()-t0 for t in self['timeJ'][ind]-j0])
                    #ma.array( [(dref + timedelta(float(d))).total_seconds() for d in self['timeJ'][ind]])
                except:
                    D = [timedelta(days=t) for t in self['timeJ'][ind]-j0]
                    #D = [(dref + timedelta(float(d))) for d in self['timeJ'][ind]]
                    timeS[ind] = ma.array([d.days*24*60*60+d.seconds-t0 for d in D])
            elif ('timeQ' in self.keys()):
                #yref = self.attributes['datetime'].year - \
                #        int(self['timeQ'].min()/86400./365.25
                #dref = datetime(yref,1,1)
                #timeS[ind] = self['timeQ'][ind] - self['timeQ'].min()

                timeS = ma.masked_all(self['timeQ'].shape,
                        self['timeQ'].dtype)
                timeS.set_fill_value(float(self.attributes['bad_flag']))
                ind = np.nonzero(~ma.getmaskarray(self['timeQ']))[0]
                try:
                    dref = (self.attributes['datetime'] -
                        datetime(2000, 1, 1)).total_seconds()
                except:
                    dref = (self.attributes['datetime'] -
                        datetime(2000, 1, 1))
                    dref = dref.days*24*60*60+dref.seconds
                timeS = self['timeQ'] - dref

            else:
                return

            self.data.append(timeS)
            self.data[-1].attributes = {'name': 'timeS'}
            self.ids.append(len(self.data))

    def get_datetime(self):
        """ Extract the reference date and time

            !!! ATENTION, better move it to a rule in the rules.
        """
        #datetime.strptime('Aug 28 2008 12:33:46','%b %d %Y %H:%M:%S')
        # Needed to include an :21, because some cases has a [bla bla]
        #   after.
        # It's probably not the best solution.
        self.attributes['datetime'] = datetime.strptime(
                self.attributes['start_time'][:20], '%b %d %Y %H:%M:%S')

    def get_location(self):
        """ Extract the station location (Lat, Lon)

            Sometimes the CTD unit station is not connected to the GPS, so it's
              written manually in the headerblob. In that case, I'll try to
              extract it

            !! ATENTION!!! Might be a good idea to store lat,lon as floats
              with min. and sec. as fractions.

            On some old format files, the notes where stored with single
              * instead of **. One possible solution is if can't load from
              notes, try to load from intro.

            In the rules, it is set to use only . as separator for the
              decimals of the minutes. Might be a good idea to allow \.|\,
              but on that case I would need to substitute , by . for proper
              load as a float.
        """
        if ('latitude' in self.attributes) and \
                (re.search(self.rule['latitude'],
                    self.attributes['latitude'],
                    re.VERBOSE)):
                lat = re.search(self.rule['latitude'],
                        self.attributes['latitude'],
                        re.VERBOSE).groupdict()
        elif ('notes' in self.raw_header().keys()) and \
                re.search(self.rule['latitude'],
                        self.raw_header()['notes'],
                        re.VERBOSE):
                lat = re.search(self.rule['latitude'],
                        self.raw_header()['notes'],
                        re.VERBOSE).groupdict()
        try:
                lat_deg = int(lat['degree'])
                lat_min = float(lat['minute'])
                #self.attributes['lat_deg'] = lat_deg
                #self.attributes['lat_min'] = lat_min
                self.attributes['latitude'] = lat_deg + lat_min/60.
                if lat['hemisphere'] in ['S', 's']:
                    self.attributes['latitude'] = -1*self.attributes['latitude']
        except:
            self.attributes['latitude'] = None

        if ('longitude' in self.attributes) and \
                (re.search(self.rule['longitude'],
                        self.attributes['longitude'],
                        re.VERBOSE)):
                lon = re.search(self.rule['longitude'],
                        self.attributes['longitude'],
                        re.VERBOSE).groupdict()
        elif ('notes' in self.raw_header().keys()) and \
                (re.search(self.rule['longitude'],
                        self.raw_header()['notes'],
                        re.VERBOSE)):
                lon = re.search(self.rule['longitude'],
                        self.raw_header()['notes'],
                        re.VERBOSE).groupdict()

        try:
                lon_deg = int(lon['degree'])
                lon_min = float(lon['minute'])
                #self.attributes['lon_deg'] = lon_deg
                #self.attributes['lon_min'] = lon_min
                self.attributes['longitude'] = lon_deg + lon_min/60.
                if lon['hemisphere'] in ['W', 'w']:
                    self.attributes['longitude'] = -1*self.attributes['longitude']
        except:
            self.attributes['longitude'] = None

    def as_DataFrame(self):
        """ Return the data as a pandas.DataFrame

            ATENTION, I should improve this.
        """
        try:
            import pandas as pd
        except:
            self.logger.warn("I'm not able to import pandas")
            return

        output = {}
        for k in self.keys():
            tmp = self[k].data
            tmp[self[k].mask] = np.nan
            output[k] = tmp
        output = pd.DataFrame(output)
        output['latitude'] = self.attributes['latitude']
        output['longitude'] = self.attributes['longitude']

        return output

    def check_consistency(self):
        """ Some consistency checks

            Check if the dataset is consistent with the info from the
              header.

            Might be a good idea to move these tests outside the
              class.
        """
        # Check if the number of variables is equal to nquan
        nquan = int(self.attributes['nquan'])
        if nquan != len(self.keys()):
            self.logger.warn("It was supposed to has %s variables." % (nquan))

        # Check if each variable have nvalues
        nvalues = int(self.attributes['nvalues'])
        for k in self.keys():
            if len(self[k]) != nvalues:
                self.logger.warn(
                        "\033[91m%s was supposed to has %s values, but found only %s.\033[0m" %
                        (k, nvalues, len(self[k])))


class fCNV(CNV):
    """ The same of CNV class, but the input is a filename
          instead of the straight text.

        Input:
            filename [String]: The path/filename to the CTD file.

        Output:
            This class responds as it was a dictionary of variables,
              and each hash has a Masked Array.

        Check out the doc of the class CNV for more details.

        Ex.:
        profile = fCNV("~/data/CTD.cnv")
        profile.keys()  # Return the available variables
        profile.attributes # Return a dictionary with the file header
          masked array
    """
    def __init__(self, file, defaultsfile=None, logger=None):

        self.logger = logger or logging.getLogger(__name__)
        self.logger.debug("Openning file: %s" % file)

        self.filename = file

        f = open(file)
        text = f.read()
        f.close()

        # if defaultsfile is given, read as a yaml file
        if defaultsfile:
            f = open(defaultsfile)
            defaults = yaml.load(f.read())
            f.close()
        else:
            defaults = None

        try:
            super(fCNV, self).__init__(text, defaults, logger=self.logger)
        except CNVError as e:
            if e.tag == 'noparsingrule':
                e.msg += " File: %s" % self.filename
            raise

        self.name = 'fCNV'
        self.attributes['filename'] = os.path.basename(file)

    def load_defaults(self, defaultsfile):
        pass


def press2depth(press, latitude):
    """ calculate depth from pressure
        http://www.seabird.com/application_notes/AN69.htm

        ATENTION, move it to fluid.
    """
    x = np.sin((np.pi/180) * latitude / 57.29578)**2
    g = 9.780318 * (1.0 + (5.2788e-3 + 2.36e-5 * x) * x) + 1.092e-6 * press
    depth = -((((-1.82e-15 * press + 2.279e-10) * press - 2.2512e-5) * press + 9.72659) * press) / g
    return depth
