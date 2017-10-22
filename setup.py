# -*- coding: utf-8 -*-

# Learn more: https://github.com/thanhn9/geocity/setup.py

from setuptools import setup, find_packages

VERSION = '0.1.0'

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='geocity',
    version=VERSION,
    description='Get city proxmity and city keyword querying',
    long_description=readme,
    author='Thanh Nguyen',
    author_email='sibeam@gmail.com',
    url='https://github.com/thanhn9/geocity',
    license=license,
    packages=find_packages(exclude=('docs', 'data'))
)

