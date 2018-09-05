from distutils.core import setup
setup(
  name = 'pymsteams',
  packages = ['pymsteams'],
  version = '0.1.5',
  description = 'Format messages and post to Microsoft Teams.',
  author = 'Ryan Veach',
  author_email = 'rveach@gmail.com',
  url = 'https://github.com/rveachkc/pymsteams',
  download_url = 'https://github.com/rveachkc/pymsteams/archive/0.1.5.tar.gz',
  keywords = ['Microsoft', 'Teams'], # arbitrary keywords
  classifiers = [],
  install_requires=['requests'],
)
