#!/usr/bin/env python
import os

from distutils.command.install import INSTALL_SCHEMES
from distutils.core import setup

root = os.path.abspath(os.path.dirname(__file__))
os.chdir(root)

VERSION = '0.62.0'

# Make data go to the right place.
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

setup(
    name='django-olwidget',
    version=VERSION,
    description="OpenLayers mapping widget for Django",
    author='Charlie DeTar',
    author_email='cfd@media.mit.edu',
    url='http://olwidget.org',
    packages=['olwidget'],
    package_dir={'': 'django-olwidget'},
    package_data={
        'olwidget': ['static/*', 'templates/*'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: JavaScript',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
