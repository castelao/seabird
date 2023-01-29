#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from codecs import open

setup(
    author='Guilherme Castelao , Luiz Irber',
    author_email='guilherme@castelao.net, luiz.irber@gmail.com',
    packages=[
        'seabird',
    ],
    package_dir={'seabird':
                 'seabird'},
    include_package_data=True,
    license='3-clause BSD',
    zip_safe=False,
    platforms='any',
)
