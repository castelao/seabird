# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import re
import pkg_resources
import os
import logging
import struct
import json

try:
    import hashlib
    md5 = hashlib.md5
except ImportError:
    # for Python << 2.5
    import md5
    md5 = md5.new

# import codecs
import numpy as np
from numpy import ma

from seabird.exceptions import CNVError
from seabird.utils import load_rule

module_logger = logging.getLogger('seabird.cnv')


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
        profile.attrs # Return a dictionary with the file header
    """
    def __init__(self, raw_text, defaults=None):

        module_logger.debug('Initializing CNV class')

        # Clean empty lines first
        self.raw_text = re.sub('\n\s*(?=\n)', '', raw_text)
        self.defaults = defaults
        self.attrs = {}
        # ----
        self.rule, self.parsed = load_rule(self.raw_text)

        if not hasattr(self, 'parsed'):
            return
        self.get_intro()
        self.get_attrs()
        self.prepare_data()
        self.get_datetime()
        self.get_location()

        # Think well how/where to implement this. It should overwrite
        #   the regular attributes input, but might be necessary to load the
        #   real attributes to respond right.
        # It definitely should not be here, but inside some function.
        try:
            for k in defaults['attrs']:
                self.attrs[k] = defaults['attrs'][k]
        except:
            pass

        if 'bindata' in self.raw_data().keys():
            self.load_bindata()
        elif 'bottledata' in self.raw_data().keys():
            self.load_bottledata()
        else:
            self.load_data()

        self.products()

        self.check_consistency()

    def keys(self):
        """ Return the available keys in self.data
        """
        return [d.attrs['name'] for d in self.data]

    def __getitem__(self, key):
        """ Return the key array from self.data
        """
        for d in self.data:
            if d.attrs['name'] == key:
                return d
        raise KeyError('%s not found' % key)

    @property
    def attributes(self):
        return self.attrs

    def raw_header(self):
        r = self.rule['header'] + self.rule['sep']
        content_re = re.compile(r, re.VERBOSE)
        return content_re.search(self.raw_text).groupdict()

    def raw_data(self):
        if ('instrument_type' in self.attrs) and \
                self.attrs['instrument_type'] == 'CTD-bottle':
            return {'bottledata': self.parsed['data']}

        r = self.rule['sep'] + self.rule['data']
        content_re = re.compile(r, re.VERBOSE)
        return content_re.search(self.raw_text).groupdict()

    def get_intro(self):
        """ Parse the intro part of the header
        """
        for k in self.rule['intro'].keys():
            pattern = re.compile(self.rule['intro'][k], re.VERBOSE)
            if pattern.search(self.parsed['intro']):
                self.attrs[k] = pattern.search(
                        self.parsed['intro']
                        ).groupdict()['value']
                self.parsed['intro'] = pattern.sub(
                        '', self.parsed['intro'], count=1)
        try:
            self.attrs['instrument_type'] = \
                    self.rule['attributes']['instrument_type']
        except:
            if 'sbe_model' in self.attrs:
                if self.attrs['sbe_model'] in ['9', '17', '19plus',
                                               '19plus V2']:
                    self.attrs['instrument_type'] = 'CTD'
                elif self.attrs['sbe_model'] in ['21', '45']:
                    self.attrs['instrument_type'] = 'TSG'

    def get_attrs(self):
        """
        """
        for k in self.rule['descriptors'].keys():
            pattern = re.compile(self.rule['descriptors'][k], re.VERBOSE)
            if pattern.search(self.parsed['descriptors']):
                self.attrs[k] = pattern.search(
                            self.parsed['descriptors']
                            ).groupdict()['value']
                self.parsed['descriptors'] = \
                    pattern.sub('', self.parsed['descriptors'], count=1)
        # ----
        # Temporary solution. Failsafe MD5
        try:
            self.attrs['md5'] = md5(
                    self.raw_text.encode('utf-8')
                    ).hexdigest()
        except:
            self.attrs['md5'] = md5(
                    self.raw_text.decode(
                        'latin1', 'replace'
                        ).encode('utf-8')
                    ).hexdigest()

    def prepare_data(self):
        """
        """
        attrib_text = self.parsed['descriptors']
        self.data = []
        self.ids = []
        # ----
        rule_file = "rules/refnames.json"
        text = pkg_resources.resource_string(__name__, rule_file)
        refnames = json.loads(text.decode('utf-8'), encoding="utf-8")
        # ---- Parse fields

        if ('attrs' in self.rule) and \
                (self.rule['attrs']['instrument_type'] == 'CTD-bottle'):
                    rule = r"""
                      \s+ Bottle \s+ Date .* \n
                      \s+ Position \s+ Time .* \n
                    """
                    attrib_text = re.search(r"""\n \s+ Bottle \s+ Date \s+ (.*) \s*\r?\n \s+ Position \s+ Time""", self.parsed['header'], re.VERBOSE).group(1)
                    pattern = re.compile(r"""(?P<varname>[-|+|\w|\.|/]+)""", re.VERBOSE)

                    self.ids = [0, 1, 2]
                    self.data = [ma.array([]), ma.array([]), ma.array([])]
                    self.data[0].attrs = {
                            'id': 0,
                            'name': 'bottle'}
                    self.data[1].attrs = {
                            'id': 1,
                            'name': 'date'}
                    self.data[2].attrs = {
                            'id': 2,
                            'name': 'time'}

                    for x in pattern.finditer(str(attrib_text)):
                        self.ids.append(len(self.ids))
                        self.data.append(ma.array([]))
                        try:
                            reference = refnames[x.groupdict()['varname']]
                            varname = reference['name']
                            #longname = reference['longname']
                        except:
                            varname = x.groupdict()['varname']
                        self.data[-1].attrs = {
                                'id': self.ids[-1],
                                'name': varname,
                                #'longname': x.groupdict()['longname'],
                                }
                    return

        pattern = re.compile(self.rule['fieldname'], re.VERBOSE)
        for x in pattern.finditer(str(attrib_text)):
            self.ids.append(int(x.groupdict()['id']))
            try:
                reference = refnames[x.groupdict()['name']]
                name = reference['name']
            except:
                name = x.groupdict()['name']
            self.data.append(ma.array([]))
            self.data[-1].attrs = {
                    'id': (x.groupdict()['id']),
                    'name': name,
                    'longname': x.groupdict()['longname'],
                    }
        attrib_text = pattern.sub('', attrib_text)

        # ---- Load span limits on each list item
        pattern = re.compile(self.rule['fieldspan'], re.VERBOSE)
        for x in pattern.finditer(str(attrib_text)):
            i = self.ids.index(int(x.groupdict()['id']))
            self.data[i].attrs['span'] = [
                    x.groupdict()['valuemin'].strip(),
                    x.groupdict()['valuemax'].strip()]
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
        data_rows = re.sub(
                '(\n\s*)+\n', '\n',
                re.sub('\r\n', '\n', self.raw_data()['data'])
                ).split('\n')[:-1]
        data = ma.masked_values(
                np.array(
                    [CNV.__split_row(d) for d in data_rows], dtype=np.float),
                float(self.attrs['bad_flag']),
                atol=1e-30)
        # Talvez usar o np.fromstring(data, sep=" ")
        for i in self.ids:
            attrs = self.data[i].attrs
            self.data[i] = data[:, i]
            self.data[i].attrs = attrs

            # ma.masked_all(int(self.attrs['nvalues']))

    @staticmethod
    def __split_row(row):
        """
        Splits rows based on position. Seabird cnv files delimit fields after
        11 positions
        :param row: string representation of a row that needs to be split into
        fields
        :return: list of fields as strings
        """

        n = 11  # number of chars per row
        return [row[start:start+n].strip() for start in range(0, len(row), n)]

    def load_bindata(self):
        content = self.raw_data()['bindata']
        nvars = len(self.ids)
        fmt = nvars*'f'
        linesize = struct.calcsize(fmt)
        output = []
        # FIXME: This does not allow to read the most it can from a corrupted
        #   file, i.e. incomplete file.
        for n in range(len(content)/linesize):
            output.append(struct.unpack_from(fmt, content, n*linesize))
        data = ma.masked_values(
                output,
                float(self.attrs['bad_flag']),
                atol=1e-30)
        for i in self.ids:
            attrs = self.data[i].attrs
            self.data[i] = data[:, i]
            self.data[i].attrs = attrs

    def load_bottledata(self):
        content = self.raw_data()['bottledata']
        nvars = len(self.ids)
        for rec in re.finditer(self.rule['data'], content, re.VERBOSE):
            attrs = self.data[0].attrs
            self.data[0] = np.append(self.data[0],
                                     int(rec.groupdict()['bottle']))
            self.data[0].attrs = attrs

            d = datetime.strptime(rec.groupdict()['date'].strip(), '%b %d %Y')
            attrs = self.data[1].attrs
            self.data[1] = np.append(self.data[1], d.date())
            self.data[1].attrs = attrs

            d = datetime.strptime(rec.groupdict()['time'].strip(), '%H:%M:%S')
            attrs = self.data[2].attrs
            self.data[2] = np.append(self.data[2], d.time())
            self.data[2].attrs = attrs

            for n, v in enumerate(re.findall('[-|+|\w|\.]+',
                                  rec.groupdict()['values']),
                                  start=3):
                attrs = self.data[n].attrs
                self.data[n] = np.append(self.data[n], v)
                self.data[n].attrs = attrs

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
                j0 = int(self.attrs['datetime'].date().strftime('%j'))
                t0 = self.attrs['datetime'].time()
                t0 = (t0.hour*60+t0.minute)*60+t0.second
                # I need to subtract one day, but I'm not so sure why should I.
                # dref = datetime(self.attrs['datetime'].year,1,1) \
                #        - timedelta(days=1) \
                #        - self.attrs['datetime']
                # dJ0 = datetime(dref.year,1,1)
                timeS = ma.masked_all(
                        self['timeJ'].shape, self['timeJ'].dtype)
                timeS.set_fill_value(float(self.attrs['bad_flag']))
                ind = np.nonzero(~ma.getmaskarray(self['timeJ']))[0]
                try:
                    timeS[ind] = ma.array([
                        timedelta(days=t).total_seconds() - t0
                        for t in self['timeJ'][ind]-j0])
                    # ma.array( [(dref + timedelta(float(d))).total_seconds()
                    #   for d in self['timeJ'][ind]])
                except:
                    D = [timedelta(days=t) for t in self['timeJ'][ind]-j0]
                    # D = [(dref + timedelta(float(d)))
                    #   for d in self['timeJ'][ind]]
                    timeS[ind] = ma.array([
                        d.days * 86400 + d.seconds - t0 for d in D])
            elif ('timeQ' in self.keys()):
                # yref = self.attrs['datetime'].year - \
                #        int(self['timeQ'].min()/86400./365.25
                # dref = datetime(yref,1,1)
                # timeS[ind] = self['timeQ'][ind] - self['timeQ'].min()

                timeS = ma.masked_all(
                        self['timeQ'].shape, self['timeQ'].dtype)
                timeS.set_fill_value(float(self.attrs['bad_flag']))
                ind = np.nonzero(~ma.getmaskarray(self['timeQ']))[0]
                try:
                    dref = (self.attrs['datetime'] -
                            datetime(2000, 1, 1)).total_seconds()
                except:
                    dref = (self.attrs['datetime'] -
                            datetime(2000, 1, 1))
                    dref = dref.days*24*60*60+dref.seconds
                timeS = self['timeQ'] - dref

            else:
                return

            self.data.append(timeS)
            self.data[-1].attrs = {'name': 'timeS'}
            self.ids.append(len(self.data))

    def get_datetime(self):
        """ Extract the reference date and time

            !!! ATENTION, better move it to a rule in the rules.
        """
        # datetime.strptime('Aug 28 2008 12:33:46','%b %d %Y %H:%M:%S')
        # Needed to include an :21, because some cases has a [bla bla]
        #   after.
        # It's probably not the best solution.
        self.attrs['datetime'] = datetime.strptime(
                self.attrs['start_time'][:20], '%b %d %Y %H:%M:%S')

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
        if ('LATITUDE' in self.attrs) and \
                (re.search(self.rule['LATITUDE'],
                           self.attrs['LATITUDE'],
                           re.VERBOSE)):
                lat = re.search(self.rule['LATITUDE'],
                                self.attrs['LATITUDE'],
                                re.VERBOSE).groupdict()
        elif ('notes' in self.raw_header().keys()) and \
                re.search(self.rule['LATITUDE'],
                          self.raw_header()['notes'],
                          re.VERBOSE):
                lat = re.search(self.rule['LATITUDE'],
                                self.raw_header()['notes'],
                                re.VERBOSE).groupdict()
        try:
                lat_deg = int(lat['degree'])
                lat_min = float(lat['minute'])
                # self.attrs['lat_deg'] = lat_deg
                # self.attrs['lat_min'] = lat_min
                self.attrs['LATITUDE'] = lat_deg + lat_min/60.
                if lat['hemisphere'] in ['S', 's']:
                    self.attrs['LATITUDE'] = -self.attrs['LATITUDE']
        except:
            pass
            # self.attrs['LATITUDE'] = None

        if ('LONGITUDE' in self.attrs) and \
                (re.search(self.rule['LONGITUDE'],
                           self.attrs['LONGITUDE'],
                           re.VERBOSE)):
                lon = re.search(self.rule['LONGITUDE'],
                                self.attrs['LONGITUDE'],
                                re.VERBOSE).groupdict()
        elif ('notes' in self.raw_header().keys()) and \
                (re.search(self.rule['LONGITUDE'],
                           self.raw_header()['notes'],
                           re.VERBOSE)):
                lon = re.search(self.rule['LONGITUDE'],
                                self.raw_header()['notes'],
                                re.VERBOSE).groupdict()

        try:
                lon_deg = int(lon['degree'])
                lon_min = float(lon['minute'])
                # self.attrs['lon_deg'] = lon_deg
                # self.attrs['lon_min'] = lon_min
                self.attrs['LONGITUDE'] = lon_deg + lon_min/60.
                if lon['hemisphere'] in ['W', 'w']:
                    self.attrs['LONGITUDE'] = \
                            -self.attrs['LONGITUDE']
        except:
            pass
            # self.attrs['LONGITUDE'] = None

    def as_DataFrame(self):
        """ Return the data as a pandas.DataFrame

            ATENTION, I should improve this.
        """
        try:
            import pandas as pd
        except:
            module_logger.warning("I'm not able to import pandas")
            return

        output = {}
        for k in self.keys():
            tmp = self[k].data
            tmp[self[k].mask] = np.nan
            output[k] = tmp
        output = pd.DataFrame(output)
        output['LATITUDE'] = self.attrs['LATITUDE']
        output['LONGITUDE'] = self.attrs['LONGITUDE']
        if "datetime" in self.attrs.keys():   
            output['datetime_first_scan'] = self.attrs['datetime']

        return output

    def check_consistency(self):
        """ Some consistency checks

            Check if the dataset is consistent with the info from the
              header.

            Might be a good idea to move these tests outside the
              class.
        """
        if 'nquan' in self.attrs:
            # Check if the number of variables is equal to nquan
            nquan = int(self.attrs['nquan'])
            if nquan != len(self.keys()):
                module_logger.warning(
                    "It was supposed to has %s variables." % (nquan))

        if 'nvalues' in self.attrs:
            # Check if each variable have nvalues
            nvalues = int(self.attrs['nvalues'])
            for k in self.keys():
                if len(self[k]) != nvalues:
                    module_logger.warning(
                        ("\033[91m%s was supposed to has %s values, "
                        "but found only %s.\033[0m") %
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
        profile.attrs # Return a dictionary with the file header
          masked array
    """
    def __init__(self, filename, defaultsfile=None):

        module_logger.debug('Initializing fCNV class with file: %s' % filename)

        self.filename = filename

        try:
            # Python 3 requires this.
            f = open(filename, "r", encoding="utf-8", errors="replace")
        except:
            f = open(filename, "r")
        text = f.read()
        f.close()

        # if defaultsfile is given, read as a yaml file
        if defaultsfile:
            f = open(defaultsfile)
            defaults = json.loads(f.read())
            f.close()
        else:
            defaults = None

        try:
            super(fCNV, self).__init__(text, defaults)
        except CNVError as e:
            if e.tag == 'noparsingrule':
                e.msg += " File: %s" % self.filename
            raise

        self.name = 'fCNV'
        self.attrs['filename'] = os.path.basename(filename)

    def load_defaults(self, defaultsfile):
        pass
