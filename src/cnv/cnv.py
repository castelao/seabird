#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

#import codecs
import yaml
import numpy
from numpy import ma


rule_file = "../rules/cnv.yaml"
cnv_file = "/Users/castelao/work/projects/python/pycnv/test_data/dPIRX003.cnv"

f = open(cnv_file)
text = f.read()
f.close()

print text[:200]

f = open(rule_file)
rule = yaml.load(f.read())

#print "==========================="
#print "Data only"
#print rule['sep']+rule['data']
#content_re = re.compile(rule['sep']+rule['data'], re.VERBOSE)
#print content_re.search(text).group()

class CNV(object):
    def __init__(self, raw_text):
        """
        """
        self.raw_text = text
        self.load_rule()
        self.get_attributes()

    def load_rule(self):
        """ Load the adequate rules to parse the data
        """
        rule_file = "../rules/cnv.yaml"
        f = open(rule_file)
        r = rule['header']+rule['sep']+rule['data']
        if re.search(r,self.raw_text, re.VERBOSE):
            self.rule = yaml.load(f.read())

    def raw_header(self):
        r = self.rule['header']+self.rule['sep']
        content_re = re.compile(r, re.VERBOSE)
        return content_re.search(self.raw_text).groupdict()

    def raw_data(self):
        r = self.rule['sep']+self.rule['data']
        content_re = re.compile(r, re.VERBOSE)
        print r
        return content_re.search(self.raw_text).groupdict()

    def get_attributes(self):
        self.attributes = {}
        #print "Hey hey hey"
        #print self.rule['descriptors']
        #print re.search(self.rule['descriptors'], self.raw_text, re.VERBOSE).groupdict()
     
        print self.raw_header().keys()
        attrib_text = self.raw_header()['descriptors']
        for k in self.rule['descriptors'].keys():
            print k
            self.attributes[k] = re.search(self.rule['descriptors'][k], attrib_text, re.VERBOSE).groups()[0]
        #print attrib_text
        #print re.search(self.rule['descriptors'], attrib_text, re.VERBOSE)
        #self.attributes['names'] = {}
        #data = ma.masked_values([d.split() for d in self.raw_data()['data'].split('\r\n')[:-1]],  float(self.attributes['bad_flag']))
        data = ma.array([d.split() for d in self.raw_data()['data'].split('\r\n')[:-1]], 'f')
        self.data = {}
        self.attributes['names'] = []
        for i, n in enumerate(re.finditer(self.rule['names'],attrib_text, re.VERBOSE)):
            d = n.groupdict()
            #self.attributes['names'] = {'id': int(d['id']), 'name':d['name']}
            self.attributes['names'].append(d['name']) 
            #self.data[d['name']]= ma.array(data[:,i])
            self.data[d['name']]= ma.masked_values(data[:,i], float(self.attributes['bad_flag']))
            #ma.masked_all(int(self.attributes['nvalues']))
