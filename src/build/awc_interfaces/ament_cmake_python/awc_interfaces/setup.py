from setuptools import find_packages
from setuptools import setup

setup(
    name='awc_interfaces',
    version='0.0.0',
    packages=find_packages(
        include=('awc_interfaces', 'awc_interfaces.*')),
)
