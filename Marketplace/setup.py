# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='CSCI-5673-MarketPlace',
    version='0.1.0',
    description='Package for Marketplace Implementation',
    long_description=readme,
    author='Swaminathan Sriram',
    author_email='swsr1249@colorado.edu',
    url='https://github.com/ssnathan30/DistributedSystems',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
