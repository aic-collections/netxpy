version = '0.0.7'

from setuptools import setup

setup(
    name = 'netxpy',
    version = version,
    url = 'http://github.com/aic-collections/netxpy',
    author = 'Kevin Ford',
    author_email = 'kford1@artic.edu',
    license = 'http://www.opensource.org/licenses/bsd-license.php',
    packages = ['netxpy', 'netxpy.methods'],
    #install_requires = install_requires,
    description = 'Interact with NetX API',
    classifiers = [],
    test_suite = 'test',
    include_package_data=True
)
