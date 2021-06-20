from setuptools import find_packages, setup
from ftpdata import __version__

setup(
    name="ftpdata",
    description="A Simple ORM connector for file servers",
    packages=find_packages(exclude=['testbench']),
    version=__version__,
    install_requires=['paramiko'],
)

"""
 Upload Steps
 
  1. Check __version__
  2. Build whl
      python setup.py bdist_wheel
  
  3. twine upload dist/fitdata-{version}-py3-none-any.whl
"""