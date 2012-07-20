#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import re
import pkg_resources


import codecs
import yaml
import numpy as np
from numpy import ma


class CNV(object):
    def __init__(self, raw_text):
        """
        """
        self.raw_text = raw_text
        self.load_rule()
        self.get_attributes()
        self.get_datetime()
        self.get_location()
        self.load_data()

    def keys(self):
        """ Return the available keys in self.data
        """
        return self.data.keys()

    def __getitem__(self, key):
        """ Return the key array from self.data
        """
        return self.data[key]

    def load_rule(self):
        """ Load the adequate rules to parse the data

            It should try all available rules, one by one, and use the one
              which fits.
        """
        rule_file = "rules/cnv.yaml"
        text = pkg_resources.resource_string(__name__, rule_file)
        rule = yaml.load(text)
        # Should I load using codec, for UTF8?? Do I need it?
        #f = codecs.open(rule_file, 'r', 'utf-8')
        #rule = yaml.load(f.read())
        r = rule['header'] + rule['sep'] + rule['data']
        if re.search(r, self.raw_text, re.VERBOSE):
            self.rule = rule

    def raw_header(self):
        r = self.rule['header'] + self.rule['sep']
        content_re = re.compile(r, re.VERBOSE)
        return content_re.search(self.raw_text).groupdict()

    def raw_data(self):
        r = self.rule['sep'] + self.rule['data']
        content_re = re.compile(r, re.VERBOSE)
        return content_re.search(self.raw_text).groupdict()

    def get_attributes(self):
        self.attributes = {}
        #print self.rule['descriptors']
        #print re.search(self.rule['descriptors'], 
        #  self.raw_text, re.VERBOSE).groupdict()
     
        print self.raw_header().keys()
        attrib_text = self.raw_header()['descriptors']
        for k in self.rule['descriptors'].keys():
            print k
            self.attributes[k] = re.search(self.rule['descriptors'][k], attrib_text, re.VERBOSE).groups()[0]
        #print attrib_text
        #print re.search(self.rule['descriptors'], attrib_text, re.VERBOSE)
        #self.attributes['names'] = {}

    def load_data(self):
        #data = ma.masked_values([d.split() for d in self.raw_data()['data'].split('\r\n')[:-1]],  float(self.attributes['bad_flag']))
        data = ma.array([d.split() for d in self.raw_data()['data'].split('\r\n')[:-1]], 'f')
        # Talvez usar o np.fromstring(data, sep=" ")
        self.data = {}
        self.attributes['names'] = []
        for i, n in enumerate(re.finditer(self.rule['names'],attrib_text, re.VERBOSE)):
            d = n.groupdict()
            #self.attributes['names'] = {'id': int(d['id']), 'name':d['name']}
            self.attributes['names'].append(d['name']) 
            #self.data[d['name']]= ma.array(data[:,i])
            self.data[d['name']]= ma.masked_values(data[:,i], float(self.attributes['bad_flag']))
            #ma.masked_all(int(self.attributes['nvalues']))
        # Need to better think about this
        if 'timeJ' in self.data.keys():
            dref = self.attributes['datetime']
            dJ0 = datetime(dref.year,1,1)
            try:
                self.data['timeS'] = ma.array([(dJ0-dref + timedelta(float(d))).total_seconds() for d in self['timeJ']])
            except:
                D = [(dJ0-dref + timedelta(float(d))) for d in self['timeJ']]
                self.data['timeS'] = ma.array([d.days*24*60*60+d.seconds for d in D])

    def get_datetime(self):
        """ Extract the reference date and time

            !!! ATENTION, better move it to a rule in the rules.
        """
        datetime.strptime('Aug 28 2008 12:33:46','%b %d %Y %H:%M:%S')
        self.attributes['datetime'] = datetime.strptime(
                self.attributes['start_time'],'%b %d %Y %H:%M:%S')

    def get_location(self):
        """ Extract the station location (Lat, Lon)

            Sometimes the CTD unit station is not connected to the GPS, so it's
              written manually in the headerblob. In that case, I'll try to
              extract it

            !! ATENTION!!! Might be a good idea to store lat,lon as floats
              with min. and sec. as fractions.
        """
        if 'latitude' not in self.attributes:
            lat = re.search(self.rule['latitude'],
                    self.raw_header()['headerblob'],
                    re.VERBOSE).groupdict()
            lat_deg = int(lat['degree'])
            lat_min = float(lat['minute'])
            #self.attributes['lat_deg'] = lat_deg
            #self.attributes['lat_min'] = lat_min
            self.attributes['latitude'] = lat_deg + lat_min/60.
            if lat['hemisphere'] in ['S','s']:
                self.attributes['latitude'] = -1*self.attributes['latitude']

        if 'longitude' not in self.attributes:
            lon = re.search(self.rule['longitude'],
                    self.raw_header()['headerblob'],
                    re.VERBOSE).groupdict()
            lon_deg = int(lon['degree'])
            lon_min = float(lon['minute'])
            #self.attributes['lon_deg'] = lon_deg
            #self.attributes['lon_min'] = lon_min
            self.attributes['longitude'] = lon_deg + lon_min/60.
            if lon['hemisphere'] in ['W','w']:
                self.attributes['longitude'] = -1*self.attributes['longitude']



def press2depth(press, latitude):
    """ calculate depth from pressure
        http://www.seabird.com/application_notes/AN69.htm

        ATENTION, move it to fluid.
    """
    x = np.sin( (np.pi/180) * latitude / 57.29578)**2
    g = 9.780318 * ( 1.0 + ( 5.2788e-3  + 2.36e-5 * x) * x ) + 1.092e-6 * press
    depth = -((((-1.82e-15 * press + 2.279e-10) * press - 2.2512e-5) * press + 9.72659) * press) / g
    return depth
