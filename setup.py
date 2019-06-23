import setuptools


NAME = 'twitter-match'
VERSION = '0.0.1'


setuptools.setup(
    name=NAME,
    version=VERSION,
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'}
)
