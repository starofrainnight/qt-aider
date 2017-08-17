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


class my_install_scripts(install_scripts):

    def run(self):
        install_scripts.run(self)

        if sys.platform == "win32":
            shell_script_template = r"""@echo off
			call python "%%~dp0%s" %%*
			"""
            shell_script_ext = ".bat"
        else:
            shell_script_template = r"""#!/bin/sh
			python "$(readlink -f $(dirname $0))/%s" $@
			"""
            shell_script_ext = ""

        for file_path in self.get_outputs():
            file_dir, file_name = os.path.split(file_path)
            froot, ext = os.path.splitext(file_name)
            shell_script_file_name = os.path.join(
                file_dir, froot + shell_script_ext)
            shell_script_contents = shell_script_template % file_name
            if self.dry_run:
                continue

            with open(shell_script_file_name, 'wt') as shell_script_file:
                shell_script_file.write(shell_script_contents)

package_name = 'rabird.qt'

install_requires = [
    'qtpy>=1.3.0',
]

long_description = (
    open('README.rst', 'r').read()
    + '\n' +
    open('CHANGES.rst', 'r').read()
)

setup(
    name=package_name,
    version='0.0.6',
    author='Hong-She Liang',
    author_email='starofrainnight@gmail.com',
    url='https://github.com/starofrainnight/%s' % package_name,
    description='An extension library for PySide',
    long_description=long_description,
    license="Apache Software License",
    classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            'License :: OSI Approved :: Apache Software License',
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Topic :: Software Development :: Libraries",
    ],
    install_requires=install_requires,
    packages=find_packages(),
    namespace_packages=[package_name.split(".")[0]],

    # FIXME: I don't know why we can't use entry_points to install our script,
    # seems that problem related to "package_dir" .
    scripts=['./scripts/rbpyside-i18n-update.py'],
    cmdclass={'install_scripts': my_install_scripts},

    # If we don't set the zip_safe to False, pip can't find us.
    zip_safe=False,
)
