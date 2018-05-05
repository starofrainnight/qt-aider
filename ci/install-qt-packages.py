
import os
import sys
import click
from distutils.version import LooseVersion


@click.command()
@click.argument('python_version')
def main(python_version):
    """Install Qt packages for python with specific version
    """

    python_version = LooseVersion(python_version)
    if python_version >= LooseVersion('3.5'):
        # PyQt5 support python3.5~ x86/x64 with Windows, MacOSX, Linux
        os.system('%s -m pip install PyQt5' % sys.executable)
    elif sys.platform.startswith('win32'):
        if python_version < LooseVersion('3.5'):
            # PySide support python2.6~2.7 x86/x64 and python3.4 x86 with
            # Windows
            os.system('%s -m pip install PySide' % sys.executable)
        else:
            os.system('%s -m pip install PyQt5' % sys.executable)
    elif sys.platform.startswith('linux'):
        # PySide support python2.7 and python3.4 x64 with Linux
        # References: https://stackoverflow.com/questions/24489588/how-can-i-install-pyside-on-travis
        os.system(
            ('%s -m pip install PySide --no-index --find-links '
             'https://parkin.github.io/python-wheelhouse/') % sys.executable)
    else:
        # MacOSX

        # Install prebuilded pyside from qt.io, support python2.7, python3.6
        os.system('%s -m pip install --index-url=http://download.qt.io/snapshots/ci/pyside/5.9/latest/ pyside2 --trusted-host download.qt.io' % sys.executable)


if __name__ == '__main__':
    main()
