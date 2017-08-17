#!/usr/bin/env python

from rabird_bootstrap import use_rabird
use_rabird()

import os
import os.path
import sys
import shutil
import logging
import fnmatch
import rabird.core.distutils
from setuptools import setup, find_packages
from distutils.command.install_scripts import install_scripts

package_name = 'rabird.qt'

long_description = (
    open('README.rst', 'r').read()
    + '\n' +
    open('CHANGES.rst', 'r').read()
)

install_requires = [
    'qtpy>=1.3.0',
]

tests_require = [
    # TODO: put package test requirements here
]

setup(
    name=package_name,
    version='0.0.6',
    author='Hong-She Liang',
    author_email='starofrainnight@gmail.com',
    url='https://github.com/starofrainnight/%s' % package_name,
    packages=find_packages(),
    namespace_packages=[package_name.split(".")[0]],
    description='An extension library for Qt library',
    long_description=long_description,
    entry_points={
        'console_scripts': [
            'rbqt-i18n-update=rabird.qt.commands:i18n_update'
        ]
    },
    include_package_data=True,
    install_requires=install_requires,
    license="Apache Software License",
    # If we don't set the zip_safe to False, pip can't find us.
    zip_safe=False,
    keywords=package_name,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: Apache Software License',
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
    ],
    test_suite='tests',
    tests_require=tests_require
)
