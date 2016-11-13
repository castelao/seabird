#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Command line utilities for package Seabird
"""

import click

from seabird.exceptions import CNVError
from .cnv import fCNV
from .netcdf import cnv2nc

@click.group()
def cli():
    """ Utilities for seabird files
    """
    pass

@cli.command(name='cnvdump')
@click.argument('inputfilename', type=click.Path(exists=True))
def dump(inputfilename):
    """ Dump the contents of a CNV file
    """

    try:
        data = fCNV(inputfilename)
    except CNVError as e:
        print("\033[91m%s\033[0m" % e.msg)
        import sys; sys.exit()
    except:
        raise

    print("file: %s" % inputfilename)
    print("Global attributes")
    for a in sorted(data.attributes.keys()):
        print("\t\033[93m%s\033[0m: %s" % (a, data.attributes[a]))

    print("\nVariabes")
    for k in data.keys():
        print("\033[91m%s\033[0m" % k)
        for a in data[k].attributes.keys():
            print("\t\033[93m%s\033[0m: %s" % (a, data[k].attributes[a]))

@cli.command(name='cnv2nc')
@click.option('--outputfilename', default=None,
        help='The output netCDF filename.')
@click.argument('inputfilename', type=click.Path(exists=True))
def nc(inputfilename, outputfilename):
    """ Export a CNV file as a netCDF
    """
    if outputfilename is None:
        outputfilename = inputfilename.replace('.cnv','.nc')
        click.echo('Saving on %s' % outputfilename)
    data = fCNV(inputfilename)
    cnv2nc(data, outputfilename)
