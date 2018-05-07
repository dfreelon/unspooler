from setuptools import setup
setup(
  name = 'unspooler',
  packages = ['unspooler'], # this must be the same as the name above
  version = '1.0.0',
  description = 'unspooler',
  author = 'Deen Freelon',
  author_email = 'dfreelon@gmail.com',
  url = 'https://github.com/dfreelon/unspooler/', # use the URL to the github repo
  download_url = 'https://github.com/dfreelon/unspooler/tarball/1.0', 
  install_requires = ['requests'],
  keywords = ['hyperlink', 'shortlink', 'bit.ly','unshorten'], # arbitrary keywords
  classifiers = [],
)