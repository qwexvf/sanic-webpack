#!/usr/bin/env python

import sys

try:
    from setuptools import setup
except ImportError:
    print('sanic-webpack needs setuptools in order to build. ' +
          'Install it using your package manager ' +
          '(usually python-setuptools) or via pip (pip install setuptools).')
    sys.exit(1)

setup(name='sanic-webpack',
      version=open('VERSION', 'r').read()[:-1],
      author='Xyz',
      author_email='qw3xvf@gmail.com',
      url='https://github.com/qwexvf/sanic-webpack',
      description='Sanic extension for managing assets with Webpack.',
      license='GPLv3',
      install_requires=['sanic', 'sanic-jinja2'],
      tests_require=['pytest'],
      packages=['sanic_webpack'],
      package_data={'sanic_webpack': ['VERSION']},
      zip_safe=False,
      data_files=[])
