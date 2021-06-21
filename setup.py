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
 
  1. Setup Docker and run tests
  
  2. Check __version__
  
  3. Build whl
      python setup.py bdist_wheel
      
  4. Upload on Pypi
      twine upload dist/fitdata-{version}-py3-none-any.whl
      
"""