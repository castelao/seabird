#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from codecs import open


with open('README.rst', encoding='utf-8') as f:
    readme = f.read()

with open('HISTORY.rst', encoding='utf-8') as f:
    history = f.read().replace('.. :changelog:', '')

with open('requirements.txt', encoding='utf-8') as f:
    requirements = f.read()

with open('requirements_dev.txt', encoding='utf-8') as f:
    requirements_test = f.read()

setup(
    name='seabird',
    version='0.10.3',
    description="Parser for Sea-Bird's CTD and TSG.",
    long_description=readme + '\n\n' + history,
    author='Guilherme Castelao , Luiz Irber',
    author_email='guilherme@castelao.net, luiz.irber@gmail.com',
    url='http://seabird.castelao.net',
    packages=[
        'seabird',
    ],
    package_dir={'seabird':
                 'seabird'},
    include_package_data=True,
    install_requires=requirements,
    extras_require={
        'test': requirements_test,
        },
    license='3-clause BSD',
    zip_safe=False,
    keywords='oceanography ocean data CTD TSG SeaBird hydrography parser',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering',
    ],
    entry_points={
        'console_scripts':
            ['seabird=seabird.cli:cli']
    },
    platforms='any',
    scripts=["bin/cnvdump", "bin/cnv2nc"],
)
