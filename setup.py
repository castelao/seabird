#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from codecs import open


with open('requirements_dev.txt', encoding='utf-8') as f:
    requirements_test = f.read()

setup(
    author='Guilherme Castelao , Luiz Irber',
    author_email='guilherme@castelao.net, luiz.irber@gmail.com',
    url='http://seabird.castelao.net',
    packages=[
        'seabird',
    ],
    package_dir={'seabird':
                 'seabird'},
    include_package_data=True,
    license='3-clause BSD',
    zip_safe=False,
    entry_points={
        'console_scripts':
            ['seabird=seabird.cli:cli']
    },
    platforms='any',
    extras_require={
        'test': requirements_test,
        'CDF': ["netCDF4>=1.4"],
        'QC': ["cotede>=0.20.2"]
        }
)
