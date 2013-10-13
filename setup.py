from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()


version = '0.4.5'

install_requires = [
    'numpy>=1.1',
    'PyYAML',
]

# Review, rething the classifiers
setup(name='seabird',
    version=version,
    description="A non official package to handle the output of Sea-Bird's CTD.",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Scientific/Engineering',
    ],
    keywords='oceanography ocean data CTD SeaBird hydrography parser',
    author='Guilherme Castelao , Luiz Irber',
    author_email='guilherme@castelao.net, luiz.irber@gmail.com',
    url='http://seabird.castelao.net',
    download_url='http://https://pypi.python.org/packages/source/s/seabird/seabird-'+version+'.tar.gz',
    #download_url='https://github.com/castelao/pycnv/blob/master/dist/cnv-'+version'+.tar.gz?raw=true',
    license='PSF',
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['seabird=seabird:main']
    },
    platforms='any',
    scripts=["bin/cnvdump", "bin/cnv2nc"],
)
