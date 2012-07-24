from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()


version = '0.1.2'

install_requires = [
    'numpy>=1.1',
    'PyYAML',
]

# Review, rething the classifiers
setup(name='cnv',
    version=version,
    description="Parser for .cnv files, the Sea-Bird CTD data format.",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Scientific/Engineering',
    ],
    keywords='parser oceanography data',
    author='Guilherme Castelao , Roberto de Almeida, Luiz Irber',
    author_email='guilherme@castelao.net,roberto@dealmeida.net, luiz.irber@gmail.com',
    url='https://bitbucket.org/castelao/pycnv/wiki',
    license='PSF',
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['cnv=cnv:main']
    }
)
