from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
  name = 'sendero',
  packages = ['sendero'],
  package_dir = {'sendero': 'sendero'},
  package_data = {'sendero': ['__init__.py']},
  version = '0.0.2',
  description = 'sendero - data filtering for humans',
  long_description = long_description,
  long_description_content_type='text/markdown',
  author = 'Daniel J. Dufour',
  author_email = 'daniel.j.dufour@gmail.com',
  url = 'https://github.com/DanielJDufour/sendero',
  download_url = 'https://github.com/DanielJDufour/sendero/tarball/download',
  keywords = ['data', 'filter', 'path'],
  classifiers = [
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent'
  ],
  install_requires=[]
)
