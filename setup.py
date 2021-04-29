from setuptools import find_packages, setup
from ftpdata import __version__

setup(
    name="ftpdata",
    description="A Simple ORM connector for file servers",
    packages=find_packages(exclude=['tests']),
    version=__version__,
    install_requires=['paramiko'],
)
