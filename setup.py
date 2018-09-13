from distutils.core import setup
from setuptools import find_packages

setup(name='pack',
      version='0.1',
      description='My first package',
      author='Alex',
      license='Settings.json',
      author_email='your@email.com',
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True)
