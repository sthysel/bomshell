#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


readme = re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.rst'))
changelog = re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))
long_description = '{}\n{}'.format(readme, changelog)

setup(
    name='bomshell',
    version='0.1.0',
    license='GPLv2',
    description='Retrieve weather data from the Australian Bureau of Meteorology',
    long_description=long_description,
    author='sthysel',
    author_email='sthysel@gmail.com',
    url='https://github.com/sthysel/bomshell',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GPLv2',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    keywords=[],
    install_requires=[
        'click',
        'requests',
        'pyxdg',
        'dbfread'
    ],
    extras_require={},
    setup_requires=[],
    entry_points={
        'console_scripts': [
            'bomshell = bomshell.cli:main',
        ]
    },
)
