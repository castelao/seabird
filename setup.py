#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

version = '0.6.2'

install_requires = [
    'numpy>=1.1',
    'PyYAML',
]

test_requirements = [
]

setup(
    name='seabird',
    version=version,
    description="Non official parser for Sea-Bird's sensors.",
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
    install_requires=install_requires,
    license='3-clause BSD',
    zip_safe=False,
    keywords='oceanography ocean data CTD SeaBird hydrography parser',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering',
    ],
    download_url='https://pypi.python.org/packages/source/s/seabird/seabird-'+version+'.tar.gz',
    entry_points={
        'console_scripts':
            ['seabird=seabird:main']
    },
    platforms='any',
    scripts=["bin/cnvdump", "bin/cnv2nc"],
    test_suite='tests',
    tests_require=test_requirements
)
